# Agente Experto basado en prompting y MCP usando LangChain y RAG Avanzado

> **Trabajo de Fin de Máster (TFM)** - Máster Universitario en Inteligencia Artificial (UNIR).

Este proyecto implementa un sistema de **Orquestación de un Agente Experto** capaz de ejecutar procesos de negocio complejos y secuenciales. 
Utiliza una arquitectura híbrida mediante el **Model Context Protocol (MCP)**, coordinando los procesos mediante un Agente en Python y haciendo uso de RAG para obtener el detalle del proceso a ejecutar.

## Resumen de la Arquitectura Híbrida

El sistema implementa una arquitectura híbrida porque combina dos ecosistemas tecnológicos unidos en una única pieza "el orquestador".

### Hibridez Cognitiva (Probabilística + Determinista)
Se fusiona la flexibilidad y comprensión del lenguaje de los LLMs con la rigurosidad y fiabilidad de los sistemas de software tradicionales. El LLM es el "operador", pero el código es el "motor".

1. Componente Probabilístico (LLM): El Router y el Planner usan IA Generativa. Entienden el lenguaje natural, infieren intenciones y son creativos adaptándose a lo que pide el usuario. Sus respuestas no son 100% fijas (varían ligeramente).
2. Componente Determinista (Código/RAG): El RAG ancla la información, los documentos determinan categoricamente el proceso que tiene que seguir el LLM sin inventar nada. El Código Java/Python ejecuta acciones estrictas: Una base de datos estrictos y, por lo tanto, ejecuta una acción mediante MCPs si fuese necesario o da error.

Se define una arquitectura de 3 niveles:
1.  **Nivel Cognitivo (Python + LangGraph):**
    * **Planificador Estricto:** Un nodo especializado lee la documentación (RAG) y genera un plan de ejecución inmutable antes de actuar.
    * **Router Semántico:** Clasifica la intención del usuario para decidir qué manual de procedimientos recuperar.
2.  **Nivel de Memoria (RAG Avanzado):**
    * **Parent Document Retriever:** Indexación híbrida que busca por fragmentos pequeños (precisión) pero recupera documentos completos (contexto), garantizando que el LLM vea todas las fases de un proceso.
    * **Qdrant & Local Store:** Base de datos vectorial para búsqueda semántica combinada con almacenamiento local persistente para los documentos padre.
3.  **Nivel de Ejecución (MCP Híbrido):**
    * **Herramientas Locales (Stdio):** Python gestiona operaciones de sistema, BBDD y notificaciones.
    * **Herramientas Remotas (SSE):** Conexión persistente *Server-Sent Events* con un backend Java Spring Boot para lógica de negocio crítica (CRM).


Además, se puede observar capacidades híbridas también en:

1. Hibridez Tecnológica (Políglota)
El uso de MCPs nos permite meidante un lenguaje común comunicar con sistemas escritos en otros lenguajes. Python (El agente experto) se conecta un con una aplicación Java Spring Boot para poder completar uno de los procesos.
2. Hibridez en la Ejecución (Local vs. Remoto)
El agente experto tiene la capacidad de leer herramientas de ejecución local (Stdio) y herramientas http (SSE).

---

## 📂 Estructura del Proyecto

```text
agent_project/
│
├── doc_store_cache/          # [GENERADO] Caché de documentos padres (Pickle)
│   └── ... 
│
├── procesos/                 # [FUENTE] Manuales de procedimientos (.md)
│   ├── alta_cliente.md
│   └── baja_cliente.md
│
├── src/
│   ├── agent/                # Lógica del Agente (Cerebro)
│   │   ├── __init__.py
│   │   ├── agent.py          # Grafo LangGraph
│   │   ├── agent_planner.py  # Planificación del proceso obtenido desde "doc_store_cache"
│   │   ├── agent_state.py    # Definición del Estado (classes)
│   │   ├── user_intention.py # Se analiza el input de usuario para identificar que quiere hacer  
│   │   └── model.py          # Configuración LLM (el de vectorización y el de conversación)
│   │
│   ├── mcps/                 # Herramientas MCP
│   │   ├── servers/          # Definición de los servidores en python que tiene salida stdout (consola).
│   │   ├── utils/            # Definición de los logs a fichero
│   │   ├── __init__.py
│   │   ├── mcp_definition.py # Schemas Pydantic de los MPCs (necesario para indicar al agente los parámetros de los MPCs)
│   │   ├── mcp_mapping.py    # Mapeo a LangChain de los MPCs
│   │   └── mcp_server.py     # Server Stdio (Python) donde se ejecutan los mpcs
│   │
│   ├── rag/                  # RAG Avanzado
│   │   ├── __init__.py
│   │   ├── rag_config.py     # Config Qdrant y modelo de embeddings (bge-m3)
│   │   ├── rag_engine.py     # Definición de las funciones principales del rag
│   │   ├── rag_index.py      # Indexación de los procesos almacenados en formato .md en la carpeta "procesos" del proyecto
│   │   └── rag_retrieval.py  # Creación del objeto de búsqueda en el RAG y en doc_store_cache
│   │
│   ├── __init__.py
│   └── main.py               # Orquestador Principal
│
├── .gitignore                # Exclusiones de Git
├── docker-compose.yml        # Infraestructura Qdrant y MongoDB
├── README.md                 # Documentación
└── requirements.txt          # Dependencias
```

## 🛠️ Requisitos Previos

* **Python:** Versión **3.11** (Estricto, necesario para `asyncio.TaskGroup` y no superior).
* **Java:** JDK 17 o superior (Para el servidor MCP CRM que está en el proyecto de java spring).
* **Docker & Docker Compose:** Para levantar la infraestructura de bases de datos.
* **Ollama:** Instalado localmente para ejecutar el modelo de lenguaje.
* **Modelo qwen2.5:32b** Modelo LLM instalado localmente en ollama para su uso por el agente.
* **Modelo bge-m3** Modelo para embeddings instalado localmente en ollama para su uso por el RAG.

---

## 🚀 Guía de Instalación y Puesta en Marcha

Sigue estos pasos en **estricto orden secuencial** para evitar errores de conexión.

### 1. instalación de los modelos sobre ollama

```bash
ollama pull qwen2.5:32b
ollama pull bge-m3
```

### 2. Instalación de dependencias
Antes de la instalación recuerda crear un entorno aislado de python para el proyecto (generar la carpeta .venv)
```bash
# En la raíz del proyecto
python3.11 -m venv .venv
source .venv/bin/activate
```
Instalar las dependencias
```bash
# En la raíz del proyecto
pip install -r requirements.txt
```

### 3. Infraestructura Base (Qdrant & MongoDB)
El proyecto incluye un archivo `docker-compose.yml` que orquesta la base de datos vectorial y la documental.

```bash
# En la raíz del proyecto (donde está el docker-compose.yml)
docker-compose up -d
```

### 4. Lanzar Agente
```bash
# En la src del proyecto
python3 main.py
```
