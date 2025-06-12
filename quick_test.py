#!/usr/bin/env python3
"""
Test rápido de notificaciones usando el sistema del bot
"""

import asyncio
import discord
import os
from time_tracker import TimeTracker

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = discord.Client(intents=intents)
time_tracker = TimeTracker()
NOTIFICATION_CHANNEL_ID = 1382057005870747808

async def test_notification_system():
    """Test directo del sistema de notificaciones"""
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if not channel:
        print("Canal no encontrado")
        return
    
    # Crear usuario de prueba
    test_user_id = 555666777
    test_user_name = "PruebaRapida"
    
    # Limpiar datos previos
    time_tracker.cancel_user_tracking(test_user_id)
    
    # Agregar exactamente 11 segundos para superar el límite
    time_tracker.add_minutes(test_user_id, test_user_name, 0)
    time_tracker.data[str(test_user_id)]['total_seconds'] = 11
    time_tracker.save_data()
    
    total_time = time_tracker.get_total_time(test_user_id)
    print(f"Tiempo configurado: {total_time} segundos")
    print(f"¿Ya notificado? {time_tracker.has_notified_10_seconds(test_user_id)}")
    
    # Verificar milestone
    if total_time >= 10 and not time_tracker.has_notified_10_seconds(test_user_id):
        print("Enviando notificación...")
        time_tracker.mark_10_seconds_notified(test_user_id)
        
        try:
            await channel.send(f"🎉 {test_user_name} ha completado 10 segundos de tiempo! (TEST RÁPIDO)")
            print("✅ Notificación enviada correctamente")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("No se envió notificación")
    
    # Limpiar
    time_tracker.cancel_user_tracking(test_user_id)

@bot.event
async def on_ready():
    print(f'Test bot conectado: {bot.user}')
    await test_notification_system()
    await bot.close()

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("Token no encontrado")