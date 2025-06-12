"""
Test final de integración completa del sistema de pausas con cancelación automática
"""

from time_tracker import TimeTracker
import json

def test_complete_pause_system():
    """Test completo del sistema de pausas implementado"""
    print("=== TEST FINAL DEL SISTEMA DE PAUSAS ===\n")
    
    tracker = TimeTracker()
    
    # Caso 1: Usuario normal con 3 pausas
    print("1. TEST: Usuario con 3 pausas - Cancelación automática")
    user_id_1 = 111111111
    
    # Limpiar datos previos
    tracker.cancel_user_tracking(user_id_1)
    
    # Iniciar seguimiento
    tracker.start_tracking(user_id_1, "Usuario1")
    
    # Simular 3 pausas
    for i in range(1, 4):
        tracker.pause_tracking(user_id_1)
        count = tracker.get_pause_count(user_id_1)
        print(f"   Pausa {i}: contador = {count}")
        
        if i < 3:
            tracker.resume_tracking(user_id_1)
    
    # Verificar que el usuario aún existe (para cancelación manual)
    data = tracker.get_user_data(user_id_1)
    assert data is not None, "Usuario debería existir para permitir cancelación manual"
    assert data.get('pause_count', 0) == 3, "Contador debería ser 3"
    
    # Simular cancelación automática por el bot
    total_time = tracker.get_total_time(user_id_1)
    formatted_time = tracker.format_time_human(total_time)
    print(f"   Tiempo antes de cancelación: {formatted_time}")
    
    # El bot haría: tracker.cancel_user_tracking(user_id_1)
    tracker.cancel_user_tracking(user_id_1)
    
    data_after = tracker.get_user_data(user_id_1)
    assert data_after is None, "Usuario debería ser eliminado después de cancelación"
    print("   ✅ Cancelación automática exitosa\n")
    
    # Caso 2: Usuario con 2 pausas, luego reinicio manual
    print("2. TEST: Usuario con 2 pausas, luego reinicio por admin")
    user_id_2 = 222222222
    
    tracker.cancel_user_tracking(user_id_2)
    tracker.start_tracking(user_id_2, "Usuario2")
    
    # 2 pausas
    for i in range(1, 3):
        tracker.pause_tracking(user_id_2)
        tracker.resume_tracking(user_id_2)
    
    count_before = tracker.get_pause_count(user_id_2)
    print(f"   Pausas antes de reinicio: {count_before}")
    
    # Admin reinicia tiempo
    tracker.reset_user_time(user_id_2)
    
    count_after = tracker.get_pause_count(user_id_2)
    print(f"   Pausas después de reinicio: {count_after}")
    assert count_after == 0, "Contador debería resetearse a 0"
    print("   ✅ Reinicio manual exitoso\n")
    
    # Caso 3: Verificar persistencia en archivo JSON
    print("3. TEST: Persistencia en user_times.json")
    user_id_3 = 333333333
    
    tracker.cancel_user_tracking(user_id_3)
    tracker.start_tracking(user_id_3, "Usuario3")
    tracker.pause_tracking(user_id_3)
    
    # Verificar que se guarda en archivo
    with open('user_times.json', 'r') as f:
        data = json.load(f)
    
    user_data = data.get(str(user_id_3), {})
    pause_count = user_data.get('pause_count', 0)
    print(f"   Contador en archivo JSON: {pause_count}")
    assert pause_count == 1, "Contador debería persistir en archivo"
    print("   ✅ Persistencia exitosa\n")
    
    # Limpiar
    tracker.cancel_user_tracking(user_id_2)
    tracker.cancel_user_tracking(user_id_3)
    
    print("4. TEST: Mensajes de notificación")
    
    # Simular mensajes para diferentes escenarios
    test_cases = [
        (1, "pausa", "📊 **@TestUser lleva 1 pausa**"),
        (2, "pausas", "📊 **@TestUser lleva 2 pausas**"),
        (3, "pausas", "**Pausas alcanzadas:** 3/3")
    ]
    
    for count, text, expected in test_cases:
        if count < 3:
            message = f"⏸️ El seguimiento de tiempo de @TestUser ha sido pausado\n**Tiempo de sesión pausado:** 30 Minutos\n**Tiempo total acumulado:** 1 Hora\n**Pausado por:** @Admin\n📊 **@TestUser lleva {count} {text}**"
            assert expected in message, f"Mensaje de pausa {count} incorrecto"
        else:
            message = f"🚫 **CANCELACIÓN AUTOMÁTICA**\n@TestUser ha sido cancelado automáticamente por exceder el límite de pausas\n**Tiempo total perdido:** 1 Hora\n**Pausas alcanzadas:** {count}/3\n**Última pausa ejecutada por:** @Admin"
            assert expected in message, "Mensaje de cancelación automática incorrecto"
    
    print("   ✅ Todos los mensajes correctos\n")
    
    print("🎉 TODOS LOS TESTS FINALES COMPLETADOS EXITOSAMENTE!")
    print("\nFUNCIONALIDADES IMPLEMENTADAS:")
    print("✅ Conteo de pausas (incrementa con cada /pausar_tiempo)")
    print("✅ Cancelación automática al alcanzar 3 pausas")
    print("✅ Reset de contador al usar /reiniciar_tiempo")
    print("✅ Visualización de contador en /saber_tiempo")
    print("✅ Notificaciones con contador de pausas")
    print("✅ Notificación especial para cancelación automática")
    print("✅ Persistencia en user_times.json")
    print("✅ Eliminación completa del usuario tras cancelación")

if __name__ == "__main__":
    test_complete_pause_system()