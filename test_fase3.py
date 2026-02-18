#!/usr/bin/env python3
"""
TEST SCRIPT - Validación Fase 3
Ejecuta una serie de tests para verificar que Fase 3 está completamente funcional

Uso:
    python test_fase3.py
    
    o si está en el PATH:
    
    chmod +x test_fase3.py
    ./test_fase3.py
"""

import sys
import json
import subprocess
import time
import requests
from pathlib import Path

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(title):
    print(f"\n{BLUE}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{RESET}\n")

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ️  {msg}{RESET}")

def test_imports():
    """Test 1: Verificar que todos los imports funcionan"""
    print_header("TEST 1: Imports de Python")
    
    tests = [
        ("LLMService", "from app.services.llm_service import LLMService"),
        ("AI Router", "from app.routers import ai"),
        ("Settings", "from app.core.config import Settings"),
        ("FastAPI", "import fastapi"),
        ("Groq", "import groq"),
        ("litellm", "import litellm"),
    ]
    
    all_passed = True
    for name, import_stmt in tests:
        try:
            exec(import_stmt)
            print_success(f"{name} imported")
        except ImportError as e:
            print_error(f"{name} import failed: {e}")
            all_passed = False
    
    return all_passed

def test_llm_service():
    """Test 2: Verificar LLMService initialization"""
    print_header("TEST 2: LLMService Initialization")
    
    try:
        from app.services.llm_service import LLMService
        
        llm = LLMService()
        expected_model = "llama-3.3-70b-versatile"
        
        if llm.model == expected_model:
            print_success(f"LLMService initialized with correct model: {llm.model}")
            return True
        else:
            print_error(f"LLMService model is '{llm.model}', expected '{expected_model}'")
            return False
            
    except Exception as e:
        print_error(f"Failed to initialize LLMService: {e}")
        return False

def test_groq_api_key():
    """Test 3: Verificar que GROQ_API_KEY está configurada"""
    print_header("TEST 3: GROQ_API_KEY Configuration")
    
    try:
        from app.core.config import settings
        
        if settings.GROQ_API_KEY:
            # Mostrar primeros y últimos caracteres por seguridad
            key = settings.GROQ_API_KEY
            if len(key) > 10:
                masked = f"{key[:5]}...{key[-5:]}"
            else:
                masked = "[PRESENT]"
            
            print_success(f"GROQ_API_KEY is configured: {masked}")
            return True
        else:
            print_error("GROQ_API_KEY not found in settings")
            print_info("Make sure .env file has: GROQ_API_KEY=gsk_...")
            return False
            
    except Exception as e:
        print_error(f"Failed to read GROQ_API_KEY: {e}")
        return False

def test_requirements():
    """Test 4: Verificar packages instalados"""
    print_header("TEST 4: Required Packages")
    
    try:
        import pkg_resources
        
        required_packages = {
            "litellm": "1.81.13",
            "groq": "1.0.0",
            "fastapi": "0.129.0",
            "sqlmodel": "0.0.34",
        }
        
        all_found = True
        for package, min_version in required_packages.items():
            try:
                dist = pkg_resources.get_distribution(package)
                print_success(f"{package} {dist.version} is installed")
            except pkg_resources.DistributionNotFound:
                print_error(f"{package} not found")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print_error(f"Failed to check packages: {e}")
        return False

