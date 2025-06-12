"""
Trigger manual milestone check for Cyprian
"""
import discord
from discord.ext import commands
import asyncio
from time_tracker import TimeTracker

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
time_tracker = TimeTracker()

async def manual_milestone_check():
    """Trigger manual milestone check for Cyprian"""
    print("🔍 Verificando milestone manual para Cyprian...")
    
    cyprian_id = 1366547765810692156
    cyprian_name = "Cyprian."
    
    # Importar la función de milestone del bot principal
    from bot import check_time_milestone
    
    try:
        await check_time_milestone(cyprian_id, cyprian_name)
        print("✅ Verificación de milestone completada")
    except Exception as e:
        print(f"❌ Error en verificación de milestone: {e}")

@bot.event
async def on_ready():
    print(f'🤖 Bot conectado como {bot.user}')
    print(f'🔍 Ejecutando verificación manual de milestone...')
    
    await manual_milestone_check()
    
    print("✅ Verificación completada. Cerrando bot...")
    await bot.close()

if __name__ == "__main__":
    import os
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ Token no encontrado")