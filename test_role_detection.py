#!/usr/bin/env python3
"""
Test script to debug role detection for specific user
"""
import discord
import json
import os
from discord.ext import commands

# Cargar token desde variables de entorno
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

# ID del usuario específico a probar
CYPRIAN_USER_ID = 1366547765810692156

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def has_unlimited_time_role(member: discord.Member) -> bool:
    """Verificar si el usuario tiene el rol de tiempo ilimitado"""
    if UNLIMITED_TIME_ROLE_ID is None:
        return False
    
    for role in member.roles:
        if role.id == UNLIMITED_TIME_ROLE_ID:
            return True
    return False

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    
    # Buscar el usuario específico
    guild = bot.guilds[0] if bot.guilds else None
    if not guild:
        print("❌ No se encontró ningún servidor")
        return
    
    print(f"🏠 Servidor: {guild.name} (ID: {guild.id})")
    
    # Obtener información del usuario
    member = guild.get_member(CYPRIAN_USER_ID)
    if not member:
        print(f"❌ No se pudo encontrar al usuario con ID {CYPRIAN_USER_ID}")
        return
    
    print(f"👤 Usuario encontrado: {member.display_name} ({member.name})")
    print(f"📋 Roles del usuario:")
    
    for role in member.roles:
        is_target = "(⭐ ROL OBJETIVO)" if role.id == UNLIMITED_TIME_ROLE_ID else ""
        print(f"   - {role.name} (ID: {role.id}) {is_target}")
    
    # Verificar la función de detección
    has_special_role = has_unlimited_time_role(member)
    print(f"🔍 ¿Tiene rol especial? {has_special_role}")
    
    # Información adicional
    print(f"🎯 Buscando rol con ID: {UNLIMITED_TIME_ROLE_ID}")
    role_ids = [role.id for role in member.roles]
    print(f"📝 IDs de roles del usuario: {role_ids}")
    
    if UNLIMITED_TIME_ROLE_ID in role_ids:
        print("✅ El rol especial SÍ está en la lista de roles del usuario")
    else:
        print("❌ El rol especial NO está en la lista de roles del usuario")
    
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ No se encontró el token del bot")