# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar el archivo requirements.txt
COPY app/requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY app/. . 

# Exponer el puerto de la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación FastAPI
CMD ["python", "run.py"]

