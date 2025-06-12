"""
Test para verificar el límite de 2 horas para usuarios sin rol especial
"""
import json
from time_tracker import TimeTracker

def test_2_hour_limit():
    """Test del límite de 2 horas para usuarios sin rol especial"""
    tracker = TimeTracker()
    
    # ID de prueba para usuario sin rol especial
    test_user_id = 999999999999999999
    test_user_name = "TestUser"
    
    print("=== Test del límite de 2 horas ===")
    
    # Simular que el usuario ya tiene 2 horas (7200 segundos)
    print(f"1. Agregando 2 horas manualmente para {test_user_name}...")
    tracker.add_minutes(test_user_id, test_user_name, 120)  # 120 minutos = 2 horas
    
    total_time = tracker.get_total_time(test_user_id)
    total_hours = total_time / 3600
    formatted_time = tracker.format_time_human(total_time)
    
    print(f"   Tiempo total: {total_hours} horas ({formatted_time})")
    
    # Verificar si puede iniciar más seguimiento
    if total_hours >= 2.0:
        print(f"❌ {test_user_name} ya alcanzó el límite de 2 horas")
        print(f"   No se puede iniciar más seguimiento")
        print(f"   Tiempo actual: {formatted_time}")
    else:
        print(f"✅ {test_user_name} puede continuar seguimiento")
    
    # Limpiar datos de prueba
    print(f"\n2. Limpiando datos de prueba...")
    tracker.cancel_user_tracking(test_user_id)
    
    print("✅ Test completado")

if __name__ == "__main__":
    test_2_hour_limit()