import streamlit as st
import requests
import json
import locale
from datetime import datetime

def get_prediction(data):
    """
    Função para obter a predição da API.

    Args:
        data (dict): Dados no formato esperado pela API.

    Returns:
        str: Predição da categoria.
    """
    print(json.dumps(data))

    endpoint = st.secrets["API-ENDPOINT"]
    api_key = st.secrets["API-KEY"]  # Certifique-se de que a chave da API é uma string
    headers = {'x-api-key': str(api_key), 'Content-Type': 'application/json'}

    response = requests.post(endpoint, data=json.dumps(data), headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(result)

        if 'body' in result:
            result_body = json.loads(result['body'])
            if result_body and 'prediction' in result_body[0]:
                prediction = result_body[0]['prediction']
                st.markdown(f"### Setor de atendimento:\n\nDe acordo com seu relato, você será direcionado para o setor abaixo, que entrará em contato em breve para atendimento especializado.\n\n**{prediction}**.")
            else:
                st.markdown("Houve um problema na consulta. Revise os dados.")
        else:
            st.markdown("Houve um problema na consulta. Revise os dados.")
    else:
        st.markdown("Houve um problema na consulta. Revise os dados.")

# Interface do usuário do Streamlit
st.title("QuantumFinance - Atendimento ao Cliente 📞")

st.markdown("## Bem-vindo ao serviço de atendimento ao cliente da QuantumFinance! ")
st.markdown("### Por favor, insira sua mensagem abaixo:")

# Entrada do usuário
user_input = st.text_area("Descrição da Mensagem", "")

if st.button("Enviar"):
    if user_input:
        # Gerar id_reclamacao baseado no horário atual
        now = datetime.now()
        id_reclamacao = int(now.timestamp())
        data_abertura = now.strftime("%Y-%m-%d")

        # Criar o payload
        data = {
            "data": [
                {
                    "id_reclamacao": id_reclamacao,
                    "data_abertura": data_abertura,
                    "descricao_reclamacao": user_input
                }
            ]
        }

        # Chamar a função de predição
        get_prediction(data)
    else:
        st.error("Por favor, insira a descrição da Mensagem.")
