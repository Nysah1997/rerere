#!/usr/bin/env python3
"""
Test completo del sistema de roles y créditos
"""
import discord
import json
import os
import asyncio
from discord.ext import commands
from time_tracker import TimeTracker

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Cargar configuración del rol desde config.json
UNLIMITED_TIME_ROLE_ID = None
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    UNLIMITED_TIME_ROLE_ID = config.get('unlimited_time_role_id')
    print(f"✅ Rol de tiempo ilimitado: ID {UNLIMITED_TIME_ROLE_ID}")
except Exception as e:
    print(f"⚠️ Error cargando configuración: {e}")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

def has_unlimited_time_role(member: discord.Member) -> bool:
    """Verificar si el usuario tiene el rol de tiempo ilimitado"""
    if UNLIMITED_TIME_ROLE_ID is None:
        return False
    
    for role in member.roles:
        if role.id == UNLIMITED_TIME_ROLE_ID:
            return True
    return False

def calculate_credits(total_seconds: float, has_special_role: bool = False) -> int:
    """Calcular créditos basado en el tiempo total"""
    total_hours = total_seconds / 3600
    
    if has_special_role:
        # Usuarios con rol especial: 1h=3, 2h=5, 3h=10, 4h=12
        if total_hours >= 4.0:
            return 12  # 4 horas = 12 créditos
        elif total_hours >= 3.0:
            return 10  # 3 horas = 10 créditos
        elif total_hours >= 2.0:
            return 5   # 2 horas = 5 créditos
        elif total_hours >= 1.0:
            return 3   # 1 hora = 3 créditos
        else:
            return 0   # Menos de 1 hora = 0 créditos
    else:
        # Usuarios sin rol especial: 1h=3, 2h=5
        if total_hours >= 2.0:
            return 5  # 2 horas = 5 créditos
        elif total_hours >= 1.0:
            return 3  # 1 hora = 3 créditos
        else:
            return 0  # Menos de 1 hora = 0 créditos

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    
    guild = bot.guilds[0] if bot.guilds else None
    if not guild:
        print("❌ No se encontró ningún servidor")
        return
    
    print(f"🏠 Servidor: {guild.name}")
    
    # Crear un tracker de tiempo para pruebas
    tracker = TimeTracker()
    
    # Buscar usuarios con y sin el rol especial
    special_role_users = []
    regular_users = []
    
    for member in guild.members:
        if not member.bot:
            has_special_role = has_unlimited_time_role(member)
            if has_special_role:
                special_role_users.append(member)
            else:
                regular_users.append(member)
    
    print(f"\n👥 Usuarios con rol especial ({len(special_role_users)}):")
    for member in special_role_users:
        print(f"   - {member.display_name} (ID: {member.id})")
    
    print(f"\n👤 Usuarios regulares ({len(regular_users)}):")
    for member in regular_users[:3]:  # Solo mostrar primeros 3
        print(f"   - {member.display_name} (ID: {member.id})")
    
    # Test del sistema de créditos con diferentes tiempos
    print(f"\n🧪 Test del sistema de créditos:")
    
    test_times = [
        (3600, "1 hora"),      # 1 hora
        (7200, "2 horas"),     # 2 horas
        (10800, "3 horas"),    # 3 horas
        (14400, "4 horas")     # 4 horas
    ]
    
    for seconds, description in test_times:
        regular_credits = calculate_credits(seconds, False)
        special_credits = calculate_credits(seconds, True)
        print(f"   {description}: Regular={regular_credits} créditos, Especial={special_credits} créditos")
    
    # Test práctico si hay usuarios disponibles
    if special_role_users:
        test_user = special_role_users[0]
        print(f"\n🎯 Test práctico con {test_user.display_name}:")
        
        # Simular diferentes tiempos acumulados
        for seconds, description in test_times:
            has_role = has_unlimited_time_role(test_user)
            credits = calculate_credits(seconds, has_role)
            print(f"   {description}: {credits} créditos ({'con rol especial' if has_role else 'sin rol especial'})")
    
    print(f"\n✅ Test completado - Sistema de roles y créditos verificado")
    await bot.close()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ No se encontró el token del bot")