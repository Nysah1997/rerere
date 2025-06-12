#!/usr/bin/env python3
"""
Test específico para verificar créditos de Cyprian con rol especial
"""
import json
from time_tracker import TimeTracker

def calculate_credits(total_seconds: float, has_special_role: bool = False) -> int:
    """Calcular créditos basado en el tiempo total"""
    total_hours = total_seconds / 3600
    
    if has_special_role:
        # Usuarios con rol especial: 1h=3, 2h=5, 3h=10, 4h=12
        if total_hours >= 4.0:
            return 12  # 4 horas = 12 créditos
        elif total_hours >= 3.0:
            return 10  # 3 horas = 10 créditos
        elif total_hours >= 2.0:
            return 5   # 2 horas = 5 créditos
        elif total_hours >= 1.0:
            return 3   # 1 hora = 3 créditos
        else:
            return 0   # Menos de 1 hora = 0 créditos
    else:
        # Usuarios sin rol especial: 1h=3, 2h=5
        if total_hours >= 2.0:
            return 5  # 2 horas = 5 créditos
        elif total_hours >= 1.0:
            return 3  # 1 hora = 3 créditos
        else:
            return 0  # Menos de 1 hora = 0 créditos

def test_cyprian_credits():
    """Test específico para Cyprian con diferentes tiempos"""
    
    print("=== Test de Créditos para Cyprian (Rol Especial) ===")
    
    cyprian_id = 1366547765810692156
    tracker = TimeTracker()
    
    # Simular diferentes tiempos para Cyprian
    test_times = [
        (3600, "1 hora", 3),     # 1 hora = 3 créditos
        (7200, "2 horas", 5),    # 2 horas = 5 créditos
        (10800, "3 horas", 10),  # 3 horas = 10 créditos
        (14400, "4 horas", 12),  # 4 horas = 12 créditos
    ]
    
    for seconds, description, expected_credits in test_times:
        # Simular tiempo acumulado
        tracker.data[str(cyprian_id)] = {
            "name": "Cyprian.",
            "total_seconds": seconds,
            "is_active": False,
            "is_paused": False,
            "last_start": None,
            "pause_start": None,
            "notified_10_seconds": False,
            "notified_milestones": []
        }
        tracker.save_data()
        
        # Calcular créditos con rol especial
        credits = calculate_credits(seconds, True)
        formatted_time = tracker.format_time_human(seconds)
        
        status = "✅" if credits == expected_credits else "❌"
        print(f"{status} {description} ({formatted_time}) = {credits} créditos (esperado: {expected_credits})")
    
    # Limpiar datos de prueba
    if str(cyprian_id) in tracker.data:
        del tracker.data[str(cyprian_id)]
        tracker.save_data()
    
    print("\n=== Resumen ===")
    print("Cyprian tiene el rol 'gold' (ID: 1382069325690830888)")
    print("Conversión de créditos para rol especial:")
    print("- 1 hora = 3 créditos")
    print("- 2 horas = 5 créditos") 
    print("- 3 horas = 10 créditos")
    print("- 4 horas = 12 créditos")
    print("✅ Test completado")

if __name__ == "__main__":
    test_cyprian_credits()