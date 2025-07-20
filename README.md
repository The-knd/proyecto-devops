# Proyecto DevOps - API de Gestión de Clientes, Productos y Ventas

## 📋 Descripción

Este proyecto implementa una solución DevOps integral que abarca todas las fases del ciclo de vida de una aplicación, desde el versionamiento del código hasta el monitoreo en producción. La aplicación base es una API REST desarrollada en FastAPI para la gestión de clientes, productos y ventas.

## 🏗️ Arquitectura del Sistema

### Componentes Principales

- **FastAPI Application**: API REST para gestión de clientes, productos y ventas
- **Docker**: Contenerización de la aplicación
- **GitHub Actions**: Pipeline CI/CD automatizado
- **Nexus Repository**: Almacenamiento de artefactos Docker
- **Prometheus**: Recolección de métricas
- **Grafana**: Visualización de métricas y dashboards
- **EC2 (AWS)**: Entorno de producción

### Diagrama de Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Repo   │    │  GitHub Actions │    │   EC2 Instance  │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Source Code │ │───▶│ │ CI/CD       │ │───▶│ │ FastAPI     │ │
│ │             │ │    │ │ Pipeline    │ │    │ │ Container   │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    │                 │
                                              │ ┌─────────────┐ │
                                              │ │ Nexus       │ │
                                              │ │ Repository  │ │
                                              │ └─────────────┘ │
                                              │                 │
                                              │ ┌─────────────┐ │
                                              │ │ Prometheus  │ │
                                              │ │ Metrics     │ │
                                              │ └─────────────┘ │
                                              │                 │
                                              │ ┌─────────────┐ │
                                              │ │ Grafana     │ │
                                              │ │ Dashboards  │ │
                                              │ └─────────────┘ │
                                              └─────────────────┘
```

## 🚀 Endpoints de la API

### Base URL
```
http://ec2-13-218-98-122.compute-1.amazonaws.com:5000
```

### Endpoints Disponibles

#### 1. Gestión de Clientes

**POST /clients** - Crear un nuevo cliente
```bash
curl -X POST http://ec2-13-218-98-122.compute-1.amazonaws.com:5000/clients \
  -H "Content-Type: application/json" \
  -d '{"name": "Juan Pérez"}'
```

**GET /clients** - Listar todos los clientes
```bash
curl http://ec2-13-218-98-122.compute-1.amazonaws.com:5000/clients
```

#### 2. Gestión de Productos

**POST /products** - Crear un nuevo producto
```bash
curl -X POST http://ec2-13-218-98-122.compute-1.amazonaws.com:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99}'
```

**GET /products** - Listar todos los productos
```bash
curl http://ec2-13-218-98-122.compute-1.amazonaws.com:5000/products
```

#### 3. Gestión de Ventas

**POST /sales** - Registrar una nueva venta
```bash
curl -X POST http://ec2-13-218-98-122.compute-1.amazonaws.com:5000/sales \
  -H "Content-Type: application/json" \
  -d '{"client_id": "<client_id>", "product_id": "<product_id>", "quantity": 2}'
```

**GET /sales** - Listar todas las ventas
```bash
curl http://ec2-13-218-98-122.compute-1.amazonaws.com:5000/sales
```

#### 4. Métricas

**GET /metrics** - Obtener métricas Prometheus
```bash
curl http://ec2-13-218-98-122.compute-1.amazonaws.com:5000/metrics
```

## 🐳 Contenerización

### Dockerfile
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/. .
EXPOSE 5000
CMD ["python", "run.py"]
```

### Docker Compose (FastAPI)
```yaml
services:
  fastapi:
    image: fastapi-app:latest
    build: .
    ports:
      - "5000:5000"
    environment:
      - PYTHONUNBUFFERED=1
```

### Docker Compose (Servicios de Infraestructura)
```yaml
services:
  nexus:
    image: sonatype/nexus3
    ports:
      - "8081:8081"
    volumes:
      - nexus-data:/nexus-data

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - prometheus-data:/prometheus
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
    volumes:
      - grafana-data:/var/lib/grafana
```

## 🔄 Pipeline CI/CD

### Flujo del Pipeline

1. **Build**: Construcción de la imagen Docker en GitHub Actions
2. **Test**: Ejecución de pruebas unitarias dentro del contenedor en EC2
3. **Deploy**: Despliegue automático en EC2
4. **Push to Nexus**: Almacenamiento de la imagen en Nexus Repository
5. **Monitoring**: Exposición de métricas para Prometheus

### Archivo de Workflow
```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  build-push-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker image
      - name: Deploy and test on EC2
      - name: Push to Nexus Repository
```

### Secrets Requeridos
- `EC2_HOST`: IP pública de la instancia EC2
- `EC2_USER`: Usuario SSH de la EC2
- `EC2_KEY`: Clave privada SSH para la EC2
- `NEXUS_EC2_PORT`: Puerto del Docker registry de Nexus (ej: 8082)
- `NEXUS_REPO`: Nombre del repositorio en Nexus
- `NEXUS_USER`: Usuario de Nexus
- `NEXUS_PASSWORD`: Contraseña de Nexus

## 🧪 Pruebas

