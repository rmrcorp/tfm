package com.tfm.mcpcrm.services;

import org.springframework.ai.tool.annotation.Tool;

public class CRMTools {

    @Tool(description = "Sincroniza un usuario en el CRM a través del DNI")
    public String sincronizarUsuarioCRM(String dni) {
        System.out.print("Cliente sincronizado!!!! con el CRM!!!!");
        return "Usuario sincronizado con exito " + dni;
    }

}
