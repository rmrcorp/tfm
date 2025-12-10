# Procedimiento: ALTA Y REGISTRO DE NUEVO CLIENTE
KEYWORDS: onboarding, nuevo contrato, registrar cliente, alta servicio, incorporación, new user, creación cuenta, inicio relación comercial.

## 1. Objeto del Procedimiento
El presente documento define las normas y pasos secuenciales para formalizar la entrada de un nuevo cliente en los sistemas de la compañía. 
Este proceso es crítico y debe cumplirse rigurosamente para garantizar la calidad del dato y la seguridad financiera.

## 2. Requisitos Previos (Datos Obligatorios)
Para iniciar cualquier expediente de alta, es obligatorio disponer de la siguiente información completa del titular. 
**No se procederá al registro si falta algún dato**:

* **Documento de Identidad (DNI/NIF):** Debe ser válido y estar vigente.
* **Nombre Completo:** Nombre y dos apellidos (o razón social).
* **Correo Electrónico:** Email corporativo o personal para comunicaciones contractuales.
* **Dirección Postal:** Domicilio fiscal completo para facturación.

## 3. Flujo del Proceso
El proceso consta de 5 fases que deben ejecutarse en estricto orden secuencial.

### FASE 1: Recopilación de Datos
El operador deberá solicitar al solicitante los datos mencionados en el apartado "Requisitos Previos". 
Es responsabilidad del operador verificar que el email tiene un formato correcto y que el DNI es coherente.

### FASE 2: Evaluación de Riesgos (Scoring Financiero)
Antes de registrar al cliente en los sistemas, la empresa exige una comprobación de solvencia crediticia.
* **Criterio de Aceptación:** Si el sistema de scoring devuelve un resultado **"APTO"** o **"VERDE"**, se autoriza el alta inmediata.
* **Criterio de Rechazo:** Si el sistema indica **"NO APTO"**, **"MOROSO"** o **"ROJO"**, el proceso de alta debe **detenerse inmediatamente**. Bajo ningún concepto se registrará a un cliente con evaluación negativa. Se deberá informar al cliente de la imposibilidad de continuar.

### FASE 3: Registro en Base de Datos
Una vez superada la evaluación financiera, se procederá al volcado de los datos (DNI, Nombre, Email, Dirección) en el Repositorio Central de Usuarios (Base de Datos). Este paso genera el "ID de Cliente" oficial.

### FASE 4: Sincronización con CRM Comercial
Una vez creado el usuario en la base de datos, se debe crear la ficha comercial en el CRM de la compañía para que el departamento de ventas tenga visibilidad del nuevo cliente. Se utilizarán los mismos datos validados anteriormente.

### FASE 5: Comunicación de Bienvenida
Como paso final para cerrar el expediente, el sistema debe enviar automáticamente un correo electrónico de bienvenida al cliente, confirmando su alta y proporcionándole sus credenciales de acceso.
