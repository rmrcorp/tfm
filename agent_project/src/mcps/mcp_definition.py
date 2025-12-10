from pydantic import BaseModel, Field

# --- DEFINICIÓN DE ESQUEMAS DE ENTRADA  ---

class SolvenciaInput(BaseModel):
    dni: str = Field(..., description="DNI o NIF del cliente a consultar (Ej: 12345678A)")

class GuardarClienteInput(BaseModel):
    dni: str = Field(..., description="Identificador único (DNI/NIF)")
    nombre_completo: str = Field(..., description="Nombre y Apellidos completos")
    email: str = Field(..., description="Email corporativo o personal")
    direccion: str = Field(..., description="Dirección fiscal completa")

class BajaClienteInput(BaseModel):
    dni: str = Field(..., description="DNI del cliente a dar de baja")
    motivo: str = Field(..., description="Razón o motivo de la baja")


class EmailInput(BaseModel):
    destinatario: str = Field(..., description="Email del receptor")
    asunto: str = Field(..., description="Asunto del correo")
    cuerpo: str = Field(..., description="Texto del mensaje")

class CrmJavaInput(BaseModel):
    dni: str = Field(..., description="DNI del usuario para el CRM")
