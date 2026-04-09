from fastapi import FastAPI
from mangum import Mangum

from main import app

# 包装 FastAPI 应用以在 Serverless 环境中运行
handler = Mangum(app)