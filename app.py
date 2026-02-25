import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = os.environ.get('REPO_OWNER')
REPO_NAME = os.environ.get('REPO_NAME')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='¡Hola! Envía /list, /add, o /remove para controlar el parental control de tu router.')

def handle_message(update, context):
    command = update.message.text.lower().strip()
    
    action_map = {
        '/list': 'list',
        '/add': 'add', 
        '/remove': 'remove',
        'list': 'list',
        'add': 'add',
        'remove': 'remove',
        'bloquear': 'add',
        'permitir': 'remove',
        'mostrar': 'list'
    }
    
    action = action_map.get(command)
    
    if action:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Ejecutando acción: {action}...')
        
        url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/parental-control.yml/dispatch'
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github+json'
        }
        data = {'ref': 'main', 'inputs': {'action': action}}
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 204:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'✅ Acción {action} iniciada.')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'❌ Error: {response.status_code}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Comandos válidos: /list, /add, /remove')

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    
    print('Bot iniciado...')
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
