import streamlit as st
import json

def salvar_usuarios(usuarios):
    # Salvar a lista de usuários no arquivo JSON
    with open("usuarios.json", "w") as arquivo:
        json.dump(usuarios, arquivo)

def carregar_usuarios():
    # Ler dados existentes do arquivo JSON (se houver)
    try:
        with open("usuarios.json", "r") as arquivo:
            usuarios = json.loads(arquivo.read())
    except FileNotFoundError:
        usuarios = []

    return usuarios

def verificar_acesso(usuario, senha):
    # Ler dados existentes do arquivo JSON
    usuarios = carregar_usuarios()

    # Verificar se o usuário e a senha correspondem a algum usuário no arquivo JSON
    for user in usuarios:
        if user["usuario"] == usuario and user["senha"] == senha:
            return user["nivel_acesso"]
    
    return None

def main():
    # Verificar se o usuário está autenticado (logado)
    if 'usuario_autenticado' not in st.session_state:
        st.session_state.usuario_autenticado = False

    # Verificar se o usuário está autenticado e qual é o seu nível de acesso
    nivel_acesso = None
    if st.session_state.usuario_autenticado:
        nivel_acesso = st.session_state.nivel_acesso

    if not nivel_acesso:
        # Escolher entre login ou registro
        opcao = st.radio("Escolha uma opção:", ("Login", "Registro"))

        if opcao == "Login":
            # Página de login
            st.title("Página de Login")
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")

            if st.button("Login"):
                nivel_acesso = verificar_acesso(usuario, senha)

                if nivel_acesso:
                    st.session_state.usuario_autenticado = True
                    st.session_state.nivel_acesso = nivel_acesso
                    st.success("Login bem-sucedido!")
                    st.experimental_rerun()  # Rerun para redirecionar para a página1
                else:
                    st.error("Nome de usuário ou senha incorretos. Tente novamente.")
        else:
            # Página de registro
            st.title("Página de Registro")
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            senha_verificacao = st.text_input("Insira a senha novamente", type="password")
            nivel_acesso = st.selectbox("Nível de Acesso", ["administrador", "operador"])

            if st.button("Registrar"):
                if senha == senha_verificacao:
                    novo_usuario = {
                        "usuario": usuario,
                        "senha": senha,
                        "nivel_acesso": nivel_acesso
                    }

                    # Carregar os usuários existentes
                    usuarios = carregar_usuarios()

                    # Adicionar o novo usuário à lista de usuários
                    usuarios.append(novo_usuario)

                    # Salvar a lista atualizada de usuários no arquivo JSON
                    salvar_usuarios(usuarios)

                    st.success("Registro bem-sucedido! Agora você pode fazer login.")
                else:
                    st.error("As senhas não coincidem. Tente novamente.")
    else:
        # Página1 após o login bem-sucedido
        st.title("Página 1")
        st.write("Bem-vindo à Página 1!")

        # Exibir conteúdo com base no nível de acesso do usuário
        if nivel_acesso == "administrador":
            st.write("Você é um administrador e tem acesso a todos os dados.")
            # Aqui você pode adicionar o conteúdo específico para o administrador.
        elif nivel_acesso == "operador":
            st.write("Você é um operador e tem acesso somente aos dados associados ao seu nome.")
            # Aqui você pode adicionar o conteúdo específico para o operador.

        # Botão de logout
        if st.button("Logout"):
            st.session_state.usuario_autenticado = False
            st.experimental_rerun()  # Rerun para voltar à página de login

if __name__ == "__main__":
    main()