### Pruebas Unitarias
Las pruebas se ejecutan automáticamente en el pipeline CI/CD y cubren:

- **test_root()**: Verificación del endpoint raíz
- **test_metrics()**: Verificación del endpoint de métricas
- **test_create_and_list_clients()**: Creación y listado de clientes
- **test_create_and_list_products()**: Creación y listado de productos
- **test_create_and_list_sales()**: Creación y listado de ventas
- **test_sale_with_invalid_ids()**: Validación de errores en ventas

### Ejecución de Pruebas
```bash
# Localmente
cd app
pytest test_app.py

# En el contenedor
docker exec <container_id> pytest test_app.py
```

## 📊 Monitoreo

### Prometheus
- **URL**: `http://ec2-13-218-98-122.compute-1.amazonaws.com:9090`
- **Configuración**: `prometheus/prometheus.yml`
- **Targets**: FastAPI app en puerto 5000

### Grafana
- **URL**: `http://ec2-13-218-98-122.compute-1.amazonaws.com:3000`
- **DataSource**: Prometheus
- **Dashboards**: Métricas de la aplicación FastAPI

### Métricas Expuestas
- `http_requests_total`: Contador total de peticiones HTTP
- `http_request_duration_seconds`: Latencia de las peticiones HTTP

## 🚀 Despliegue

### Despliegue Manual
```bash
# En la EC2
cd /home/ec2-user/proyecto-devops
docker-compose -f docker-compose.fastapi.yaml up -d
```

### Despliegue Automático
El despliegue se realiza automáticamente mediante el pipeline de GitHub Actions cuando se hace push a las ramas `main` o `develop`.

## 📁 Estructura del Proyecto

```
proyecto-devops/
├── app/
│   ├── src/
│   │   ├── __init__.py          # Configuración de FastAPI
│   │   ├── routes.py            # Endpoints de la API
│   │   └── metrics.py           # Configuración de métricas
│   ├── requirements.txt         # Dependencias Python
│   ├── run.py                   # Punto de entrada
│   └── test_app.py              # Pruebas unitarias
├── prometheus/
│   └── prometheus.yml           # Configuración de Prometheus
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # Pipeline CI/CD
├── docker-compose.yaml          # Servicios de infraestructura
├── docker-compose.fastapi.yaml  # Servicio FastAPI
├── Dockerfile                   # Imagen de la aplicación
└── README.md                    # Documentación
```

## 🔧 Configuración

### Variables de Entorno
```bash
# EC2
EC2_PATH=/home/ec2-user/proyecto-devops/

# Nexus
NEXUS_EC2_HOST=<IP_EC2>
NEXUS_EC2_PORT=8082
NEXUS_REPO=docker-hosted
NEXUS_USER=<usuario>
NEXUS_PASSWORD=<contraseña>
```

### Puertos Utilizados
- **5000**: FastAPI Application
- **8081**: Nexus Web UI
- **8082**: Nexus Docker Registry
- **9090**: Prometheus
- **3000**: Grafana

## 🛠️ Desarrollo Local

### Prerrequisitos
- Docker
- Docker Compose
- Python 3.9+

### Ejecución Local
```bash
# Clonar el repositorio
git clone <repository-url>
cd proyecto-devops

# Construir y ejecutar la aplicación
docker build -t fastapi-app .
docker run -p 5000:5000 fastapi-app

# O usar Docker Compose
docker-compose -f docker-compose.fastapi.yaml up -d
```

### Ejecutar Pruebas Localmente
```bash
cd app
pip install -r requirements.txt
pytest test_app.py
```

## 🔍 Troubleshooting

### Problemas Comunes

1. **Error de permisos en fastapi-app.tar**
   ```bash
   chmod 644 fastapi-app.tar
   ```

2. **Error de conexión a Nexus**
   - Verificar que Nexus esté corriendo en la EC2
   - Verificar puertos y credenciales

3. **Error de importación en FastAPI**
   - Verificar que el import en `run.py` sea `from src import app`

4. **Tests fallando**
   - Verificar que `httpx` esté en `requirements.txt`
   - Verificar que el contenedor esté corriendo

### Logs Útiles
```bash
# Logs de FastAPI
docker logs <fastapi_container_id>

# Logs de Nexus
docker logs proyecto-devops-nexus-1

# Logs de Prometheus
docker logs proyecto-devops-prometheus-1

# Logs de Grafana
docker logs proyecto-devops-grafana-1
```

## 📈 Métricas y Monitoreo

### Acceso a Dashboards
- **Prometheus**: `http://ec2-13-218-98-122.compute-1.amazonaws.com:9090`
- **Grafana**: `http://ec2-13-218-98-122.compute-1.amazonaws.com:3000`

### Métricas Clave
- Tasa de peticiones HTTP por endpoint
- Latencia de respuesta
- Estado de salud de la aplicación
- Uso de recursos del contenedor

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Equipo DevOps** - *Trabajo inicial* - [ProyectoDevOps]

## 🙏 Agradecimientos

- FastAPI por el framework web
- Prometheus y Grafana por las herramientas de monitoreo
- Sonatype Nexus por el repositorio de artefactos
- GitHub Actions por la automatización CI/CD