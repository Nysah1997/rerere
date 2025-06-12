#!/usr/bin/env python3
"""
Script para forzar sincronización de comandos slash
"""

import asyncio
import discord
import os
from discord.ext import commands

# Configuración
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado: {bot.user}')
    
    # Limpiar comandos globales primero
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
    print("Comandos globales limpiados")
    
    # Registrar comando de prueba
    @bot.tree.command(name="reiniciar_todos_tiempos", description="Reiniciar todos los tiempos de todos los usuarios")
    async def reiniciar_todos_tiempos(interaction: discord.Interaction):
        await interaction.response.send_message("🔄 Comando de reinicio masivo funcionando!")
    
    # Sincronizar nuevamente
    synced = await bot.tree.sync()
    print(f'Comandos sincronizados: {len(synced)}')
    
    # Listar comandos
    for cmd in bot.tree.get_commands():
        print(f'- {cmd.name}: {cmd.description}')
    
    print("Sincronización completada")
    await bot.close()

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("Token no encontrado")