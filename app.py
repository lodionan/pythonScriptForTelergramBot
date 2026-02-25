import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = os.environ.get('REPO_OWNER')
REPO_NAME = os.environ.get('REPO_NAME')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('¡Hola! Envía /list, /add, o /remove para controlar el parental control de tu router.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.lower().strip()
    
    # Mapear comandos
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
        await update.message.reply_text(f'Ejecutando acción: {action}...')
        
        # Llamar a GitHub API
        url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/parental-control.yml/dispatch'
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github+json'
        }
        data = {'ref': 'main', 'inputs': {'action': action}}
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 204:
            await update.message.reply_text(f'✅ Acción {action} iniciada. Revisa el resultado en GitHub Actions.')
        else:
            await update.message.reply_text(f'❌ Error: {response.status_code}')
    else:
        await update.message.reply_text('Comandos válidos: /list, /add, /remove')

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print('Bot iniciado...')
    asyncio.run(app.run_polling())

if __name__ == '__main__':
    main()