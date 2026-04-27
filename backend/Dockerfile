# Se utiliza una version de Linux super ligera ya con Python 3.10
FROM python:3.10-slim

# Se crea una carpeta llamada /app adentro del contenedor
WORKDIR /app

# Se copea el archivo de librerias a esa carpeta
COPY requirements.txt .

# Se instalan las librerias sin guardar archivos basura en cache
RUN pip install --no-cache-dir -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu
    
# Se copea todo el codigo (main.py, models.py) al contenedor
COPY . .

# Aviso a Docker que FastAPI se comunicara por este puerto
EXPOSE 8000

# Comando que prende el servidor cuando el contenedor arranca
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]