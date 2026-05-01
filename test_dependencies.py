#!/usr/bin/env python3
"""Test all dependencies"""
import sys

packages = ['requests', 'ntplib', 'pytz', 'urllib3', 'icmplib', 'colorama', 'linecache']
failed = []

print("=" * 50)
print("VERIFICACIÓN DE DEPENDENCIAS")
print("=" * 50)

for pkg in packages:
    try:
        __import__(pkg)
        print(f"✓ {pkg}")
    except ImportError:
        print(f"✗ {pkg} (FALTA INSTALAR)")
        failed.append(pkg)

print("=" * 50)
if not failed:
    print("✓ Todas las dependencias están disponibles")
    sys.exit(0)
else:
    print(f"✗ Faltan {len(failed)} paquete(s)")
    sys.exit(1)
