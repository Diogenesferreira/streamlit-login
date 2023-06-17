import streamlit as st
from conexao import DataBase
import time
from pathlib import Path
import streamlit as st

# Obter o caminho absoluto da pasta do projeto
diretorio_projeto = Path.cwd() / 'db'

#Crio um banco de dados usando a Classe DataBase
banco = DataBase(diretorio_projeto, 'autenticacao.db')

#Função que autentica o usuario usando parametros das classes a baixo
def autenticar_usuario(login, senha):
    validar_usuario = banco.usuario_existe(login)
    login_bd, senha_bd = banco.autenticar_usuario(login), banco.autenticar_senha(login)
    
    if validar_usuario:
        if login == login_bd and senha == senha_bd:
            return True
        else:
            st.error('Usuário ou senha inválidos!', icon="🚨")
    else:
        st.error('Usuário não cadastrado')

    return False

def login_page():
    st.title("Página de Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])  # Define as colunas para ajustar o layout
    
    with col2:  # Usa a coluna do meio para o container do formulário
        with st.form(key='autenticacao'):
            input_login = st.text_input(label='Usuário')
            input_senha = st.text_input(label='Senha', type="password")
            input_botao = st.form_submit_button('Fazer Login')

    if input_botao:
        if autenticar_usuario(input_login, input_senha):
            with st.spinner('Autenticando Usuário'):
                time.sleep(1)
                st.success('Logado!!!')
                
                # Oculta a seção de login
                st.session_state['logged_in'] = True
                
                # Atualiza a página para exibir a nova seção
                st.experimental_rerun()
                
def main_page():
    st.title("Página Principal")
    # Adiciona uma barra lateral à esquerda
    st.sidebar.title("Barra Lateral")

# Verifica se o usuário está logado ou não
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login_page()
else:
    main_page()



