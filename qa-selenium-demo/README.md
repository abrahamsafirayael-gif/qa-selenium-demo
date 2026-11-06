# QA Automation – Selenium + Python + Pytest

Framework de pruebas end-to-end sobre [Sauce Demo](https://www.saucedemo.com), una tienda online de práctica. Aplica el patrón **Page Object Model (POM)**, tests parametrizados, esperas explícitas, capturas automáticas ante fallos, reporte HTML e integración continua con GitHub Actions.

![Tests E2E](../../actions/workflows/tests.yml/badge.svg)

## Qué se prueba

| Módulo | Casos |
|---|---|
| **Login** | Login exitoso, 6 escenarios inválidos (password incorrecta, usuario inexistente, usuario bloqueado, campos vacíos), logout, acceso sin sesión |
| **Carrito** | Cantidad de productos, agregar/quitar productos y badge del carrito, contenido del carrito, ordenamiento por precio |

## Stack

- Python 3.10+
- Selenium 4 (Selenium Manager gestiona el driver automáticamente)
- Pytest + pytest-html
- GitHub Actions (CI)

## Estructura

```
├── pages/                  # Page Objects (localizadores + acciones)
│   ├── base_page.py        # Esperas explícitas y métodos comunes
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
├── tests/                  # Casos de prueba (sin localizadores)
│   ├── test_login.py
│   └── test_carrito.py
├── conftest.py             # Fixture del driver + captura en fallos
├── pytest.ini              # Config y markers
└── .github/workflows/      # Pipeline de CI
```

## Cómo ejecutarlo

```bash
# 1. Clonar e instalar
git clone <url-del-repo>
cd qa-selenium-demo
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

# 2. Correr todos los tests
pytest

# 3. Variantes útiles
pytest --headless              # sin abrir el navegador
pytest -m smoke                # solo pruebas de humo
pytest -m login                # solo login
pytest -k "bloqueado"          # por nombre
```

Al finalizar se genera `reports/reporte.html`. Si un test falla, se guarda una captura en `screenshots/`.

## Decisiones de diseño

- **POM:** los tests describen *qué* se prueba; los page objects saben *cómo* interactuar con la UI. Si cambia un localizador, se corrige en un solo lugar.
- **Esperas explícitas:** `WebDriverWait` en lugar de `time.sleep()`, para tests estables y rápidos.
- **Parametrización:** `@pytest.mark.parametrize` cubre varios escenarios de login con un solo test.
- **Fixtures:** `driver` se abre y cierra solo; `inventory` deja la sesión iniciada para los tests de carrito.
- **Markers:** permiten ejecutar suites por tipo (`smoke`, `login`, `carrito`).

## Autora

**Safira Yael Abraham** – QA Manual & Automation Jr.
[LinkedIn](https://www.linkedin.com/in/) · abrahamsafirayael@gmail.com
