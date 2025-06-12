#!/usr/bin/env python3
"""
Script de ejecución universal para hosts de Discord bot
Compatible con diferentes proveedores de hosting
"""

import os
import sys

# Configurar variables de entorno por defecto si no existen
if not os.getenv('PY_FILE'):
    os.environ['PY_FILE'] = 'bot.py'

if not os.getenv('REQUIREMENTS_FILE'):
    os.environ['REQUIREMENTS_FILE'] = 'requirements.txt'

# Ejecutar el bot
if __name__ == "__main__":
    # Importar el bot principal
    exec(open('bot.py').read())