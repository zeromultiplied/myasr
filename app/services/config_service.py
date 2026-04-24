import json
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from app.config import settings
from app.db import _get_conn


class ConfigService:
    """Service for managing system configuration with profile support."""

    @staticmethod
    def create_profile(name: str, description: str = None) -> int:
        """Create a new configuration profile."""
        conn = _get_conn()
        cursor = conn.execute(
            "INSERT INTO config_profiles (name, description) VALUES (?, ?)",
            (name, description)
        )
        profile_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return profile_id

    @staticmethod
    def get_profile(profile_id: int) -> Optional[Dict]:
        """Get a configuration profile by ID."""
        conn = _get_conn()
        row = conn.execute(
            "SELECT * FROM config_profiles WHERE id = ?", (profile_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return dict(row)

    @staticmethod
    def list_profiles() -> List[Dict]:
        """List all configuration profiles."""
        conn = _get_conn()
        rows = conn.execute(
            "SELECT * FROM config_profiles ORDER BY created_at DESC"
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def update_profile(profile_id: int, **kwargs) -> bool:
        """Update a configuration profile."""
        if not kwargs:
            return False

        conn = _get_conn()
        kwargs["updated_at"] = datetime.now().isoformat()
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values())
        values.append(profile_id)

        cursor = conn.execute(
            f"UPDATE config_profiles SET {sets} WHERE id = ?", values
        )
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    @staticmethod
    def delete_profile(profile_id: int) -> bool:
        """Delete a configuration profile."""
        conn = _get_conn()
        cursor = conn.execute(
            "DELETE FROM config_profiles WHERE id = ?", (profile_id,)
        )
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    @staticmethod
    def set_default_profile(profile_id: int) -> bool:
        """Set a profile as the default configuration."""
        conn = _get_conn()

        # First, unset any existing default
        conn.execute("UPDATE config_profiles SET is_default = 0")

        # Then set the new default
        cursor = conn.execute(
            "UPDATE config_profiles SET is_default = 1 WHERE id = ?", (profile_id,)
        )
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    @staticmethod
    def get_default_profile() -> Optional[Dict]:
        """Get the default configuration profile."""
        conn = _get_conn()
        row = conn.execute(
            "SELECT * FROM config_profiles WHERE is_default = 1"
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return dict(row)

    @staticmethod
    def save_provider_config(
        profile_id: int,
        provider_type: str,
        provider_name: str,
        api_key: str = None,
        base_url: str = None,
        model_name: str = None,
        priority: int = 1,
        is_active: bool = True
    ) -> int:
        """Save provider configuration for a profile."""
        conn = _get_conn()

        # Check if config already exists
        existing = conn.execute(
            "SELECT id FROM provider_configs WHERE profile_id = ? AND provider_type = ? AND provider_name = ?",
            (profile_id, provider_type, provider_name)
        ).fetchone()

        if existing:
            # Update existing config
            cursor = conn.execute(
                """UPDATE provider_configs SET
                    api_key = ?, base_url = ?, model_name = ?, priority = ?, is_active = ?, updated_at = ?
                    WHERE id = ?""",
                (api_key, base_url, model_name, priority, is_active, datetime.now().isoformat(), existing["id"])
            )
            config_id = existing["id"]
        else:
            # Insert new config
            cursor = conn.execute(
                """INSERT INTO provider_configs
                    (profile_id, provider_type, provider_name, api_key, base_url, model_name, priority, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (profile_id, provider_type, provider_name, api_key, base_url, model_name, priority, is_active)
            )
            config_id = cursor.lastrowid

        conn.commit()
        conn.close()
        return config_id

    @staticmethod
    def get_provider_config(profile_id: int, provider_type: str, provider_name: str) -> Optional[Dict]:
        """Get provider configuration for a profile."""
        conn = _get_conn()
        row = conn.execute(
            "SELECT * FROM provider_configs WHERE profile_id = ? AND provider_type = ? AND provider_name = ?",
            (profile_id, provider_type, provider_name)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return dict(row)

    @staticmethod
    def list_provider_configs(profile_id: int, provider_type: str = None) -> List[Dict]:
        """List provider configurations for a profile."""
        conn = _get_conn()
        if provider_type:
            rows = conn.execute(
                "SELECT * FROM provider_configs WHERE profile_id = ? AND provider_type = ? ORDER BY priority",
                (profile_id, provider_type)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM provider_configs WHERE profile_id = ? ORDER BY provider_type, priority",
                (profile_id,)
            ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def delete_provider_config(config_id: int) -> bool:
        """Delete a provider configuration."""
        conn = _get_conn()
        cursor = conn.execute(
            "DELETE FROM provider_configs WHERE id = ?", (config_id,)
        )
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    @staticmethod
    def get_active_config() -> Dict[str, Any]:
        """Get the active configuration (combines database and .env settings)."""
        config = {}

        # Get default profile
        default_profile = ConfigService.get_default_profile()
        if not default_profile:
            # Fall back to .env settings
            config.update({
                "xfyun_app_id": settings.xfyun_app_id,
                "xfyun_secret_key": settings.xfyun_secret_key,
                "default_llm_provider": settings.default_llm_provider,
                "openai_api_key": settings.openai_api_key,
                "openai_base_url": settings.openai_base_url,
                "openai_model": settings.openai_model,
                "anthropic_api_key": settings.anthropic_api_key,
                "anthropic_model": settings.anthropic_model,
                "ollama_base_url": settings.ollama_base_url,
                "ollama_model": settings.ollama_model,
                "log_level": settings.log_level,
                "max_audio_size_mb": settings.max_audio_size_mb,
                "asr_poll_interval_sec": settings.asr_poll_interval_sec,
                "asr_poll_timeout_sec": settings.asr_poll_timeout_sec,
            })
            return config

        # Get provider configurations for the default profile
        provider_configs = ConfigService.list_provider_configs(default_profile["id"])

        # Organize by provider type
        config["profile"] = default_profile
        config["providers"] = {}

        for provider in provider_configs:
            provider_type = provider["provider_type"]
            provider_name = provider["provider_name"]

            if provider_type not in config["providers"]:
                config["providers"][provider_type] = {}

            config["providers"][provider_type][provider_name] = {
                "api_key": provider["api_key"],
                "base_url": provider["base_url"],
                "model_name": provider["model_name"],
                "priority": provider["priority"],
                "is_active": bool(provider["is_active"])
            }

        # Fall back to .env settings for any missing values
        env_mapping = {
            "asr": {
                "iflytek": {
                    "api_key": settings.xfyun_secret_key,
                    "app_id": settings.xfyun_app_id
                }
            },
            "llm": {
                "openai": {
                    "api_key": settings.openai_api_key,
                    "base_url": settings.openai_base_url,
                    "model_name": settings.openai_model
                },
                "anthropic": {
                    "api_key": settings.anthropic_api_key,
                    "model_name": settings.anthropic_model
                },
                "ollama": {
                    "base_url": settings.ollama_base_url,
                    "model_name": settings.ollama_model
                }
            }
        }

        # Apply fallbacks
        for provider_type, providers in env_mapping.items():
            if provider_type not in config["providers"]:
                config["providers"][provider_type] = {}

            for provider_name, fallback_config in providers.items():
                if provider_name not in config["providers"][provider_type]:
                    config["providers"][provider_type][provider_name] = fallback_config
                else:
                    # Fill in missing values with fallbacks
                    current = config["providers"][provider_type][provider_name]
                    for key, value in fallback_config.items():
                        if not current.get(key):
                            current[key] = value

        return config