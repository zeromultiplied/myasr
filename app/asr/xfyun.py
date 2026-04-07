import base64
import hashlib
import hmac
import json
import logging
import time
import urllib.parse

import httpx

from app.asr.base import ASRProvider
from app.config import settings

logger = logging.getLogger(__name__)

LFASR_HOST = "https://raasr.xfyun.cn/v2/api"
API_UPLOAD = "/upload"
API_GET_RESULT = "/getResult"


def _generate_signa(app_id: str, secret_key: str, ts: str) -> str:
    """与官方 Ifasr_new.py demo get_signa 完全一致。"""
    m2 = hashlib.md5()
    m2.update((app_id + ts).encode("utf-8"))
    md5 = m2.hexdigest()
    md5 = bytes(md5, encoding="utf-8")
    signa = hmac.new(secret_key.encode("utf-8"), md5, hashlib.sha1).digest()
    signa = base64.b64encode(signa)
    return str(signa, "utf-8")


class XfyunASRProvider(ASRProvider):
    def __init__(self):
        self.app_id = settings.xfyun_app_id
        self.secret_key = settings.xfyun_secret_key
        if not self.app_id or not self.secret_key:
            raise ValueError("XFYUN_APP_ID and XFYUN_SECRET_KEY must be configured")

    def _build_params(self) -> dict:
        ts = str(int(time.time()))
        return {
            "appId": self.app_id,
            "signa": _generate_signa(self.app_id, self.secret_key, ts),
            "ts": ts,
        }

    async def upload(self, audio_data: bytes, filename: str, duration: str = "200") -> str:
        """Upload audio to iFlytek v2 API, return orderId."""
        import os
        params = self._build_params()
        params["fileSize"] = len(audio_data)
        params["fileName"] = filename
        params["duration"] = duration

        url = LFASR_HOST + API_UPLOAD + "?" + urllib.parse.urlencode(params)
        logger.info("XFyun v2 upload: file=%s size=%d", filename, len(audio_data))

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                url,
                headers={"Content-type": "application/json"},
                content=audio_data,
            )
            result = resp.json()
            logger.info("XFyun v2 upload resp: %s", result)

            if result.get("code") != "000000":
                raise RuntimeError(
                    f"XFyun upload failed: {result.get('code')} - {result.get('descInfo')}"
                )
            return result["content"]["orderId"]

    async def get_result(self, order_id: str) -> dict:
        """Query result for an orderId. Returns dict with status and data."""
        params = self._build_params()
        params["orderId"] = order_id
        params["resultType"] = "transfer"

        url = LFASR_HOST + API_GET_RESULT + "?" + urllib.parse.urlencode(params)

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                url,
                headers={"Content-type": "application/json"},
            )
            result = resp.json()

            if result.get("code") != "000000":
                raise RuntimeError(
                    f"XFyun getResult failed: {result.get('code')} - {result.get('descInfo')}"
                )

            order_info = result["content"]["orderInfo"]
            status = order_info["status"]
            order_result = result["content"].get("orderResult")

            # status: 0=created, 3=processing, 4=done, -1=failed
            if status == 4:
                return {"status": "done", "data": order_result}
            elif status == -1:
                # Some failTypes (e.g. 11=predict not enabled) still have transcription data
                if order_result:
                    logger.warning("XFyun order %s status=-1 but has orderResult, treating as done (failType=%s)",
                                   order_id, order_info.get("failType"))
                    return {"status": "done", "data": order_result}
                return {"status": "failed", "data": None}
            else:
                return {"status": "processing", "data": None}

    async def transcribe(self, audio_data: bytes, filename: str) -> str:
        """Upload and poll until done (blocking). For backward compatibility."""
        order_id = await self.upload(audio_data, filename)
        logger.info("XFyun v2 orderId=%s, polling...", order_id)

        timeout = settings.asr_poll_timeout_sec
        interval = settings.asr_poll_interval_sec
        import asyncio
        elapsed = 0

        while elapsed < timeout:
            result = await self.get_result(order_id)

            if result["status"] == "done":
                return self._parse_transcription(result["data"])
            elif result["status"] == "failed":
                raise RuntimeError(f"XFyun transcription failed (orderId={order_id})")

            logger.info("XFyun v2 processing... elapsed=%ds", elapsed)
            await asyncio.sleep(interval)
            elapsed += interval

        raise TimeoutError(f"XFyun ASR timed out after {timeout}s (orderId={order_id})")

    @staticmethod
    def _parse_transcription(order_result: str) -> str:
        """Parse the orderResult JSON to extract transcription text."""
        if not order_result:
            return ""

        try:
            result_data = json.loads(order_result)
        except (json.JSONDecodeError, TypeError):
            return str(order_result)

        # v2 API result format: lattice array with json_1best
        lattice = result_data.get("lattice", [])
        segments = []
        for item in lattice:
            json_1best_str = item.get("json_1best", "")
            if not json_1best_str:
                continue
            try:
                json_1best = json.loads(json_1best_str)
                st = json_1best.get("st", {})
                rt = st.get("rt", [])
                for r in rt:
                    ws = r.get("ws", [])
                    for w in ws:
                        cw = w.get("cw", [])
                        for c in cw:
                            segments.append(c.get("w", ""))
            except (json.JSONDecodeError, TypeError):
                continue

        return "".join(segments)
