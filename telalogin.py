import streamlit as st
import json
import datetime

class LoginApp:
    def __init__(self):
        self.usuarios = self.carregar_usuarios()

    @staticmethod
    def carregar_usuarios():
        try:
            with open('usuarios.json', 'r') as arquivo:
                usuarios = json.load(arquivo)
            return usuarios['usuarios']
        except FileNotFoundError:
            st.error("Arquivo de usuários não encontrado.")
            return []

    def autenticar_usuario(self, usuario, senha):
        for user in self.usuarios:
            if user["usuario"] == usuario and user["senha"] == senha:
                return user["nivel"]
        return None

    def obter_dados_usuario_por_nome(self, nome):
        for user in self.usuarios:
            if user["nome"] == nome:
                return user
        return None

    @staticmethod
    def salvar_ultimo_login(usuario, usuarios):
        for user in usuarios:
            if user["usuario"] == usuario:
                user["ultimo_login"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def admin_page(self, usuario):
        st.header(f"Bem-vindo(a), {usuario}!")
        
        # Obter dados do usuário logado
        dados_usuario = self.obter_dados_usuario_por_nome(usuario)
        if dados_usuario is not None and "ultimo_login" in dados_usuario:
            st.write(f"Seu último login foi em: {dados_usuario['ultimo_login']}")
        
        st.sidebar.button('Novo usuário')
        if st.sidebar.button('Logout'):
            st.experimental_set_query_params(logout='true')  # Adicionar parâmetro 'logout' na URL
            st.experimental_rerun()  # Recarregar a página para exibir o login novamente

    def run(self):
        st.title('Tela de Login')

        usuario = st.text_input('Usuário')
        senha = st.text_input('Senha', type='password')

        if st.button('Entrar'):
            nivel_acesso = self.autenticar_usuario(usuario, senha)

            if nivel_acesso == "administrador":
                st.experimental_set_query_params(admin='true')  # Adicionar parâmetro 'admin' na URL
                st.session_state["usuario"] = usuario  # Armazenar o usuário autenticado na sessão
                st.experimental_rerun()  # Recarregar a página para exibir a página do administrador
            elif nivel_acesso == "operador":
                st.error('Acesso permitido somente para administradores.')
            else:
                st.error('Usuário ou senha incorretos.')
        
        # Verificar se o parâmetro 'admin' está na URL para redirecionar para a página do administrador
        if 'admin' in st.experimental_get_query_params():
            usuario = st.session_state.get("usuario", None)  # Obter o usuário autenticado da sessão
            if usuario:
                self.admin_page(usuario)

        # Verificar se o parâmetro 'logout' está na URL para redirecionar para a página de login
        if 'logout' in st.experimental_get_query_params():
            st.experimental_set_query_params()  # Limpar parâmetros da URL
            st.experimental_rerun()  # Recarregar a página para exibir a página de login novamente
        

if __name__ == '__main__':
    login_app = LoginApp()
    login_app.run()
