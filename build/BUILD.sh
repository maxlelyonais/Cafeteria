cd ../Cafeteria
pyinstaller --add-data "main.kv:." --add-data ".env:." --icon="../build/icon.ico" Cafeteria.py

cd ./dist