import streamlit as st
import json

def login():
    st.title("Página de Login")

    # Lendo os dados dos usuários do arquivo usuarios.json
    with open('usuarios.json', 'r') as file:
        data = json.load(file)
        usuarios = data["usuarios"]

    page = st.empty()

    if not page.button("Cadastrar Novo Usuário"):
        with page.form("login_form"):
            username = st.text_input("Usuário (Matrícula)")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar")

            if submitted:
                for user in usuarios:
                    if user["usuario"] == username and user["senha"] == password:
                        if user["nivel"] == "administrador":
                            st.success("Login bem-sucedido como Administrador")
                            st.write(f"Bem-vindo, {user['nome']}!")
                            page.button("Logout")
                        elif user["nivel"] == "operador":
                            st.success("Login bem-sucedido como Operador")
                            st.write(f"Bem-vindo, {user['nome']}!")
                            page.button("Logout")
                        break
                else:
                    st.error("Usuário ou senha incorretos")
    else:
        show_cadastro_form()

def show_cadastro_form():
    st.title("Cadastro de Novo Usuário")
    nome = st.text_input("Nome Completo")
    matricula = st.text_input("Matrícula")
    nivel = st.selectbox("Nível de Acesso", ["administrador", "operador"])
    senha = "123456"  # Geração automática de senha (mínimo 6 dígitos)
    email = st.text_input("E-mail")
    
    with st.form("cadastro_form"):
        st.write("Confira os dados abaixo antes de cadastrar:")
        st.write(f"Nome: {nome}")
        st.write(f"Matrícula: {matricula}")
        st.write(f"Nível de Acesso: {nivel}")
        st.write(f"E-mail: {email}")
        submitted = st.form_submit_button("Cadastrar")

        if submitted:
            # Lendo os dados existentes do arquivo usuarios.json
            with open('usuarios.json', 'r') as file:
                data = json.load(file)
                usuarios = data["usuarios"]

            # Verificando se a matrícula já existe
            for user in usuarios:
                if user["matricula"] == matricula:
                    st.error("Matrícula já cadastrada")
                    return

            # Criando um novo usuário
            novo_usuario = {
                "nome": nome,
                "usuario": matricula,
                "senha": senha,
                "email": email,
                "matricula": matricula,
                "nivel": nivel
            }

            # Adicionando o novo usuário à lista de usuários
            usuarios.append(novo_usuario)

            # Salvando os dados atualizados no arquivo usuarios.json
            with open('usuarios.json', 'w') as file:
                json.dump(data, file, indent=4)

            st.success("Usuário cadastrado com sucesso!")

if __name__ == "__main__":
    login()
