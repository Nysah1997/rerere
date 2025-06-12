#!/usr/bin/env python3
"""
Script to identify current server members and their roles
"""
import discord
import json
import os
from discord.ext import commands

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Cargar configuración del rol desde config.json
UNLIMITED_TIME_ROLE_ID = None
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    UNLIMITED_TIME_ROLE_ID = config.get('unlimited_time_role_id')
    print(f"Buscando rol especial con ID: {UNLIMITED_TIME_ROLE_ID}")
except Exception as e:
    print(f"Error cargando configuración: {e}")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    
    guild = bot.guilds[0] if bot.guilds else None
    if not guild:
        print("No se encontró ningún servidor")
        return
    
    print(f"Servidor: {guild.name} (ID: {guild.id})")
    print(f"Total de miembros: {guild.member_count}")
    
    # Obtener información detallada de cada miembro
    print("\nMiembros del servidor:")
    special_role_count = 0
    
    for member in guild.members:
        if not member.bot:  # Solo usuarios humanos
            has_special_role = False
            role_names = []
            
            for role in member.roles:
                if role.name != "@everyone":
                    role_names.append(f"{role.name} (ID: {role.id})")
                if role.id == UNLIMITED_TIME_ROLE_ID:
                    has_special_role = True
            
            status = "⭐ TIENE ROL ESPECIAL" if has_special_role else "Usuario regular"
            if has_special_role:
                special_role_count += 1
            
            print(f"\n👤 {member.display_name} (@{member.name})")
            print(f"   ID: {member.id}")
            print(f"   Estado: {status}")
            if role_names:
                print(f"   Roles: {', '.join(role_names)}")
    
    print(f"\n📊 Resumen:")
    print(f"   - Usuarios con rol especial: {special_role_count}")
    print(f"   - Rol especial buscado: ID {UNLIMITED_TIME_ROLE_ID}")
    
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("No se encontró el token del bot")