#!/usr/bin/env python3
"""
Test para verificar que el seguimiento se detiene automáticamente a los 10 segundos
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

async def test_auto_stop():
    """Test del sistema de parada automática"""
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if not channel:
        print("Canal no encontrado")
        return
    
    # Crear usuario de prueba
    test_user_id = 111222333
    test_user_name = "AutoStopTest"
    
    # Limpiar datos previos
    time_tracker.cancel_user_tracking(test_user_id)
    
    await channel.send("🧪 Iniciando test de parada automática...")
    
    # Iniciar seguimiento
    time_tracker.start_tracking(test_user_id, test_user_name)
    print(f"Seguimiento iniciado para {test_user_name}")
    print(f"Estado inicial - Activo: {time_tracker.data[str(test_user_id)]['is_active']}")
    
    # Simular 11 segundos
    time_tracker.data[str(test_user_id)]['total_seconds'] = 11
    time_tracker.save_data()
    
    total_time = time_tracker.get_total_time(test_user_id)
    print(f"Tiempo configurado: {total_time} segundos")
    
    # Simular la verificación de milestone
    if total_time >= 10 and not time_tracker.has_notified_10_seconds(test_user_id):
        print("Activando sistema de milestone...")
        time_tracker.mark_10_seconds_notified(test_user_id)
        
        # Detener seguimiento automáticamente
        time_tracker.stop_tracking(test_user_id)
        print("Seguimiento detenido automáticamente")
        
        formatted_time = time_tracker.format_time_display(total_time)
        message = f"🎉 {test_user_name} ha completado 10 segundos! Tiempo final: {formatted_time} - Seguimiento detenido automáticamente."
        
        await channel.send(message)
        print("Notificación enviada")
        
        # Verificar estado final
        user_data = time_tracker.get_user_data(test_user_id)
        if user_data:
            print(f"Estado final - Activo: {user_data['is_active']}")
            print(f"Estado final - Pausado: {user_data['is_paused']}")
            await channel.send(f"Estado final: Activo={user_data['is_active']}, Pausado={user_data['is_paused']}")
        else:
            print("Usuario no encontrado después de la prueba")
    
    # Limpiar
    time_tracker.cancel_user_tracking(test_user_id)
    await channel.send("✅ Test completado y datos limpiados")

@bot.event
async def on_ready():
    print(f'Test auto-stop conectado: {bot.user}')
    await test_auto_stop()
    await bot.close()

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("Token no encontrado")