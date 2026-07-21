# Appendix B: Configuration Reference — Resumo

Esta seção do documento (de *Claude-Code-Definitive-Guide.pdf*) cobre a configuração do **Claude Code**. Aqui estão os tópicos principais identificados nos trechos recuperados:

## 1. Onde os Settings Vivem

O Claude Code organiza a configuração em três níveis de escopo:

| Escopo | Localização | Uso |
|---|---|---|
| **User Settings** | `~/.claude/settings.json` | Suas configurações globais, seguem para todos os projetos |
| **Project Settings** | `.claude/settings.json` (no repositório) | Configurado e enviado ao version control — compartilhado pela equipe |
| **Local Settings** | `.claude/settings.local.json` | Sobrescrevimentos por máquina, `.gitignored` — personalizações individuais |

A configuração do projeto (`.claude/settings.json`) compartilha mais do que permissões: inclui hooks, ativação de plugins, variáveis de ambiente padrão e configurações de ferramentas para toda a equipe. Alterações passam por revisão de código.

## 2. Variáveis de Ambiente

O Claude Code suporta mais de **70 variáveis de ambiente**, agrupadas por função. As mais comuns incluem:

- **`CLAUDE_ENV_FILE`**: Persiste variáveis de ambiente ao longo de toda a sessão, sem que o Claude Code precise conhecer o processo de setup. Útil para gerenciadores de versões de linguagem, ambientes virtuais e configurações de CI.
- **Variáveis de Gateway**: Configure a variável de URL base para apontar o Claude Code para o seu gateway em vez de diretamente para o provedor. O gateway gerencia autenticação e roteamento transparentemente. Funciona com acesso API direto, roteamento de provedor de cloud, ou qualquer provedor que suporte a interface API padrão.

## 3. Server Configuration Fields

Há uma seção específica sobre os campos de configuração do servidor, que abrange a infraestrutura e campos de configuração de servidor.

## 4. Model Configuration

Cobre a configuração dos modelos, com campos e variáveis de ambiente relacionados ao modelo utilizado.

## 5. JSON Schema para Settings

O arquivo `.claude/settings.json` contém um JSON Schema referenciado:

```json
"$schema": "https://json.schemastore.org/claude-code-settings.json"
```

---

**Nota**: Esta é uma visão geral baseada nos trechos recuperados. Para detalhes completos de cada campo de configuração, variável de ambiente e schema JSON, seria necessário consultar as seções completas do documento *Claude-Code-Definitive-Guide.pdf*, especificamente o **Appendix B**.