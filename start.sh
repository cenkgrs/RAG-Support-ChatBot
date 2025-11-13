#!/bin/bash

# Frontend
cd frontend
npm run dev &

# Backend
cd ..
cd backend
source venv/bin/activate
uvicorn main:app --reload