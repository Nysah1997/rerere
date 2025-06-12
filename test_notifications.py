#!/usr/bin/env python3
"""
Script de prueba para verificar las notificaciones del bot
"""

from time_tracker import TimeTracker
import time

def test_notification_trigger():
    """Simular el proceso de alcanzar 10 segundos para probar notificaciones"""
    tracker = TimeTracker()
    
    # Limpiar datos de prueba si existen
    test_user_id = 999999999
    tracker.cancel_user_tracking(test_user_id)
    
    print("Iniciando seguimiento de usuario de prueba...")
    tracker.start_tracking(test_user_id, "UsuarioPrueba")
    
    # Simular 5 segundos de actividad
    time.sleep(5)
    
    # Pausar y verificar tiempo
    tracker.pause_tracking(test_user_id)
    current_time = tracker.get_total_time(test_user_id)
    print(f"Tiempo después de 5 segundos: {tracker.format_time_display(current_time)}")
    
    # Agregar 6 segundos más manualmente para superar los 10 segundos
    tracker.add_minutes(test_user_id, "UsuarioPrueba", 0)  # 0 minutos
    tracker.data[str(test_user_id)]['total_seconds'] += 6  # Agregar 6 segundos directamente
    tracker.save_data()
    
    final_time = tracker.get_total_time(test_user_id)
    print(f"Tiempo final: {tracker.format_time_display(final_time)}")
    print(f"¿Ha sido notificado? {tracker.has_notified_10_seconds(test_user_id)}")
    
    # Verificar si se debe notificar
    if final_time >= 10 and not tracker.has_notified_10_seconds(test_user_id):
        print("✅ Debería enviarse notificación!")
        tracker.mark_10_seconds_notified(test_user_id)
    else:
        print("❌ No se debería enviar notificación")
    
    # Limpiar
    tracker.cancel_user_tracking(test_user_id)
    print("Prueba completada")

if __name__ == "__main__":
    test_notification_trigger()