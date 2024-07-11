from supabase_py import create_client, Client
import os
from dotenv import load_dotenv
from models.usuario import Usuario

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class SupabaseClient:
    def __init__(self, url: str, api_key: str):
        self.client: Client = create_client(url, api_key)
    
    def registrar_usuario(self, usuario: Usuario):
        # Registrar o usuário no sistema de autenticação
        response = self.client.auth.sign_up(email=usuario.email, password=usuario.senha)
        if response.get("error"):
            return response

        # Adicionar informações adicionais do usuário
        data = {
            "email": usuario.email,
            "nome": usuario.nome,
            "sexo": usuario.sexo,
            "idade": usuario.idade,
            "peso": usuario.peso,
            "altura": usuario.altura
        }
        response = self.client.from_("usuarios").insert(data).execute()
        return response

    def autenticar_usuario(self, email: str, senha: str):
        response = self.client.auth.sign_in(email=email, password=senha)
        return response
    
    def autenticar_google(self, access_token: str):
        response = self.client.auth.sign_in(provider="google", access_token=access_token)
        return response

# Configuração da URL e API Key do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)
