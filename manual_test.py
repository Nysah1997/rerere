#!/usr/bin/env python3
"""
Test manual para simular el proceso completo de notificaciones
"""

import asyncio
import discord
import os
from time_tracker import TimeTracker

# Configuración
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = discord.Client(intents=intents)
time_tracker = TimeTracker()
NOTIFICATION_CHANNEL_ID = 1382057005870747808

@bot.event
async def on_ready():
    print(f'Bot de prueba manual conectado como {bot.user}')
    
    # Obtener canal
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if not channel:
        print(f'Error: Canal no encontrado con ID {NOTIFICATION_CHANNEL_ID}')
        await bot.close()
        return
    
    print(f'Canal encontrado: {channel.name if hasattr(channel, "name") else "Canal privado"}')
    
    # Enviar mensaje inicial
    await channel.send("🔧 Iniciando prueba manual de notificaciones...")
    
    # Simular usuario uniéndose a canal de voz
    test_user_id = 987654321
    test_user_name = "TestUser"
    
    print(f"Simulando: {test_user_name} se une a canal de voz")
    success = time_tracker.start_tracking(test_user_id, test_user_name)
    print(f"Seguimiento iniciado: {success}")
    
    # Esperar 12 segundos para superar el límite
    print("Esperando 12 segundos...")
    await asyncio.sleep(12)
    
    # Simular que el usuario sale del canal
    print(f"Simulando: {test_user_name} sale del canal de voz")
    success = time_tracker.pause_tracking(test_user_id)
    print(f"Seguimiento pausado: {success}")
    
    # Verificar tiempo total
    total_time = time_tracker.get_total_time(test_user_id)
    formatted_time = time_tracker.format_time_display(total_time)
    print(f"Tiempo total: {formatted_time} ({total_time} segundos)")
    
    # Verificar si debe notificar
    should_notify = total_time >= 10 and not time_tracker.has_notified_10_seconds(test_user_id)
    print(f"¿Debe notificar? {should_notify}")
    
    if should_notify:
        print("Enviando notificación...")
        time_tracker.mark_10_seconds_notified(test_user_id)
        await channel.send(f"🎉 {test_user_name} ha completado 10 segundos de tiempo! (Tiempo total: {formatted_time})")
        print("Notificación enviada")
    else:
        await channel.send(f"❌ No se envió notificación para {test_user_name}. Tiempo: {formatted_time}, Ya notificado: {time_tracker.has_notified_10_seconds(test_user_id)}")
    
    # Limpiar
    time_tracker.cancel_user_tracking(test_user_id)
    await channel.send("✅ Prueba completada y datos limpiados")
    
    print("Prueba manual completada")
    await bot.close()

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("Token no encontrado")