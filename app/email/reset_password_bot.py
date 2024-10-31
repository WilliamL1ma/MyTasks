import os
import pathlib
import smtplib
from string import Template
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
from cryptography.fernet import Fernet

# Carrega as variáveis do arquivo .env
load_dotenv()

# Caminho para o arquivo HTML
CAMINHO_HTML = pathlib.Path(__file__).parent / 'email_password.html'

# Variáveis de e-mail
remetente = os.getenv('FROM_EMAIL', '')
smtp_user = os.getenv('FROM_EMAIL', '')
smtp_password = os.getenv('EMAIL_PASSWORD', '')

# Servidor SMTP do Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Caminho para o arquivo da chave
key_file_path = pathlib.Path(__file__).parent.parent / 'data' / 'secret.key'

# Carregar a chave para Fernet
with open(key_file_path, 'rb') as key_file:
    key = key_file.read()
fernet = Fernet(key)

# Função para gerar um código aleatório
def gerar_codigo_aleatorio(tamanho=10):
    caracteres = string.ascii_letters + string.digits  # Letras e números
    return ''.join(random.choices(caracteres, k=tamanho))

# Função para criptografar o link de redefinição
def criptografar_link(link):
    return fernet.encrypt(link.encode()).decode()

def enviar_email_recuperacao(destinatario, email):
    codigo_aleatorio = gerar_codigo_aleatorio()
    
    # Crie uma string com os parâmetros
    parametros = f"email={email}&codigo={codigo_aleatorio}"
    
    # Criptografar apenas os parâmetros
    parametros_criptografados = criptografar_link(parametros)

    # Montar o link de redefinição
    link_redefinicao = f"http://localhost:5000/redefinir-senha?dados={parametros_criptografados}"
    
    # Verifica se as credenciais foram carregadas corretamente
    if not smtp_user or not smtp_password:
        raise ValueError("Credenciais de e-mail não foram carregadas corretamente. Verifique o arquivo .env")
    
    # Lê o arquivo HTML e prepara o corpo do e-mail
    try:
        with open(CAMINHO_HTML, 'r', encoding='utf-8') as arquivo:
            texto_arquivo = arquivo.read()
            template = Template(texto_arquivo)
            texto_email = template.substitute(link_redefinicao=link_redefinicao)
    except FileNotFoundError:
        print("Arquivo HTML não encontrado. Verifique o caminho e o nome do arquivo.")
        return

    # Criação do e-mail
    mime_multipart = MIMEMultipart()
    mime_multipart['From'] = remetente
    mime_multipart['To'] = destinatario
    mime_multipart['Subject'] = 'Recuperação de Senha'

    # Anexa o corpo HTML ao e-mail
    corpo_email = MIMEText(texto_email, 'html', 'utf-8')
    mime_multipart.attach(corpo_email)

    # Envio do e-mail
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()  # Inicia a comunicação criptografada
            server.login(smtp_user, smtp_password)  # Faz o login
            server.sendmail(remetente, destinatario, mime_multipart.as_string())  # Envia o e-mail
            print(f'E-mail enviado para {destinatario}')
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