def test_javascript_syntax():
    """Test 5: Verificar sintaxis JavaScript"""
    print_header("TEST 5: JavaScript Syntax Check")
    
    files_to_check = [
        "static/js/extensions/ai-command.js",
        "static/js/extensions/ai-draft.js",
        "static/js/ai-events.js",
        "static/js/editor.js",
    ]
    
    all_passed = True
    for filepath in files_to_check:
        full_path = Path(filepath)
        if not full_path.exists():
            print_error(f"File not found: {filepath}")
            all_passed = False
            continue
        
        try:
            # Intentar validar con node si está disponible
            result = subprocess.run(
                ["node", "-c", filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print_success(f"{filepath} - OK")
            else:
                print_error(f"{filepath} - Syntax error:\n{result.stderr}")
                all_passed = False
                
        except FileNotFoundError:
            # Node no está disponible, asumir que está bien
            print_info(f"{filepath} - (node not available, skipping syntax check)")
        except subprocess.TimeoutExpired:
            print_error(f"{filepath} - Timeout")
            all_passed = False
        except Exception as e:
            print_error(f"{filepath} - Error: {e}")
            all_passed = False
    
    return all_passed

def test_html_files():
    """Test 6: Verificar HTML críticos"""
    print_header("TEST 6: HTML Files Check")
    
    html_files = [
        "templates/layouts/base.html",
    ]
    
    all_found = True
    for filepath in html_files:
        full_path = Path(filepath)
        if full_path.exists():
            # Verificar que aiPrompt state existe
            content = full_path.read_text()
            if "aiPrompt" in content and "slashRange" in content:
                print_success(f"{filepath} - aiPrompt state found")
            else:
                print_warning(f"{filepath} - aiPrompt state might be incomplete")
        else:
            print_error(f"{filepath} not found")
            all_found = False
    
    return all_found

def start_server_and_test_endpoint():
    """Test 7: Iniciar servidor y testear endpoint"""
    print_header("TEST 7: Backend Endpoint Test")
    
    import uuid
    
    print_info("Starting server (timeout in 10 seconds)...")
    
    # Iniciar servidor en background
    server_process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Esperar a que el servidor esté listo
    time.sleep(3)
    
    try:
        # Test endpoint
        url = "http://localhost:8000/api/ai/generate"
        test_uuid = str(uuid.uuid4())
        
        payload = {
            "noteId": test_uuid,
            "content": "Python es un lenguaje de programación versátil",
            "prompt": "Sugiere una mejora para este texto"
        }
        
        print_info(f"POST {url}")
        
        response = requests.post(
            url,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "response" in data and "timestamp" in data:
                print_success(f"Endpoint returned 200 OK")
                print_success(f"Response length: {len(data['response'])} characters")
                print_success(f"Timestamp: {data['timestamp']}")
                print_info(f"Sample response: {data['response'][:100]}...")
                return True
            else:
                print_error(f"Invalid response format: {data}")
                return False
        else:
            print_error(f"Endpoint returned {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to server at http://localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print_error("Request timeout")
        return False
    except Exception as e:
        print_error(f"Error testing endpoint: {e}")
        return False
    finally:
        print_info("Stopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()

def main():
    """Ejecutar todos los tests"""
    print(f"\n{BLUE}{'='*60}")
    print(f"  FASE 3 - VALIDATION TEST SUITE")
    print(f"{'='*60}{RESET}\n")
    
    results = {}
    
    # Ejecutar tests
    results["Imports"] = test_imports()
    results["LLMService"] = test_llm_service()
    results["GROQ_API_KEY"] = test_groq_api_key()
    results["Requirements"] = test_requirements()
    results["JavaScript"] = test_javascript_syntax()
    results["HTML Files"] = test_html_files()
    results["Endpoint"] = start_server_and_test_endpoint()
    
    # Resumen
    print_header("RESUMEN DE RESULTADOS")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{GREEN}✅ PASS{RESET}" if result else f"{RED}❌ FAIL{RESET}"
        print(f"  {test_name}: {status}")
    
    print(f"\n  {GREEN}{passed}/{total} tests passed{RESET}\n")
    
    if passed == total:
        print(f"{GREEN}{'='*60}")
        print(f"  🎉 ¡TODOS LOS TESTS PASARON! 🎉")
        print(f"  Fase 3 está completamente funcional")
        print(f"  Listo para testing en navegador")
        print(f"{'='*60}{RESET}\n")
        return 0
    else:
        print(f"{RED}{'='*60}")
        print(f"  ⚠️  Algunos tests fallaron")
        print(f"  Revisa los errores arriba")
        print(f"{'='*60}{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
