#!/usr/bin/env python3
"""
Script simple para probar las notificaciones manualmente
"""

import asyncio
import discord
import os
from time_tracker import TimeTracker

# Configuración del bot de prueba
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = discord.Client(intents=intents)
time_tracker = TimeTracker()
NOTIFICATION_CHANNEL_ID = 1382057005870747808

@bot.event
async def on_ready():
    print(f'Bot de prueba conectado como {bot.user}')
    
    # Buscar el canal
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if channel:
        print(f'Canal encontrado: {channel.name if hasattr(channel, "name") else "Sin nombre"}')
        try:
            await channel.send("🧪 Test de notificaciones - Bot conectado")
            print("Mensaje de prueba enviado exitosamente")
        except Exception as e:
            print(f"Error enviando mensaje de prueba: {e}")
    else:
        print(f'Canal no encontrado con ID: {NOTIFICATION_CHANNEL_ID}')
    
    # Simular notificación de 10 segundos
    await asyncio.sleep(2)
    
    # Crear usuario de prueba
    test_user_id = 123456789
    test_user_name = "UsuarioPrueba"
    
    # Agregar exactamente 11 segundos para superar el límite
    time_tracker.start_tracking(test_user_id, test_user_name)
    time_tracker.data[str(test_user_id)]['total_seconds'] = 11
    time_tracker.save_data()
    
    total_time = time_tracker.get_total_time(test_user_id)
    print(f"Tiempo del usuario de prueba: {total_time} segundos")
    
    if total_time >= 10 and not time_tracker.has_notified_10_seconds(test_user_id):
        print("Enviando notificación de prueba...")
        time_tracker.mark_10_seconds_notified(test_user_id)
        
        if channel:
            try:
                await channel.send(f"🎉 {test_user_name} ha completado 10 segundos de tiempo! (PRUEBA)")
                print("Notificación de prueba enviada exitosamente")
            except Exception as e:
                print(f"Error enviando notificación de prueba: {e}")
    
    # Limpiar datos de prueba
    time_tracker.cancel_user_tracking(test_user_id)
    
    await bot.close()

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("Token no encontrado")