import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

class TimeTracker:
    def __init__(self, data_file: str = 'user_times.json'):
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Cargar datos desde el archivo JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar datos: {e}")
            return {}
    
    def save_data(self) -> bool:
        """Guardar datos al archivo JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error al guardar datos: {e}")
            return False
    
    def start_tracking(self, user_id: int, user_name: str) -> bool:
        """Iniciar el seguimiento de tiempo para un usuario"""
        user_id_str = str(user_id)
        current_time = datetime.now().isoformat()
        
        if user_id_str not in self.data:
            self.data[user_id_str] = {
                'name': user_name,
                'total_seconds': 0,
                'is_active': False,
                'is_paused': False,
                'last_start': None,
                'pause_start': None,
                'notified_10_seconds': False,
                'pause_count': 0
            }
        
        # Si ya está activo, no hacer nada
        if self.data[user_id_str]['is_active'] and not self.data[user_id_str]['is_paused']:
            return False
        
        # Si estaba pausado, reanudar
        if self.data[user_id_str]['is_paused']:
            return self.resume_tracking(user_id)
        
        # Iniciar nuevo seguimiento
        self.data[user_id_str]['is_active'] = True
        self.data[user_id_str]['is_paused'] = False
        self.data[user_id_str]['last_start'] = current_time
        self.data[user_id_str]['name'] = user_name  # Actualizar nombre por si cambió
        
        return self.save_data()
    
    def pause_tracking(self, user_id: int) -> bool:
        """Pausar el seguimiento de tiempo para un usuario"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data or not self.data[user_id_str]['is_active']:
            return False
        
        if self.data[user_id_str]['is_paused']:
            return False
        
        # Calcular tiempo transcurrido y agregarlo al total
        if self.data[user_id_str]['last_start']:
            start_time = datetime.fromisoformat(self.data[user_id_str]['last_start'])
            elapsed_seconds = (datetime.now() - start_time).total_seconds()
            self.data[user_id_str]['total_seconds'] += elapsed_seconds
        
        # Marcar como pausado e incrementar contador de pausas
        self.data[user_id_str]['is_paused'] = True
        self.data[user_id_str]['pause_start'] = datetime.now().isoformat()
        
        # Incrementar contador de pausas
        self.data[user_id_str]['pause_count'] = self.data[user_id_str].get('pause_count', 0) + 1
        
        return self.save_data()
    
    def get_paused_duration(self, user_id: int) -> float:
        """Obtener la duración que el usuario ha estado pausado en segundos"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data or not self.data[user_id_str]['is_paused']:
            return 0.0
        
        pause_start_str = self.data[user_id_str].get('pause_start')
        if not pause_start_str:
            return 0.0
        
        pause_start = datetime.fromisoformat(pause_start_str)
        return (datetime.now() - pause_start).total_seconds()

    def resume_tracking(self, user_id: int) -> bool:
        """Reanudar el seguimiento de tiempo para un usuario"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data or not self.data[user_id_str]['is_active']:
            return False
        
        if not self.data[user_id_str]['is_paused']:
            return False
        
        # Reanudar seguimiento
        self.data[user_id_str]['is_paused'] = False
        self.data[user_id_str]['last_start'] = datetime.now().isoformat()
        self.data[user_id_str]['pause_start'] = None
        
        return self.save_data()
    
    def stop_tracking(self, user_id: int) -> bool:
        """Detener completamente el seguimiento de tiempo para un usuario"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data or not self.data[user_id_str]['is_active']:
            return False
        
        # Si no está pausado, calcular tiempo transcurrido
        if not self.data[user_id_str]['is_paused'] and self.data[user_id_str]['last_start']:
            start_time = datetime.fromisoformat(self.data[user_id_str]['last_start'])
            elapsed_seconds = (datetime.now() - start_time).total_seconds()
            self.data[user_id_str]['total_seconds'] += elapsed_seconds
        
        # Detener seguimiento
        self.data[user_id_str]['is_active'] = False
        self.data[user_id_str]['is_paused'] = False
        self.data[user_id_str]['last_start'] = None
        self.data[user_id_str]['pause_start'] = None
        
        return self.save_data()
    
    def add_minutes(self, user_id: int, user_name: str, minutes: int) -> bool:
        """Agregar minutos al tiempo total de un usuario"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            self.data[user_id_str] = {
                'name': user_name,
                'total_seconds': 0,
                'is_active': False,
                'is_paused': False,
                'last_start': None,
                'pause_start': None,
                'notified_10_seconds': False
            }
        
        self.data[user_id_str]['total_seconds'] += minutes * 60
        self.data[user_id_str]['name'] = user_name  # Actualizar nombre
        
        return self.save_data()
    
    def subtract_minutes(self, user_id: int, minutes: int) -> bool:
        """Restar minutos del tiempo total de un usuario"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return False
        
        seconds_to_subtract = minutes * 60
        self.data[user_id_str]['total_seconds'] = max(0, self.data[user_id_str]['total_seconds'] - seconds_to_subtract)
        
        return self.save_data()
    
    def get_total_time(self, user_id: int) -> float:
        """Obtener el tiempo total (en segundos) para un usuario, incluyendo sesión actual si está activa"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return 0.0
        
        total_seconds = self.data[user_id_str]['total_seconds']
        
        # Si está activo y no pausado, agregar tiempo de la sesión actual
        if (self.data[user_id_str]['is_active'] and 
            not self.data[user_id_str]['is_paused'] and 
            self.data[user_id_str]['last_start']):
            
            start_time = datetime.fromisoformat(self.data[user_id_str]['last_start'])
            current_session_seconds = (datetime.now() - start_time).total_seconds()
            total_seconds += current_session_seconds
        
        return total_seconds
    
    def format_time_display(self, total_seconds: float) -> str:
        """Formatear segundos en formato legible (HH:MM:SS)"""
        if total_seconds < 0:
            total_seconds = 0
        
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def format_seconds_only(self, total_seconds: float) -> str:
        """Formatear segundos en formato simple (X Segundos)"""
        if total_seconds < 0:
            total_seconds = 0
        
        seconds = int(total_seconds)
        return f"{seconds} Segundos"
    
    def format_time_human(self, total_seconds: float) -> str:
        """Formatear tiempo en formato humano detallado (X hora, Y minutos y Z segundos)"""
        if total_seconds < 0:
            total_seconds = 0
        
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        
        parts = []
        
        # Agregar horas
        if hours > 0:
            if hours == 1:
                parts.append("1 hora")
            else:
                parts.append(f"{hours} horas")
        
        # Agregar minutos
        if minutes > 0:
            if minutes == 1:
                parts.append("1 minuto")
            else:
                parts.append(f"{minutes} minutos")
        
        # Agregar segundos
        if seconds > 0:
            if seconds == 1:
                parts.append("1 segundo")
            else:
                parts.append(f"{seconds} segundos")
        
        # Si no hay tiempo registrado
        if not parts:
            return "0 segundos"
        
        # Formatear la respuesta según el número de partes
        if len(parts) == 1:
            return parts[0]
        elif len(parts) == 2:
            return f"{parts[0]} y {parts[1]}"
        elif len(parts) == 3:
            return f"{parts[0]}, {parts[1]} y {parts[2]}"
        else:
            return "0 segundos"
    
    def get_all_tracked_users(self) -> Dict:
        """Obtener todos los usuarios con seguimiento"""
        return self.data.copy()
    
    def get_user_data(self, user_id: int) -> Optional[Dict]:
        """Obtener datos específicos de un usuario"""
        user_id_str = str(user_id)
        return self.data.get(user_id_str)
    
    def reset_user_time(self, user_id: int) -> bool:
        """Reiniciar el tiempo de un usuario a cero"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return False
        
        # Mantener info del usuario pero reiniciar tiempos
        user_name = self.data[user_id_str]['name']
        self.data[user_id_str] = {
            'name': user_name,
            'total_seconds': 0,
            'is_active': False,
            'is_paused': False,
            'last_start': None,
            'pause_start': None,
            'notified_10_seconds': False,
            'pause_count': 0
        }
        
        return self.save_data()
    
    def reset_all_user_times(self) -> int:
        """Reiniciar todos los tiempos de todos los usuarios a cero"""
        count = 0
        
        for user_id_str, data in self.data.items():
            # Mantener info del usuario pero reiniciar tiempos y notificaciones
            user_name = data.get('name', f'Usuario {user_id_str}')
            self.data[user_id_str] = {
                'name': user_name,
                'total_seconds': 0,
                'is_active': False,
                'is_paused': False,
                'last_start': None,
                'pause_start': None,
                'notified_10_seconds': False,
                'pause_count': 0
            }
            count += 1
        
        if count > 0:
            self.save_data()
        
        return count
    
    def cancel_user_tracking(self, user_id: int) -> bool:
        """Cancelar completamente el seguimiento de un usuario eliminando su registro"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return False
        
        # Eliminar completamente el registro del usuario
        del self.data[user_id_str]
        
        return self.save_data()
    
    def cleanup_inactive_users(self, days_threshold: int = 30) -> int:
        """Limpiar usuarios inactivos después de X días (opcional)"""
        current_time = datetime.now()
        users_to_remove = []
        
        for user_id, data in self.data.items():
            if not data['is_active'] and data.get('last_start'):
                last_activity = datetime.fromisoformat(data['last_start'])
                if (current_time - last_activity).days > days_threshold:
                    users_to_remove.append(user_id)
        
        for user_id in users_to_remove:
            del self.data[user_id]
        
        if users_to_remove:
            self.save_data()
        
        return len(users_to_remove)
    
    def has_notified_10_seconds(self, user_id: int) -> bool:
        """Verificar si ya se notificó los 10 segundos para este usuario"""
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            return False
        return self.data[user_id_str].get('notified_10_seconds', False)
    
    def mark_10_seconds_notified(self, user_id: int) -> bool:
        """Marcar que ya se notificaron los 10 segundos para este usuario"""
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            return False
        self.data[user_id_str]['notified_10_seconds'] = True
        return self.save_data()
    
    def get_pause_count(self, user_id: int) -> int:
        """Obtener el número de pausas para un usuario"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return 0
        
        return self.data[user_id_str].get('pause_count', 0)
    
    def reset_pause_count(self, user_id: int) -> bool:
        """Resetear el contador de pausas a cero"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return False
        
        self.data[user_id_str]['pause_count'] = 0
        return self.save_data()
    
    def clear_all_data(self) -> bool:
        """Limpiar completamente todos los datos de usuarios de la base de datos"""
        try:
            # Resetear los datos en memoria
            self.data = {}
            
            # Guardar archivo vacío
            success = self.save_data()
            
            if success:
                print("🗑️ Base de datos completamente limpiada")
                return True
            else:
                print("❌ Error al guardar archivo después de limpiar")
                return False
                
        except Exception as e:
            print(f"❌ Error al limpiar base de datos: {e}")
            return False
