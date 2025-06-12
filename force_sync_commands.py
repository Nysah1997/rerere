
#!/usr/bin/env python3
"""
Script para forzar la sincronización de comandos slash
"""
import discord
from discord.ext import commands
import json
import os

# Cargar configuración
with open('config.json', 'r') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 Bot conectado como {bot.user}')
    
    # Forzar sincronización de comandos
    try:
        synced = await bot.tree.sync()
        print(f'✅ Sincronizados {len(synced)} comandos slash')
        
        # Listar comandos sincronizados
        for cmd in synced:
            print(f'  - /{cmd.name}: {cmd.description}')
            
    except Exception as e:
        print(f'❌ Error sincronizando comandos: {e}')
    
    print('🔄 Sincronización completada. Cerrando bot...')
    await bot.close()

if __name__ == "__main__":
    token = config.get('discord_bot_token') or os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ No se encontró el token de Discord")
