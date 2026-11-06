import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecutar Chrome sin interfaz grafica (necesario en CI)",
    )


@pytest.fixture
def driver(request):
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # Evita popups de "cambiar contrasena" de Chrome en saucedemo
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda una captura de pantalla cuando un test falla."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"screenshots/{item.name}_{timestamp}.png"
            driver.save_screenshot(path)
            print(f"\nCaptura guardada en: {path}")
