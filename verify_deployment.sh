#!/bin/bash

# MyASR Vercel 部署验证脚本

echo "=== MyASR Vercel 部署验证 ==="

# 1. 检查关键文件是否存在
echo "1. 检查配置文件..."
files=("vercel.json" ".vercelignore" "DEPLOYMENT.md" "api/main.py" "app/db_postgres.py")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ 缺少: $file"
        exit 1
    fi
done

# 2. 检查前端构建
echo "2. 检查前端构建..."
if [ -d "frontend/dist" ]; then
    echo "   ✓ 前端已构建"
else
    echo "   - 前端未构建 (将在部署时自动构建)"
fi

# 3. 测试 Python 模块导入
echo "3. 测试 Python 模块导入..."
if python3.12 -c "from main import app; print('   ✓ FastAPI 应用导入成功')" 2>/dev/null; then
    echo "   ✓ FastAPI 应用导入成功"
else
    echo "   ✗ FastAPI 应用导入失败"
    exit 1
fi

# 4. 检查数据库模块
echo "4. 检查数据库模块..."
if python3.12 -c "from app.db import init_db; print('   ✓ SQLite 数据库模块正常')" 2>/dev/null; then
    echo "   ✓ SQLite 数据库模块正常"
else
    echo "   ✗ SQLite 数据库模块异常"
    exit 1
fi

# 5. 检查依赖文件
echo "5. 检查依赖配置..."
if grep -q "mangum" requirements.txt && grep -q "psycopg2" requirements.txt; then
    echo "   ✓ 依赖配置完整"
else
    echo "   ✗ 依赖配置不完整"
    exit 1
fi

echo "=== 验证完成! ==="
echo "项目已准备好部署到 Vercel:"
echo "1. 安装 Vercel CLI: npm i -g vercel"
echo "2. 登录: vercel login"
echo "3. 部署: vercel --prod"
echo ""
echo "记得在 Vercel 控制台配置所有环境变量:"
echo "- 讯飞 ASR: XFYUN_APP_ID, XFYUN_SECRET_KEY"
echo "- LLM 提供商: OPENAI_API_KEY, ANTHROPIC_API_KEY 等"