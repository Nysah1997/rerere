#!/usr/bin/env python3
"""
Script to list all members in the Discord server to identify correct user IDs
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
    print(f"✅ Rol de tiempo ilimitado cargado desde config: ID {UNLIMITED_TIME_ROLE_ID}")
except Exception as e:
    print(f"⚠️ No se pudo cargar configuración del rol: {e}")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Enable member intent to get all members
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    
    guild = bot.guilds[0] if bot.guilds else None
    if not guild:
        print("❌ No se encontró ningún servidor")
        return
    
    print(f"🏠 Servidor: {guild.name} (ID: {guild.id})")
    print(f"👥 Total de miembros: {guild.member_count}")
    print("\n📋 Lista de miembros:")
    
    for member in guild.members:
        if not member.bot:  # Solo usuarios humanos
            has_special_role = False
            special_roles = []
            
            for role in member.roles:
                if role.id == UNLIMITED_TIME_ROLE_ID:
                    has_special_role = True
                    special_roles.append(f"{role.name} (ID: {role.id})")
            
            role_indicator = "⭐ TIENE ROL ESPECIAL" if has_special_role else "⚪ Usuario regular"
            print(f"   - {member.display_name} (@{member.name}) - ID: {member.id} - {role_indicator}")
            
            if special_roles:
                print(f"     Roles especiales: {', '.join(special_roles)}")
    
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ No se encontró el token del bot")