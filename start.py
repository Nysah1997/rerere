#!/usr/bin/env python3
"""
Script de inicio universal para diferentes hosts de Discord bot
Compatible con Pterodactyl, Railway, Heroku, Replit y otros hosts
"""

import os
import sys
import subprocess
import json

def install_dependencies():
    """Instalar dependencias si no están disponibles"""
    try:
        import discord
        print("discord.py detectado")
        return True
    except ImportError:
        print("Instalando discord.py...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "discord.py", "--user", "--quiet"])
            print("discord.py instalado correctamente")
            return True
        except Exception as e:
            print(f"Error instalando discord.py: {e}")
            return False

def check_config():
    """Verificar configuración del bot"""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        token = config.get('discord_bot_token', '').strip()
        if token:
            print("Token encontrado en config.json")
            return True
            
        env_token = os.getenv('DISCORD_BOT_TOKEN', '').strip()
        if env_token:
            print("Token encontrado en variables de entorno")
            return True
            
        print("CONFIGURACION REQUERIDA:")
        print("Edita config.json y pon tu token en 'discord_bot_token'")
        print("O configura la variable DISCORD_BOT_TOKEN")
        return False
        
    except FileNotFoundError:
        print("Error: config.json no encontrado")
        return False
    except Exception as e:
        print(f"Error verificando configuración: {e}")
        return False

def main():
    """Función principal de inicio"""
    print("Iniciando Discord Time Tracker Bot...")
    
    # Verificar e instalar dependencias
    if not install_dependencies():
        sys.exit(1)
    
    # Verificar configuración
    if not check_config():
        sys.exit(1)
    
    # Importar y ejecutar el bot
    try:
        print("Cargando bot...")
        import bot
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()