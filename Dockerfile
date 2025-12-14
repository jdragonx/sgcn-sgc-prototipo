FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY pyproject.toml ./

# Instalar dependencias de Python
RUN pip install uv && uv sync --frozen

# Copiar código de la aplicación
COPY . .

# Crear directorio para uploads
RUN mkdir -p uploads/documents

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

