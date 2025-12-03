"""
Script de verificación de setup
Verifica que todas las dependencias estén instaladas correctamente
"""

import sys
import io

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ requerido. Versión actual: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    dependencies = {
        'pygame': 'pygame-ce',  # pygame-ce es compatible con pygame
        'pytmx': 'pytmx'
    }
    
    all_ok = True
    for module_name, package_name in dependencies.items():
        try:
            __import__(module_name)
            print(f"✅ {package_name} instalado")
        except ImportError:
            print(f"❌ {package_name} NO instalado. Ejecuta: pip install {package_name}")
            all_ok = False
    
    return all_ok

def check_structure():
    """Verifica que la estructura de carpetas esté correcta"""
    import os
    
    required_dirs = [
        'src',
        'assets/sprites',
        'assets/tilesets',
        'assets/ui',
        'assets/audio',
        'data/items',
        'data/characters',
        'data/enemies',
        'data/dialogs',
        'data/quests',
        'data/maps',
        'saves',
        'tests'
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ no existe")
            all_ok = False
    
    return all_ok

def main():
    """Ejecuta todas las verificaciones"""
    print("=" * 50)
    print("Verificación de Setup - El Gremio del Sol Naciente")
    print("=" * 50)
    print()
    
    checks = [
        ("Versión de Python", check_python_version),
        ("Dependencias", check_dependencies),
        ("Estructura de carpetas", check_structure)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 30)
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ ¡Todo está listo! Puedes ejecutar el juego con: python main.py")
        return 0
    else:
        print("❌ Hay problemas que resolver antes de ejecutar el juego")
        return 1

if __name__ == "__main__":
    sys.exit(main())

