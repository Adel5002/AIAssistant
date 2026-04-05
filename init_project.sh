#!/bin/bash

PROJECT_NAME="assistant_bot"

echo "Creating project structure for $PROJECT_NAME..."

# Создаем всю иерархию папок одной командой
mkdir -p $PROJECT_NAME/{bot/{handlers,middlewares,keyboards,states},core/database,services,data,migrations}

cd $PROJECT_NAME

# Создаем базовые файлы в корне
touch main.py requirements.txt .env .gitignore

# Инициализируем python-пакеты и файлы логики
touch bot/__init__.py bot/{handlers,middlewares,keyboards,states}/__init__.py
touch core/__init__.py core/config.py core/database/__init__.py
touch services/__init__.py services/{ai_service.py,excel_engine.py,scheduler.py,storage.py}

# Добавим стандартный .gitignore для Python
echo "venv/
__pycache__/
*.pyc
.env
data/*
!data/.gitkeep" > .gitignore

echo -e "\n[DONE] Structure created successfully!"
echo "Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. python3 -m venv venv"
echo "3. source venv/bin/activate"
