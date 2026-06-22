# 💰 NEI — O Parça Financeiro

O **NEI** é um agente de Inteligência Artificial Generativa consultivo, proativo e altamente didático voltado para o mercado financeiro. Ele foi desenhado sob a premissa de ser um "tradutor cultural", convertendo jargões técnicos complexos em explicações simples, acessíveis e diretamente conectadas com a realidade financeira do brasileiro comum.

---

## 🚀 Funcionalidades Principais

- **Adaptação Dinâmica de Tom (Inteligência Situacional):** O NEI mapeia o comportamento do usuário e ajusta sua linguagem sem perder seus princípios éticos[cite: 2]. Ele se comunica de formas específicas para 3 públicos-alvo:
  - **Autônomos:** Foco em parceria, flexibilidade e linguagem prática
  - **Aposentados:** Linguagem acolhedora, respeitosa, priorizando segurança e proteção de patrimônio
  - **Jovens Trabalhadores:** Tom descontraído, dinâmico e focado em dar os primeiros passos.
- **Arquitetura RAG Eficiente:** Integração direta com bases locais para leitura de históricos e carteiras em tempo real, evitando sobrecarga no prompt do sistema e garantindo respostas rápidas.
- **Filtro Antialucinação e Escopo Rígido:** Respostas estritamente fundamentadas no catálogo de produtos reais do banco, com diretrizes claras para recusar palpites de mercado, suporte técnico ou transações diretas.

---

## 📊 Base de Dados e Conhecimento

A base estruturada do repositório foi otimizada e conta com dados simulados realistas para o funcionamento do agente:
- **`perfil_investidor.json`**: Definição de perfis de risco (Conservador, Moderado e Arrojado).
- **`produtos_financeiros.json`**: Portfólio contendo opções completas de investimento (Renda Fixa, Previdência, Fundos e ativos de volatilidade).
- **Históricos (`transacoes.csv` e `historico_atendimento.csv`)**: Registros expandidos para contextualizar as finanças e os comportamentos de consumo de cada cliente simulado.

---

## 🛠️ Tecnologias Utilizadas

- **Interface do Usuário:** Streamlit
- **Processamento de Dados:** Python e Pandas
- **Modelos de Linguagem:** Integrações via APIs (como OpenAI) ou modelos locais via Ollama[cite: 2].

---

## 📁 Estrutura do Repositório
├── 📁 data/                  # Fontes de dados JSON e CSV (perfis, produtos e transações)
├── 📁 docs/                  # Concepção do agente, engenharia de prompts e métricas
├── 📁 src/                   # Código-fonte do sistema
│   ├── app.py                # Interface web (Streamlit)
│   ├── agente.py             # Lógica de orquestração do RAG e LLM
│   └── requirements.txt      # Dependências do projeto
└── 📄 README.md              # Visão geral do projeto

---

## 🔧 Como Executar a Solução

1. Certifique-se de ter o Python instalado em sua máquina.
2. Instale as dependências obrigatórias:
```bash
   pip install -r src/requirements.txt
```
Configure suas credenciais de ambiente para os modelos de IA utilizados.

Execute o servidor do Streamlit para testar a interface:

```Bash
   streamlit run src/app.py
```
