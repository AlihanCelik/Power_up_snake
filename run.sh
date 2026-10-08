#!/bin/bash
# Power-up Snake Başlatıcı (MacOS / Linux)

# Sanal ortam kontrolü ve çalıştırma
if [ -d ".venv" ]; then
    source .venv/bin/activate
    python3 main.py
else
    python3 main.py
fi
