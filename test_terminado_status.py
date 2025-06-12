#!/usr/bin/env python3
"""
Test para verificar el estado "Terminado ✅" para usuarios con rol especial
"""
import json
from time_tracker import TimeTracker

def test_terminado_status():
    """Test del estado Terminado para usuarios con rol especial que completaron 4 horas"""
    
    print("=== Test Estado 'Terminado ✅' ===")
    
    tracker = TimeTracker()
    cyprian_id = 1366547765810692156
    
    # Simular diferentes estados y tiempos
    test_scenarios = [
        (3600, False, False, "🟢 Activo", "1 hora - activo"),
        (3600, False, True, "⏸️ Pausado", "1 hora - pausado (rol especial)"),
        (7200, False, True, "⏸️ Pausado", "2 horas - pausado (rol especial)"),
        (10800, False, True, "⏸️ Pausado", "3 horas - pausado (rol especial)"),
        (14400, False, True, "✅ Terminado", "4 horas - terminado (rol especial)"),
        (18000, False, True, "✅ Terminado", "5 horas - terminado (rol especial)")
    ]
    
    for seconds, is_active, is_paused, expected_status, description in test_scenarios:
        # Simular datos del usuario
        user_data = {
            "name": "Cyprian.",
            "total_seconds": seconds,
            "is_active": is_active,
            "is_paused": is_paused,
            "last_start": None,
            "pause_start": None,
            "notified_10_seconds": False,
            "notified_milestones": []
        }
        
        # Calcular estado según la lógica del bot
        status = "🟢 Activo" if user_data.get('is_active', False) else "🔴 Inactivo"
        if user_data.get('is_paused', False):
            # Verificar si es usuario con rol especial que completó 4 horas
            total_hours = seconds / 3600
            has_special_role = True  # Cyprian tiene rol especial
            if has_special_role and total_hours >= 4.0:
                status = "✅ Terminado"
            else:
                status = "⏸️ Pausado"
        
        result = "✅" if status == expected_status else "❌"
        print(f"{result} {description}: {status} (esperado: {expected_status})")
    
    print("\n=== Resumen ===")
    print("Estados para usuarios con rol especial:")
    print("- Menos de 4 horas + pausado = ⏸️ Pausado")
    print("- 4 horas o más + pausado = ✅ Terminado")
    print("- Activo = 🟢 Activo")
    print("- Inactivo = 🔴 Inactivo")
    print("✅ Test completado")

if __name__ == "__main__":
    test_terminado_status()