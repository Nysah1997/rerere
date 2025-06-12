"""
Test específico para verificar el milestone de Cyprian
"""
import json
from datetime import datetime

def test_cyprian_milestone():
    """Test manual del milestone de Cyprian"""
    
    # Cargar datos actuales
    with open('user_times.json', 'r') as f:
        data = json.load(f)
    
    cyprian_id = "1366547765810692156"
    
    if cyprian_id not in data:
        print("❌ Cyprian no encontrado en los datos")
        return
    
    user_data = data[cyprian_id]
    print(f"📊 Datos de Cyprian:")
    print(f"  - Nombre: {user_data.get('name')}")
    print(f"  - Tiempo total: {user_data.get('total_seconds')} segundos")
    print(f"  - Activo: {user_data.get('is_active')}")
    print(f"  - Pausado: {user_data.get('is_paused')}")
    print(f"  - Inicio sesión: {user_data.get('last_start')}")
    print(f"  - Inicio pausa: {user_data.get('pause_start')}")
    print(f"  - Milestones notificados: {user_data.get('notified_milestones', [])}")
    
    # Calcular tiempo de sesión
    if user_data.get('last_start'):
        session_start = datetime.fromisoformat(user_data['last_start'])
        
        if user_data.get('is_paused') and user_data.get('pause_start'):
            pause_start = datetime.fromisoformat(user_data['pause_start'])
            session_time = (pause_start - session_start).total_seconds()
        else:
            current_time = datetime.now()
            session_time = (current_time - session_start).total_seconds()
        
        print(f"  - Tiempo de sesión: {session_time} segundos ({session_time/3600:.2f} horas)")
        
        # Verificar si debería recibir notificación
        total_hours = int(user_data.get('total_seconds', 0) // 3600)
        hour_milestone = total_hours * 3600
        notified_milestones = user_data.get('notified_milestones', [])
        
        print(f"  - Horas totales: {total_hours}")
        print(f"  - Milestone de hora: {hour_milestone}")
        print(f"  - ¿Sesión >= 1 hora?: {session_time >= 3600}")
        print(f"  - ¿Ya notificado milestone?: {hour_milestone in notified_milestones}")
        
        if session_time >= 3600 and hour_milestone not in notified_milestones:
            print("✅ Cyprian DEBERÍA recibir notificación de milestone")
        else:
            print("❌ Cyprian NO debería recibir notificación")
            if session_time < 3600:
                print(f"    Razón: Sesión no alcanza 1 hora ({session_time/3600:.2f} horas)")
            if hour_milestone in notified_milestones:
                print(f"    Razón: Ya fue notificado del milestone {total_hours} horas")

if __name__ == "__main__":
    test_cyprian_milestone()