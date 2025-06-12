#!/usr/bin/env python3
"""
Archivo principal alternativo para hosts que buscan main.py
Este archivo simplemente importa y ejecuta bot.py
"""

import os
import sys

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar y ejecutar el bot
if __name__ == "__main__":
    import bot