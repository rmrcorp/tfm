El problema que estás sufriendo (confusión entre "Alta" y "Baja" cuando ambos textos están presentes) es una limitación clásica de la "Ventana de Atención" de los modelos pequeños (8B). Un modelo de 8B parámetros tiene menos "capacidad cerebral" para sostener dos conceptos contradictorios en la cabeza y elegir el correcto; tiende a mezclarlos.

Un modelo más grande (14B, 32B o 70B) tiene una capacidad de razonamiento y seguimiento de instrucciones exponencialmente superior. Diferencia perfectamente el Alta de la Baja sin necesidad de prompts tan agresivos.

¿Qué modelo debería usar? (La Guía del Experto)
Dependiendo de la memoria RAM/VRAM (Tarjeta Gráfica) que tengas en tu ordenador local, aquí tienes mis recomendaciones para Ollama:

1. Si tienes 12GB - 16GB de VRAM (La opción equilibrada)
👉 Recomendación: Qwen 2.5 (14B) Actualmente, la familia Qwen 2.5 (de Alibaba) está superando a Llama 3.1 en casi todos los benchmarks de lógica y código. El modelo de 14B es mucho más listo que Llama 8B y cabe en tarjetas gráficas medias (RTX 3060/4060 de 12GB o Mac M1/M2/M3 con 16GB).

Comando: ollama pull qwen2.5:14b

2. Si tienes 24GB de VRAM o Mac con 32GB+ (La opción profesional)
👉 Recomendación: Qwen 2.5 (32B) Este es el "punto dulce" actual de la IA local. Tiene un nivel de inteligencia cercano a GPT-4 para tareas de negocio. Es extremadamente difícil confundirlo. Si puedes correr este, tus problemas de "Alta vs Baja" desaparecerán instantáneamente.

Comando: ollama pull qwen2.5:32b

3. La Bestia (Si tienes Mac Studio o Dual GPU)
👉 Recomendación: Llama 3.3 (70B) Es el estado del arte. Razona mejor que muchos humanos. Pero necesitas una máquina muy potente.

Comando: ollama pull llama3.3

Cómo cambiar tu Agente para usar Qwen 2.5 (14B o 32B)
El cambio es trivial. Qwen funciona increíblemente bien con LangChain y Function Calling en las últimas versiones de Ollama.


El Candidato Ideal: Mistral NeMo (12B)Si quieres usar Mistral, este es el que debes instalar.Es un modelo de 12 Billones de parámetros creado conjuntamente por NVIDIA y Mistral AI.Por qué funciona: Esos 4B parámetros extra respecto a Llama 3.1 (8B) marcan una diferencia enorme en capacidad de atención. Tiene una ventana de contexto de 128k tokens, lo que significa que es muy bueno leyendo documentos largos sin perderse.Hardware: Cabe perfectamente en una tarjeta gráfica de 12GB (RTX 3060/4070) o en un Mac con 16GB de RAM.Comando: ollama pull mistral-nemo2. El "Estándar": Mistral 7B (v0.3)Veredicto: No te lo recomiendo para este problema.Razón: Al tener 7B parámetros, tiene la misma limitación cognitiva que Llama 3.1. Es muy rápido, pero ante instrucciones contradictorias ("Aquí dice Alta, aquí dice Baja"), se va a liar igual que te pasa ahora.3. El Peso Pesado: Mistral Small (24B)Veredicto: Una bestia en razonamiento, rivaliza con GPT-3.5/4.Contra: Requiere una tarjeta de 24GB VRAM (RTX 3090/4090) o un Mac con 32GB+ de RAM unificada. Es lento si no tienes buen hardware.Comando: ollama pull mistral-smallComparativa: Qwen 2.5 (14B) vs Mistral NeMo (12B)Dado que te recomendé Qwen 2.5 (14B) antes, aquí tienes la diferencia clave para tu Agente BPM:CaracterísticaQwen 2.5 (14B)Mistral NeMo (12B)Lógica Estricta🏆 Superior. Sigue instrucciones como un robot. Ideal para procesos de negocio rígidos.Muy buena, pero a veces intenta ser más "conversacional".Uso de Herramientas🥇 Excelente. Entiende JSON y esquemas Pydantic mejor que casi nadie en su peso.Bueno, pero a veces falla en el formato exacto de los argumentos.Idioma EspañolMuy bueno.🥇 Nativo y fluido. Mistral suele redactar mejor en idiomas europeos.Separación de ContextoMuy alta. Distingue bien Alta de Baja.Alta. Su gran ventana de contexto ayuda mucho.Mi Recomendación DefinitivaPara un sistema que ejecuta procesos de negocio (BPM) donde un error es crítico (borrar un usuario en vez de crearlo):Tu Opción A (La más segura): qwen2.5:14b. Es más "frío" y calculador, lo cual es perfecto para seguir reglas y manejar herramientas (MCP).Tu Opción B (Si prefieres Mistral): mistral-nemo. Es una gran alternativa si notas que Qwen es demasiado "seco" o si Qwen te da problemas con el español (raro, pero posible).Prueba rápida:Ejecuta esto en tu terminal y cambia el modelo en src/agent.py:Bashollama pull mistral-nemo
Y en el código:Pythonllm = ChatOllama(model="mistral-nemo", temperature=0)
Si Mistral NeMo sigue confundiendo Alta con Baja, entonces ve directo a Qwen 2.5 14B, que es actualmente el rey de la lógica en ese tamaño.