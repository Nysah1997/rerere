"""
Test para verificar el sistema de cálculo de créditos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

def test_credit_calculation():
    """Test del sistema de cálculo de créditos"""
    
    print("=== Test del Sistema de Créditos ===")
    
    print("\n--- Usuarios SIN rol especial ---")
    test_cases_regular = [
        (0, 0),        # 0 segundos = 0 créditos
        (1800, 0),     # 30 minutos = 0 créditos
        (3600, 3),     # 1 hora = 3 créditos
        (5400, 3),     # 1.5 horas = 3 créditos
        (7200, 5),     # 2 horas = 5 créditos
    ]
    
    for seconds, expected_credits in test_cases_regular:
        hours = seconds / 3600
        credits = calculate_credits(seconds, False)
        status = "✅" if credits == expected_credits else "❌"
        print(f"{status} {hours:.1f} horas = {credits} créditos (esperado: {expected_credits})")
    
    print("\n--- Usuarios CON rol especial ---")
    test_cases_special = [
        (0, 0),        # 0 segundos = 0 créditos
        (1800, 0),     # 30 minutos = 0 créditos
        (3600, 3),     # 1 hora = 3 créditos
        (5400, 3),     # 1.5 horas = 3 créditos
        (7200, 5),     # 2 horas = 5 créditos
        (9000, 5),     # 2.5 horas = 5 créditos
        (10800, 10),   # 3 horas = 10 créditos
        (12600, 10),   # 3.5 horas = 10 créditos
        (14400, 12),   # 4 horas = 12 créditos
    ]
    
    for seconds, expected_credits in test_cases_special:
        hours = seconds / 3600
        credits = calculate_credits(seconds, True)
        status = "✅" if credits == expected_credits else "❌"
        print(f"{status} {hours:.1f} horas = {credits} créditos (esperado: {expected_credits})")
    
    print("\n=== Conversión de Créditos ===")
    print("Usuarios regulares: 1h=3, 2h=5")
    print("Usuarios especiales: 1h=3, 2h=5, 3h=10, 4h=12")
    print("✅ Test completado")

if __name__ == "__main__":
    test_credit_calculation()