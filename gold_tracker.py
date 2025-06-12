
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

class GoldTracker:
    def __init__(self, data_file: str = 'gold_memberships.json'):
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Cargar datos de membresías desde el archivo JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar datos de membresías Gold: {e}")
            return {}
    
    def save_data(self) -> bool:
        """Guardar datos de membresías al archivo JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error al guardar datos de membresías Gold: {e}")
            return False
    
    def grant_gold(self, user_id: int, username: str, role_id: int, role_name: str, granted_by: int) -> bool:
        """Otorgar membresía Gold a un usuario"""
        user_id_str = str(user_id)
        current_time = datetime.now()
        expiry_time = current_time + timedelta(days=30)
        
        self.data[user_id_str] = {
            'username': username,
            'role_id': role_id,
            'role_name': role_name,
            'granted_date': current_time.isoformat(),
            'expiry_date': expiry_time.isoformat(),
            'granted_by': granted_by,
            'is_active': True,
            'notified_expiry': False,
            'days_remaining_when_notified': None
        }
        
        return self.save_data()
    
    def remove_gold(self, user_id: int) -> bool:
        """Remover membresía Gold de un usuario"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return False
        
        # Eliminar completamente el registro del usuario
        del self.data[user_id_str]
        return self.save_data()
    
    def get_user_gold_data(self, user_id: int) -> Optional[Dict]:
        """Obtener datos de membresía Gold de un usuario"""
        user_id_str = str(user_id)
        return self.data.get(user_id_str)
    
    def is_gold_active(self, user_id: int) -> bool:
        """Verificar si la membresía Gold del usuario está activa"""
        user_data = self.get_user_gold_data(user_id)
        if not user_data or not user_data.get('is_active', False):
            return False
        
        # Verificar si no ha expirado
        expiry_date = datetime.fromisoformat(user_data['expiry_date'])
        return datetime.now() < expiry_date
    
    def get_expiring_memberships(self, days_ahead: int = 3) -> list:
        """Obtener membresías que expiran en los próximos X días"""
        expiring = []
        current_time = datetime.now()
        threshold_time = current_time + timedelta(days=days_ahead)
        
        for user_id_str, data in self.data.items():
            if not data.get('is_active', False):
                continue
            
            expiry_date = datetime.fromisoformat(data['expiry_date'])
            
            # Si expira dentro del rango y aún no se ha notificado
            if current_time < expiry_date <= threshold_time:
                if not data.get('notified_expiry', False):
                    days_remaining = (expiry_date - current_time).days
                    expiring.append({
                        'user_id': int(user_id_str),
                        'username': data['username'],
                        'role_name': data['role_name'],
                        'expiry_date': expiry_date,
                        'days_remaining': days_remaining
                    })
        
        return expiring
    
    def get_expired_memberships(self) -> list:
        """Obtener membresías que ya expiraron"""
        expired = []
        current_time = datetime.now()
        
        for user_id_str, data in self.data.items():
            if not data.get('is_active', False):
                continue
            
            expiry_date = datetime.fromisoformat(data['expiry_date'])
            
            if current_time >= expiry_date:
                expired.append({
                    'user_id': int(user_id_str),
                    'username': data['username'],
                    'role_id': data['role_id'],
                    'role_name': data['role_name'],
                    'expiry_date': expiry_date,
                    'granted_date': datetime.fromisoformat(data['granted_date'])
                })
        
        return expired
    
    def mark_expiry_notified(self, user_id: int, days_remaining: int) -> bool:
        """Marcar que se notificó la expiración próxima"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return False
        
        self.data[user_id_str]['notified_expiry'] = True
        self.data[user_id_str]['days_remaining_when_notified'] = days_remaining
        return self.save_data()
    
    def deactivate_membership(self, user_id: int) -> bool:
        """Desactivar membresía (marcar como expirada)"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return False
        
        self.data[user_id_str]['is_active'] = False
        return self.save_data()
    
    def get_all_active_memberships(self) -> Dict:
        """Obtener todas las membresías activas"""
        active = {}
        current_time = datetime.now()
        
        for user_id_str, data in self.data.items():
            if not data.get('is_active', False):
                continue
            
            expiry_date = datetime.fromisoformat(data['expiry_date'])
            if current_time < expiry_date:
                active[user_id_str] = data.copy()
                # Agregar días restantes
                days_remaining = (expiry_date - current_time).days
                active[user_id_str]['days_remaining'] = days_remaining
        
        return active
    
    def format_time_remaining(self, expiry_date: datetime) -> str:
        """Formatear tiempo restante hasta expiración"""
        current_time = datetime.now()
        time_diff = expiry_date - current_time
        
        if time_diff.total_seconds() <= 0:
            return "Expirado"
        
        days = time_diff.days
        hours = time_diff.seconds // 3600
        
        if days > 0:
            return f"{days} día{'s' if days != 1 else ''}"
        elif hours > 0:
            return f"{hours} hora{'s' if hours != 1 else ''}"
        else:
            return "Menos de 1 hora"
    
    def cleanup_expired_memberships(self) -> int:
        """Limpiar membresías expiradas del sistema (opcional)"""
        expired_count = 0
        current_time = datetime.now()
        users_to_remove = []
        
        for user_id_str, data in self.data.items():
            expiry_date = datetime.fromisoformat(data['expiry_date'])
            
            # Remover membresías expiradas hace más de 7 días
            if (current_time - expiry_date).days > 7:
                users_to_remove.append(user_id_str)
                expired_count += 1
        
        for user_id_str in users_to_remove:
            del self.data[user_id_str]
        
        if users_to_remove:
            self.save_data()
        
        return expired_count
