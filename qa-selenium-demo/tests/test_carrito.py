import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture
def inventory(driver):
    """Deja al usuario logueado y parado en el inventario."""
    LoginPage(driver).load().login("standard_user", "secret_sauce")
    page = InventoryPage(driver)
    page.wait_for_url_contains("inventory")
    return page


@pytest.mark.carrito
def test_inventario_muestra_6_productos(inventory):
    assert inventory.item_count() == 6


@pytest.mark.smoke
@pytest.mark.carrito
def test_agregar_producto_actualiza_badge(inventory):
    assert inventory.cart_count() == 0

    inventory.add_backpack()

    assert inventory.cart_count() == 1


@pytest.mark.carrito
def test_agregar_dos_productos_y_verificar_carrito(driver, inventory):
    inventory.add_backpack()
    inventory.add_bike_light()
    assert inventory.cart_count() == 2

    inventory.go_to_cart()
    cart = CartPage(driver)

    assert cart.item_count() == 2
    assert "Sauce Labs Backpack" in cart.item_names()
    assert "Sauce Labs Bike Light" in cart.item_names()


@pytest.mark.carrito
def test_quitar_producto_vacia_el_badge(inventory):
    inventory.add_backpack()
    assert inventory.cart_count() == 1

    inventory.remove_backpack()

    assert inventory.cart_count() == 0


@pytest.mark.carrito
@pytest.mark.parametrize(
    "orden, key",
    [
        ("lohi", lambda precios: precios == sorted(precios)),
        ("hilo", lambda precios: precios == sorted(precios, reverse=True)),
    ],
    ids=["precio_menor_a_mayor", "precio_mayor_a_menor"],
)
def test_ordenar_por_precio(inventory, orden, key):
    inventory.sort_by(orden)

    assert key(inventory.prices())
