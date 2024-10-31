import os
import pathlib
import smtplib
from string import Template
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string

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

# Função para gerar um código aleatório
def gerar_codigo_aleatorio(tamanho=5):
    return ''.join(random.choices(string.digits, k=tamanho))

# Função para enviar o e-mail de recuperação
def enviar_email_recuperacao(destinatario, email):
    codigo_aleatorio = gerar_codigo_aleatorio()
    link_redefinicao = f"http://localhost:5000/redefinir-senha?email={email}&codigo={codigo_aleatorio}"

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

    # Cria a estrutura do e-mail 
    mime_multipart = MIMEMultipart()
    mime_multipart['From'] = remetente
    mime_multipart['To'] = destinatario
    mime_multipart['Subject'] = 'Recuperação de Senha'

    # Anexa o corpo HTML ao e-mail
    corpo_email = MIMEText(texto_email, 'html', 'utf-8')
    mime_multipart.attach(corpo_email)

    # Envia o e-mail usando o servidor SMTP do Gmail
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()  # Inicia a comunicação criptografada
            server.login(smtp_user, smtp_password)  # Faz o login
            server.sendmail(remetente, destinatario, mime_multipart.as_string())  # Envia o e-mail
            print(f'E-mail enviado para {destinatario}')
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
