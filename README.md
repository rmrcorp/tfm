# Orquestación de Agente Experto Híbrido con Protocolo MCP y RAG Avanzado
Trabajo de Fin de Máster (TFM) - Máster Universitario en Inteligencia Artificial (UNIR).

## Resumen del Proyecto
Este repositorio contiene la implementación completa de un sistema de Agentes Autónomos diseñado para ejecutar procesos de negocio complejos y secuenciales a partir de documentos existentes en entornos empresariales exportados a extensión ".md".
El proyecto resuelve la problemática de la integración de sistemas heterogéneos y la adherencia estricta a procedimientos empresariales mediante una Arquitectura Híbrida. Utiliza el estándar Model Context Protocol (MCP) para coordinar un orquestador en Python apoyándose en técnicas de RAG Avanzado para la recuperación de conocimiento procedimental.

## Arquitectura Híbrida
El núcleo de este TFM reside en su concepción híbrida, la cual está detallada en el README del proyecto agente (agent_project).

## Estructura del Sistema
La solución se divide en 3 niveles lógicos implementados en dos proyectos contenidos en este repositorio:

## Diagrama de Niveles
Nivel Cognitivo (Python): Planificación estricta, Routing semántico y contexto en memoria.

Nivel de Memoria (RAG): Parent Document Retriever sobre Qdrant (Vectorial) y almacenamiento local.

Nivel de Ejecución (MCP): Herramientas distribuidas.

Organización del Repositorio

```text
root/
│
├── agent_project/        # [PYTHON] El Orquestador (Cliente MCP)
│   ├── src/agent/        # Lógica LangGraph, Planner y Router
│   ├── src/rag/          # Motor RAG, Indexación y Qdrant
│   └── src/mcps/         # Cliente MCP y Server Stdio local
│
├── spring_boot_mcp/      # [JAVA] El Backend CRM (Servidor MCP)
│   ├── src/main/java/    # Lógica de Spring AI y Servicios
│   └── build.gradle      # Gestión de dependencias
│
└── docker-compose.yml    # Infraestructura transversal (BBDD)
```

## Guía de Inicio Rápido (Global)
Para levantar el ecosistema completo, es necesario seguir un orden estricto debido a las dependencias de conexión persistente (SSE) del mcp del CRM.

1. Requisitos Previos Globales
- Docker & Docker Compose (Para Qdrant y MongoDB).
- Ollama ejecutándose localmente.
- Python 3.11
- JDK 17. 

2. Preparación de Modelos (Ollama) e infraestructura
Ver documento README de agent_project

3. Ejecución de los Módulos
El sistema requiere que el servidor Java esté activo antes de lanzar el agente Python.

**Paso A**: Backend CRM (Java)
Entra en el directorio del proyecto Java y levanta el servidor:

```bash

cd spring_boot_mcp  # (O el nombre de tu carpeta java)
./gradlew bootRun
```
Esperar: Hasta ver Netty started on port 8080.

**Paso B**: Agente Experto (Python)
En una nueva terminal, entra en el directorio del proyecto Python, activa el entorno y lanza el orquestador:

```bash
cd agent_project
# (Asegúrate de haber instalado dependencias y creado el .venv previamente)
source .venv/bin/activate
python src/main.py
```
Documentación Detallada
Para ver los detalles de implementación, configuración de variables de entorno (.env) e instalación de dependencias específicas, consulta los README de cada sub-proyecto:

Documentación del Agente Python (Orquestador): Detalle sobre LangGraph, configuración del RAG e instalación de requirements.txt.
Documentación del Servidor CRM (Java): Detalle sobre Spring AI, endpoints MCP y compilación con Gradle.
