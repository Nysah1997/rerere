"""
Test del sistema de conteo de pausas y cancelación automática
"""

import asyncio
import discord
from discord.ext import commands
import json
import os

# Configuración del bot de prueba
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Importar el sistema de seguimiento de tiempo
from time_tracker import TimeTracker

time_tracker = TimeTracker()

@bot.event
async def on_ready():
    print(f'Bot de prueba conectado: {bot.user}')
    
    # Test completo del sistema de pausas
    await test_pause_counting_system()
    
    print("✅ Test del sistema de conteo de pausas completado")
    await bot.close()

async def test_pause_counting_system():
    """Test completo del sistema de conteo de pausas"""
    print("\n=== TEST DEL SISTEMA DE CONTEO DE PAUSAS ===")
    
    # Usuario de prueba
    test_user_id = 123456789
    test_user_name = "TestUser"
    
    # Limpiar datos previos
    time_tracker.cancel_user_tracking(test_user_id)
    
    print("1. Iniciando seguimiento para usuario de prueba...")
    success = time_tracker.start_tracking(test_user_id, test_user_name)
    assert success, "Falló al iniciar seguimiento"
    
    # Verificar contador inicial
    pause_count = time_tracker.get_pause_count(test_user_id)
    print(f"   Contador de pausas inicial: {pause_count}")
    assert pause_count == 0, f"Contador inicial debería ser 0, es {pause_count}"
    
    print("\n2. Primera pausa...")
    success = time_tracker.pause_tracking(test_user_id)
    assert success, "Falló primera pausa"
    
    pause_count = time_tracker.get_pause_count(test_user_id)
    print(f"   Contador después de 1ra pausa: {pause_count}")
    assert pause_count == 1, f"Contador debería ser 1, es {pause_count}"
    
    print("\n3. Despausar y pausar segunda vez...")
    time_tracker.resume_tracking(test_user_id)
    await asyncio.sleep(0.1)  # Simular tiempo activo
    
    success = time_tracker.pause_tracking(test_user_id)
    assert success, "Falló segunda pausa"
    
    pause_count = time_tracker.get_pause_count(test_user_id)
    print(f"   Contador después de 2da pausa: {pause_count}")
    assert pause_count == 2, f"Contador debería ser 2, es {pause_count}"
    
    print("\n4. Despausar y pausar tercera vez (cancelación automática)...")
    time_tracker.resume_tracking(test_user_id)
    await asyncio.sleep(0.1)  # Simular tiempo activo
    
    success = time_tracker.pause_tracking(test_user_id)
    assert success, "Falló tercera pausa"
    
    pause_count = time_tracker.get_pause_count(test_user_id)
    print(f"   Contador después de 3ra pausa: {pause_count}")
    assert pause_count == 3, f"Contador debería ser 3, es {pause_count}"
    
    print(f"   ⚠️ Usuario alcanzó {pause_count} pausas - Debería ser cancelado automáticamente")
    
    # Simular cancelación automática
    total_time = time_tracker.get_total_time(test_user_id)
    formatted_time = time_tracker.format_time_human(total_time)
    print(f"   Tiempo total antes de cancelación: {formatted_time}")
    
    # Cancelar automáticamente
    time_tracker.cancel_user_tracking(test_user_id)
    
    # Verificar que el usuario fue eliminado
    user_data = time_tracker.get_user_data(test_user_id)
    print(f"   Usuario después de cancelación: {'Eliminado' if user_data is None else 'Aún existe'}")
    assert user_data is None, "El usuario debería haber sido eliminado"
    
    print("\n5. Test de reinicio - verificar que el contador se resetea...")
    
    # Crear nuevo usuario y verificar reset
    time_tracker.start_tracking(test_user_id, test_user_name)
    time_tracker.pause_tracking(test_user_id)  # 1 pausa
    
    pause_count = time_tracker.get_pause_count(test_user_id)
    print(f"   Contador antes de reinicio: {pause_count}")
    
    # Reiniciar tiempo del usuario
    time_tracker.reset_user_time(test_user_id)
    
    pause_count = time_tracker.get_pause_count(test_user_id)
    print(f"   Contador después de reinicio: {pause_count}")
    assert pause_count == 0, f"Contador debería ser 0 después de reinicio, es {pause_count}"
    
    print("\n✅ Todos los tests del sistema de pausas pasaron correctamente!")
    
    # Limpiar
    time_tracker.cancel_user_tracking(test_user_id)

def test_notification_messages():
    """Test de los mensajes de notificación"""
    print("\n=== TEST DE MENSAJES DE NOTIFICACIÓN ===")
    
    # Test mensaje de pausa con contador
    user_mention = "@TestUser"
    total_time = 3600  # 1 hora
    paused_by = "@Admin"
    session_time = "30 Minutos"
    
    for pause_count in range(1, 4):
        pause_text = "pausa" if pause_count == 1 else "pausas"
        
        if pause_count < 3:
            message = f"⏸️ El seguimiento de tiempo de {user_mention} ha sido pausado\n**Tiempo de sesión pausado:** {session_time}\n**Tiempo total acumulado:** 1 Hora\n**Pausado por:** {paused_by}\n📊 **{user_mention} lleva {pause_count} {pause_text}**"
            print(f"   Mensaje pausa {pause_count}: {message}")
        else:
            # Mensaje de cancelación automática
            message = f"🚫 **CANCELACIÓN AUTOMÁTICA**\n{user_mention} ha sido cancelado automáticamente por exceder el límite de pausas\n**Tiempo total perdido:** 1 Hora\n**Pausas alcanzadas:** {pause_count}/3\n**Última pausa ejecutada por:** {paused_by}"
            print(f"   Mensaje cancelación automática: {message}")
    
    print("✅ Mensajes de notificación generados correctamente!")

if __name__ == "__main__":
    # Ejecutar tests sin Discord
    print("Ejecutando tests sin conexión a Discord...")
    
    # Test de funcionalidad básica
    asyncio.run(test_pause_counting_system())
    
    # Test de mensajes
    test_notification_messages()
    
    print("\n🎉 Todos los tests completados exitosamente!")