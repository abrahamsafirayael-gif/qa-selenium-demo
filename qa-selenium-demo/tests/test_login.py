import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.login
def test_login_exitoso(driver):
    login = LoginPage(driver).load()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.wait_for_url_contains("inventory")
    assert inventory.title() == "Products"


@pytest.mark.login
@pytest.mark.parametrize(
    "username, password, mensaje_esperado",
    [
        ("standard_user", "incorrecta", "Username and password do not match"),
        ("usuario_inexistente", "secret_sauce", "Username and password do not match"),
        ("locked_out_user", "secret_sauce", "this user has been locked out"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("", "", "Username is required"),
    ],
    ids=[
        "password_incorrecta",
        "usuario_inexistente",
        "usuario_bloqueado",
        "usuario_vacio",
        "password_vacia",
        "ambos_vacios",
    ],
)
def test_login_invalido(driver, username, password, mensaje_esperado):
    login = LoginPage(driver).load()
    login.login(username, password)

    assert mensaje_esperado in login.error_message()


@pytest.mark.login
def test_logout(driver):
    LoginPage(driver).load().login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.wait_for_url_contains("inventory")
    inventory.logout()

    login = LoginPage(driver)
    assert login.find(login.LOGIN_BUTTON).is_displayed()


@pytest.mark.login
def test_no_se_puede_acceder_al_inventario_sin_login(driver):
    driver.get("https://www.saucedemo.com/inventory.html")

    login = LoginPage(driver)
    assert "only access '/inventory.html' when you are logged in" in login.error_message()
