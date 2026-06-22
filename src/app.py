import json
import os

import pandas as pd
import requests
import streamlit as st


OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"
DATA_DIR = "data"


SYSTEM_PROMPT = """
Você é o Nei, um agente financeiro amigável e didático.

Regras:
- Fale apenas sobre finanças pessoais.
- Não recomende investimentos específicos.
- Use somente os dados fornecidos no contexto.
- Não invente números, produtos, metas ou perfis.
- Se faltar informação, diga: "Não tenho informação suficiente para responder com segurança."
- Responda em: Contexto, Explicação, Próximos passos e Perguntas adicionais.
- Finalize com: "Você quem decide, eu só mostro o caminho."
"""


def carregar_json(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError as erro:
        st.error(f"Erro no JSON: {caminho}")
        st.error(f"Linha {erro.lineno}, coluna {erro.colno}: {erro.msg}")
        st.stop()


@st.cache_data
def carregar_dados():
    historico = pd.read_csv(os.path.join(DATA_DIR, "historico_atendimento.csv"))
    transacoes = pd.read_csv(os.path.join(DATA_DIR, "transacoes.csv"))

    perfil_json = carregar_json(os.path.join(DATA_DIR, "perfil_investidor.json"))
    produtos = carregar_json(os.path.join(DATA_DIR, "produtos_financeiros.json"))

    if isinstance(perfil_json, list):
        perfil = perfil_json[0]
    else:
        perfil = perfil_json

    return historico, transacoes, perfil, produtos


def montar_contexto(historico, transacoes, perfil, produtos):
    entradas = transacoes[transacoes["tipo"] == "entrada"]["valor"].sum()
    saidas = transacoes[transacoes["tipo"] == "saida"]["valor"].sum()
    saldo = entradas - saidas

    gastos = (
        transacoes[transacoes["tipo"] == "saida"]
        .groupby("categoria")["valor"]
        .sum()
        .sort_values(ascending=False)
    )

    resumo_gastos = "\n".join(
        f"- {categoria}: R$ {valor:.2f}"
        for categoria, valor in gastos.items()
    )

    metas = "\n".join(
        f"- {meta.get('meta')}: R$ {meta.get('valor_necessario', 0):.2f} até {meta.get('prazo')}"
        for meta in perfil.get("metas", [])
    )

    ultimas_transacoes = transacoes.tail(10).to_string(index=False)

    return f"""
[DADOS DO CLIENTE]
Nome: {perfil.get("nome")}
Idade: {perfil.get("idade")}
Profissão: {perfil.get("profissao")}
Perfil investidor: {perfil.get("perfil_investidor")}
Objetivo principal: {perfil.get("objetivo_principal")}
Patrimônio total: R$ {perfil.get("patrimonio_total", 0):.2f}
Reserva de emergência: R$ {perfil.get("reserva_emergencia_atual", 0):.2f}
Aceita risco: {perfil.get("aceita_risco")}

[METAS]
{metas}

[RESUMO FINANCEIRO]
Total de entradas: R$ {entradas:.2f}
Total de saídas: R$ {saidas:.2f}
Saldo do período: R$ {saldo:.2f}

[GASTOS POR CATEGORIA]
{resumo_gastos}

[ÚLTIMAS TRANSAÇÕES]
{ultimas_transacoes}

[PRODUTOS DISPONÍVEIS]
{json.dumps(produtos, ensure_ascii=False)}
"""


def perguntar(pergunta, contexto):
    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}
"""

    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 600}
            },
            timeout=120
        )

        r.raise_for_status()
        resposta = r.json().get("response", "").strip()

        return resposta or "Não consegui gerar uma resposta. Tente perguntar de outro jeito."

    except requests.exceptions.ConnectionError:
        return "Não consegui conectar ao Ollama. Verifique se ele está aberto."

    except requests.exceptions.Timeout:
        return "O Ollama demorou demais para responder."

    except Exception as erro:
        return f"Erro inesperado: {erro}"


st.set_page_config(page_title="NEI Financeiro", page_icon="💰")

st.title("💰 NEI - Seu Parça Financeiro")
st.caption("Planejamento financeiro simples, direto e seguro.")

historico, transacoes, perfil, produtos = carregar_dados()
contexto = montar_contexto(historico, transacoes, perfil, produtos)

with st.sidebar:
    st.success("Dados carregados")
    st.write(f"Atendimentos: {len(historico)}")
    st.write(f"Transações: {len(transacoes)}")

    if st.checkbox("Mostrar contexto"):
        st.text(contexto)

if "messages" not in st.session_state:
    st.session_state.messages = []

for mensagem in st.session_state.messages:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta = st.chat_input("Digite sua dúvida sobre finanças...")

if pergunta:
    st.session_state.messages.append({"role": "user", "content": pergunta})

    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("NEI está pensando..."):
            resposta = perguntar(pergunta, contexto)
            st.markdown(resposta)

    st.session_state.messages.append({"role": "assistant", "content": resposta})