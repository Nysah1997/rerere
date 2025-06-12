#!/usr/bin/env python3
"""
Test para verificar que el comando reiniciar_todos_tiempos funciona correctamente
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

async def test_reset_all():
    """Test del comando reiniciar todos los tiempos"""
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if not channel:
        print("Canal no encontrado")
        return
    
    await channel.send("🧪 Iniciando test de reinicio masivo...")
    
    # Crear varios usuarios de prueba con tiempo
    test_users = [
        (444555666, "Usuario1", 25),
        (777888999, "Usuario2", 45), 
        (111333555, "Usuario3", 15)
    ]
    
    # Agregar usuarios con tiempo
    for user_id, user_name, seconds in test_users:
        time_tracker.start_tracking(user_id, user_name)
        time_tracker.data[str(user_id)]['total_seconds'] = seconds
        time_tracker.data[str(user_id)]['notified_10_seconds'] = True  # Simular que ya fueron notificados
        time_tracker.save_data()
        print(f"Usuario {user_name} creado con {seconds} segundos")
    
    # Mostrar estado antes del reinicio
    await channel.send(f"Usuarios creados: {len(test_users)}")
    
    tracked_before = time_tracker.get_all_tracked_users()
    total_before = sum(data['total_seconds'] for data in tracked_before.values())
    await channel.send(f"Tiempo total antes del reinicio: {total_before} segundos")
    
    # Ejecutar reinicio masivo
    usuarios_reiniciados = time_tracker.reset_all_user_times()
    print(f"Usuarios reiniciados: {usuarios_reiniciados}")
    
    await channel.send(f"🔄 Reiniciados {usuarios_reiniciados} usuarios")
    
    # Verificar estado después del reinicio
    tracked_after = time_tracker.get_all_tracked_users()
    total_after = sum(data['total_seconds'] for data in tracked_after.values())
    notifications_reset = sum(1 for data in tracked_after.values() if not data.get('notified_10_seconds', False))
    
    await channel.send(f"Tiempo total después del reinicio: {total_after} segundos")
    await channel.send(f"Notificaciones reiniciadas: {notifications_reset}/{len(tracked_after)}")
    
    # Verificar que todos los tiempos son 0
    all_zero = all(data['total_seconds'] == 0 for data in tracked_after.values())
    all_inactive = all(not data['is_active'] for data in tracked_after.values())
    
    if all_zero and all_inactive:
        await channel.send("✅ Test exitoso: Todos los tiempos reiniciados correctamente")
    else:
        await channel.send("❌ Test fallido: Algunos tiempos no se reiniciaron")
    
    # Limpiar datos de prueba
    for user_id, _, _ in test_users:
        time_tracker.cancel_user_tracking(user_id)
    
    await channel.send("🧹 Datos de prueba limpiados")

@bot.event
async def on_ready():
    print(f'Test reset-all conectado: {bot.user}')
    await test_reset_all()
    await bot.close()

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("Token no encontrado")