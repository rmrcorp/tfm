package com.tfm.mcpcrm.config;

import com.tfm.mcpcrm.services.CRMTools;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MCPConfig {

    @Bean
    public ToolCallbackProvider syncUserCRM() {
        return MethodToolCallbackProvider.builder().toolObjects(new CRMTools()).build();
    }

}