# Frontend
cd frontend

# Gereksinimleri Yükle
npm install

# Frontend ayağa kaldır
npm run dev &

# Backend
cd ..
cd backend

# Virtual env oluştur
python3 -m venv venv

# Aktif et
source venv/bin/activate

# Gereksinimleri Yükle
pip install -r requirements.txt

# Uvicorn ile ayağa kadlır
uvicorn main:app --reload

Frontend 5173, Backend 8000 port da açılır