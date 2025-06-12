"""
Test completo del sistema de milestones para usuarios con rol ilimitado
"""
import discord
from discord.ext import commands
import asyncio
import json
from time_tracker import TimeTracker

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
time_tracker = TimeTracker()

# Configuración de canales y roles (usar IDs reales)
NOTIFICATION_CHANNEL_ID = 1382057005870747808  # Canal de milestones
UNLIMITED_ROLE_ID = 1382081735726895174  # Rol de tiempo ilimitado

async def test_milestone_notifications():
    """Test completo del sistema de milestones"""
    print("🧪 Iniciando test del sistema de milestones...")
    
    # Simular datos de usuario con rol ilimitado
    test_user_id = 123456789
    test_user_name = "TestUser"
    
    # Limpiar datos previos
    time_tracker.cancel_user_tracking(test_user_id)
    
    # Simular tiempo acumulado para probar cada milestone
    milestones_to_test = [
        (3600, "1 Hora"),     # 1 hora
        (7200, "2 Horas"),    # 2 horas
        (10800, "3 Horas"),   # 3 horas
        (14400, "4 Horas")    # 4 horas
    ]
    
    print(f"📊 Iniciando seguimiento para {test_user_name}...")
    time_tracker.start_tracking(test_user_id, test_user_name)
    
    # Obtener canal de notificaciones
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    if not channel:
        print(f"❌ No se pudo encontrar el canal con ID: {NOTIFICATION_CHANNEL_ID}")
        return
    
    for milestone_seconds, milestone_name in milestones_to_test:
        print(f"\n🎯 Probando milestone: {milestone_name} ({milestone_seconds} segundos)")
        
        # Simular tiempo acumulado añadiendo minutos
        minutes_to_add = int(milestone_seconds // 60)
        time_tracker.add_minutes(test_user_id, test_user_name, minutes_to_add)
        
        # Verificar tiempo total
        total_time = time_tracker.get_total_time(test_user_id)
        print(f"⏱️ Tiempo total simulado: {total_time} segundos")
        
        # Verificar milestone
        user_data = time_tracker.get_user_data(test_user_id)
        if user_data:
            # Asegurar que existe el campo notified_milestones
            if 'notified_milestones' not in user_data:
                user_data['notified_milestones'] = []
                time_tracker.save_data()
            
            notified_milestones = user_data.get('notified_milestones', [])
            print(f"📋 Milestones ya notificados: {notified_milestones}")
            
            if milestone_seconds not in notified_milestones:
                print(f"✅ Enviando notificación de {milestone_name}...")
                
                # Marcar milestone como notificado
                notified_milestones.append(milestone_seconds)
                user_data['notified_milestones'] = notified_milestones
                time_tracker.save_data()
                
                # Simular notificación
                formatted_time = time_tracker.format_time_human(total_time)
                message = f"🎉 <@{test_user_id}> ha completado {milestone_name}! Tiempo acumulado: {formatted_time}"
                
                try:
                    await channel.send(message)
                    print(f"📨 Notificación enviada: {message}")
                except Exception as e:
                    print(f"❌ Error enviando notificación: {e}")
            else:
                print(f"⚠️ Milestone {milestone_name} ya fue notificado anteriormente")
        
        await asyncio.sleep(1)  # Pausa entre pruebas
    
    print(f"\n🎯 Test completado. Datos finales del usuario:")
    final_data = time_tracker.get_user_data(test_user_id)
    if final_data:
        print(f"📊 Tiempo total: {time_tracker.format_time_human(final_data.get('total_seconds', 0))}")
        print(f"📋 Milestones notificados: {final_data.get('notified_milestones', [])}")
    
    # Limpiar datos de prueba
    time_tracker.cancel_user_tracking(test_user_id)
    print("🧹 Datos de prueba limpiados")

@bot.event
async def on_ready():
    print(f'🤖 Bot conectado como {bot.user}')
    print(f'📊 Iniciando test del sistema de milestones...')
    
    await test_milestone_notifications()
    
    print("✅ Test completado. El bot seguirá ejecutándose...")

if __name__ == "__main__":
    import os
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ Token no encontrado. Configura DISCORD_BOT_TOKEN")