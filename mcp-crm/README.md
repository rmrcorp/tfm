# MCP CRM Server (Spring Boot + Gradle)
Este proyecto implementa un **Servidor MCP (Model Context Protocol)** utilizando **Java Spring Boot** y **Spring AI**.
Actúa como un backend que expone **Herramientas de Negocio (Tools)**  para la operativa de un CRM y poder ser consumidas por un Agente de IA remoto (Python/LangChain) a través de una conexión persistente **SSE (Server-Sent Events)**.
El proyecto está construido y gestionado mediante **Gradle**, asegurando una gestión de dependencias y ciclo de vida de compilación.

---

## Características

* **Protocolo MCP:** Implementación estándar para conectar IA con sistemas externos.
* **Transporte SSE:** Conexión asíncrona y persistente (`/sse`).
* **Spring AI:** Abstracción `@Tool` para convertir métodos Java en capacidades de IA.
* **Build System:** Gradle (con Wrapper incluido para máxima portabilidad).
* **Herramienta Expuesta:** `sincronizarUsuarioCRM` (Simulación de sincronización por DNI).

---

## Requisitos Previos
* **Java:** JDK 17 o superior instalado.
* **No necesitas instalar Gradle globalmente:** El proyecto incluye el **Gradle Wrapper** (`gradlew`), que descargará la versión correcta de Gradle automáticamente la primera vez que lo ejecutes.

---

## Comandos de Gradle (Guía Rápida)
Este proyecto utiliza el Gradle Wrapper. Dependiendo de tu sistema operativo, usa `./gradlew` (Mac/Linux) o `gradlew.bat` (Windows).

### 1. Ejecutar la Aplicación (Modo Desarrollo)
Este es el comando principal para levantar el servidor:

**Mac / Linux:**
```bash
./gradlew bootRun
```

**Windows:**
```bash
gradlew.bat bootRun
```

## Generar jar
**Mac / Linux:**
```bash
./gradlew bootJar
```

**Windows:**
```bash
gradlew.bat bootJar
```


---

## Configuración
La configuración principal se encuentra en `src/main/resources/application.properties`.

| Propiedad | Valor | Descripción |
| :--- | :--- | :--- |
| `server.port` | `8080` | Puerto donde escucha el servidor. |
| `spring.ai.mcp.server.name` | `SpringCrm` | Nombre identificativo del servidor MCP. |
| `spring.ai.mcp.server.sse-endpoint` | `/sse` | Endpoint para establecer la conexión de eventos. |
| `spring.ai.mcp.server.type` | `sync` | Modo de operación (Síncrono). |

### Logging
El nivel de log está configurado para trazar la actividad del protocolo MCP, lo cual es útil para depuración:

```properties
logging.level.io.modelcontextprotocol=trace
logging.level.org.springframework.ai.mcp=trace
```