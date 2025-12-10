# Procedimiento: BAJA Y CANCELACIÓN DE CLIENTE
KEYWORDS: eliminar cliente, baja cliente, offboarding, finalizar contrato, borrar usuario, suprimir ficha, cancelación cuenta, cierre expediente, delete, terminar relación.

## 1. Objeto del Procedimiento
Este documento establece el protocolo de actuación para gestionar la finalización de la relación contractual con un **cliente**. El objetivo es garantizar una salida ordenada del titular, asegurando que no queden obligaciones pendientes antes de la desactivación de su ficha.

## 2. Requisitos Previos (Datos Obligatorios)
Para iniciar cualquier expediente de baja, es imprescindible identificar inequívocamente al titular y la causa de la solicitud. El operador debe recabar:

* **Documento de Identidad (DNI/NIF):** Identificador único del cliente a dar de baja.
* **Motivo de la Baja:** Justificación explícita de la salida (Ej: "Insatisfacción precio", "Traslado", "Cierre negocio", "Defunción"). **Es obligatorio registrar la causa** para fines estadísticos y de calidad.

## 3. Flujo del Proceso
El proceso consta de 3 fases críticas que deben ejecutarse secuencialmente. No es posible saltar ninguna fase.

### FASE 1: Identificación y Solicitud
El operador debe solicitar al cliente el DNI y el motivo por el cual desea finalizar su relación como cliente.
* Si el cliente no proporciona el motivo, se le deberá insistir amablemente, ya que el sistema no permite bajas de clientes "en blanco".

### FASE 2: Auditoría de Estado Financiero (Deuda Cero)
Antes de proceder a la baja definitiva del cliente, es **mandatorio** verificar que no existan facturas impagadas o saldos pendientes.
* El sistema deberá consultar el estado de solvencia o deuda actual del cliente.
* **Criterio de Bloqueo:** Si el cliente tiene deudas pendientes (**"MOROSO"**, **"DEUDA PENDIENTE"**, **"SALDO NEGATIVO"**), el proceso de baja **se paralizará cautelarmente**. Se informará al cliente de que debe regularizar su situación financiera antes de poder finalizar el contrato.
* **Criterio de Continuidad:** Solo si el estado financiero es **"APTO"**, **"AL CORRIENTE"** o **"SALDO CERO"**, se autorizará el paso a la siguiente fase.

### FASE 3: Desactivación en Base de Datos
Una vez confirmada la identidad y la ausencia de deudas, se procederá a la actualización de la ficha del cliente en el Repositorio Central (Base de Datos).
* El estado del cliente pasará de "Activo" a **"Baja"**.
* Se deberá registrar la fecha y hora exacta de la operación, así como el motivo proporcionado en la Fase 1.
* Esta acción es definitiva y marca el fin del ciclo de vida del cliente en la compañía.

### FASE 3: Comunicado de baja
* Se enviará un mail indicando que se ha procedido a la baja del usuario, se adjuntará en el texto el motivo de la baja.