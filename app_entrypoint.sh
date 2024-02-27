#!/bin/bash
echo "Running parser"
python src/main.py &

cd src/web
echo "Running server"
uvicorn app:app --host=0.0.0.0 --reload