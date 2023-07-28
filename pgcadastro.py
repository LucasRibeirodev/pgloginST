import streamlit as st
import random
import string
import json

class CadastroUsuarios:
    def __init__(self):
        self.niveis = ['administrador', 'supervisor', 'operador']

    def gerar_senha_aleatoria(self):
        caracteres = string.ascii_letters + string.digits
        senha = ''.join(random.choice(caracteres) for i in range(6))
        return senha

    def salvar_usuario(self, usuario_data):
        try:
            with open('usuarios.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"usuarios": []}

        data["usuarios"].append(usuario_data)

        with open('usuarios.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def cadastrar_usuario(self):
        st.title('Cadastro de Usuários')

        # Formulário para cadastro de usuários
        nome = st.text_input('Nome completo do usuário')
        usuario = st.text_input('Usuário (Matrícula)')
        senha = st.text_input('Senha', value=self.gerar_senha_aleatoria(), type='password')
        email = st.text_input('Email')
        matricula = st.number_input('Matrícula', step=1)
        nivel = st.selectbox('Nível', self.niveis)

        # Botão para enviar o formulário
        enviar = st.button('Cadastrar')

        # Verificação dos campos preenchidos e salvamento no arquivo JSON
        if enviar:
            if nome and usuario and senha and email and matricula and nivel:
                usuario_data = {
                    'nome': nome,
                    'usuario': usuario,
                    'senha': senha,
                    'email': email,
                    'matricula': str(matricula),
                    'nivel': nivel
                }
                self.salvar_usuario(usuario_data)
                st.success('Usuário cadastrado com sucesso!')
            else:
                st.warning('Por favor, preencha todos os campos obrigatórios.')

# Criar uma instância da classe e chamar a função cadastrar_usuario()
cadastro = CadastroUsuarios()
cadastro.cadastrar_usuario()
