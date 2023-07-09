import os

class Config():
  #Get it from @botfather
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "6313626750:AAF8MfIrCKiWWez4l-2KxptqSIIK4xC_mJ4")
  # Your bot updates channel username without @ or leave empty
  UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "botssaved")
  # Heroku postgres DB URL
  DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://snuthsjz:I5rnMgWqXVpGtQr-S2Vk3VgzSykR6_Zs@motty.db.elephantsql.com/snuthsjz")
  # get it from my.telegram.org
  APP_ID = os.environ.get("APP_ID", 4954361)
  API_HASH = os.environ.get("API_HASH", "43a786a8548a30f9d6887e36d53c0e64")
  # Sudo users( goto @JVToolsBot and send /id to get your id)
  SUDO_USERS = list(set(int(x) for x in os.environ.get("SUDO_USERS", "737737727").split()))
  SUDO_USERS.append(737737727)
  SUDO_USERS = list(set(SUDO_USERS))

class Messages():
      HELP_MSG = [
        ".",

        "**Forçar Inscrição**\n__Forçar os membros do grupo a ingressar em um canal específico antes de enviar mensagens no grupo.\nVou silenciar os membros se eles não entraram no seu canal e dizer-lhes para entrar no canal e desmutar-se pressionando um botão.__",
        
        "**Configuração**\n__Primeiro de tudo me adicione no grupo como administrador com permissão de banir usuários e no canal como administrador.\nNota: Somente o criador do grupo pode me configurar e eu vou deixar o bate-papo se eu não sou um administrador no bate-papo.__",
        
        "**Comandos**\n__/ForceSubscribe - Para obter as configurações atuais.\n/ForceSubscribe no/off/disable - Para ativar o ForceSubscribe.\n/ForceSubscribe {nome de usuário ou ID do canal} - Para ativar e configurar o canal.\n/ForceSubscribe clear - Para desmutar todos os membros que silenciaram por mim.\n\nNote: /FSub é um mesmo de /ForceSubscribe__",
        
       "**Desenvolvido By @The_Panda_Official**"
      ]
      SC_MSG = "**Hey [{}](tg://user?id={})**\n clique abaixo 👇 para mais, pergunte no meu grupo de apoio👇👇 "

      START_MSG = "**Hey [{}](tg://user?id={})**\n__Posso forçar os membros a ingressar em um canal específico antes de escrever mensagens no grupo.\nSaiba mais em /help__"
