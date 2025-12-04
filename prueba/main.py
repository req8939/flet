import flet as ft
import math

# --- DATOS MOCK (Simulación de base de datos) ---
class Donut:
    def __init__(self, name, price, image_url, color_theme, description, nutrition):
        self.name = name
        self.price = price
        self.image_url = image_url
        self.color_theme = color_theme # Hex color
        self.description = description
        self.nutrition = nutrition # Dict: {'Salt': '8g', 'Sugar': '8g', etc.}

# Lista de donas basada en el video
donuts_data = [
    Donut(
        name="Red Velvet",
        price=2.50,
        image_url="https://cdn-icons-png.flaticon.com/512/3081/3081840.png", 
        color_theme=ft.Colors.RED_100,
        description="Una clásica dona roja con chispas blancas.",
        nutrition={'Salt': '8g', 'Sugar': '9g', 'Fat': '12g', 'Energy': '130cal'}
    ),
    Donut(
        name="Pink Sprinkle",
        price=3.00,
        image_url="https://cdn-icons-png.flaticon.com/512/3081/3081829.png",
        color_theme=ft.Colors.PINK_100,
        description="Dulce glaseado de fresa con chispas de colores.",
        nutrition={'Salt': '8g', 'Sugar': '15g', 'Fat': '10g', 'Energy': '150cal'}
    ),
    Donut(
        name="Yellow Glaze",
        price=2.25,
        image_url="https://cdn-icons-png.flaticon.com/512/3081/3081850.png",
        color_theme=ft.Colors.YELLOW_100,
        description="Glaseado de limón cítrico y refrescante.",
        nutrition={'Salt': '6g', 'Sugar': '8g', 'Fat': '9g', 'Energy': '120cal'}
    ),
    Donut(
        name="Blueberry",
        price=2.80,
        image_url="https://cdn-icons-png.flaticon.com/512/3081/3081867.png",
        color_theme=ft.Colors.BLUE_100,
        description="Rellena de mermelada de arándanos frescos.",
        nutrition={'Salt': '7g', 'Sugar': '10g', 'Fat': '11g', 'Energy': '140cal'}
    ),
]

def main(page: ft.Page):
    # Configuración general de la página para simular móvil
    page.title = "Donuts Shop"
    page.window_width = 390
    page.window_height = 844
    page.bgcolor = ft.Colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    # Estado de la aplicación
    current_donut = donuts_data[0]
    cart_qty = ft.Ref[ft.Text]()
    qty_value = 1

    def change_qty(e, delta):
        nonlocal qty_value
        qty_value += delta
        if qty_value < 1: qty_value = 1
        cart_qty.current.value = str(qty_value)
        cart_qty.current.update()

    def add_to_cart(e):
        # Muestra un diálogo de éxito
        dlg = ft.AlertDialog(
            title=ft.Text("¡Orden Realizada!"),
            content=ft.Column([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=60),
                ft.Text(f"Has agregado {qty_value} x {current_donut.name}", text_align=ft.TextAlign.CENTER),
                ft.Text(f"Total: ${qty_value * current_donut.price:.2f}", weight=ft.FontWeight.BOLD, size=20)
            ], height=150, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[
                ft.TextButton("Volver al Inicio", on_click=lambda x: go_home(x))
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def go_home(e):
        if page.dialog:
            page.dialog.open = False
        page.go("/")

    def go_details(e, donut):
        nonlocal current_donut, qty_value
        current_donut = donut
        qty_value = 1 # Reset cantidad
        page.go("/details")

    # --- COMPONENTES UI ---

    def NutritionItem(label, value, percent, color):
        """Crea una fila de información nutricional estilo píldora"""
        return ft.Container(
            padding=10,
            border_radius=20,
            bgcolor=ft.Colors.WHITE54,
            content=ft.Row([
                ft.Container(
                    content=ft.Text(label, size=12, color=ft.Colors.BLACK54, weight=ft.FontWeight.BOLD),
                    width=50
                ),
                ft.Container(
                    content=ft.Text(value, size=12, weight=ft.FontWeight.BOLD),
                    width=40
                ),
                # Barra de progreso circular simple
                ft.Stack([
                    ft.Container(width=30, height=30, border_radius=15, bgcolor=ft.Colors.with_opacity(0.2, color)),
                    ft.Container(
                        content=ft.Text(f"{percent}%", size=10, weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center,
                        width=30, height=30
                    )
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    def BuildDonutCard(donut):
        """Tarjeta de dona para la pantalla principal"""
        return ft.Container(
            width=220,
            height=320,
            margin=ft.margin.only(right=20, bottom=20),
            on_click=lambda e: go_details(e, donut),
            content=ft.Stack([
                # Fondo de la tarjeta
                ft.Container(
                    top=50,
                    width=220,
                    height=270,
                    bgcolor=donut.color_theme,
                    border_radius=ft.border_radius.only(top_left=100, top_right=100, bottom_left=20, bottom_right=20),
                    padding=20,
                    content=ft.Column([
                        ft.Container(height=120), # Espaciador para la imagen
                        ft.Text(donut.name, size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLACK87),
                        ft.Text(f"${donut.price:.2f}", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                        ft.Row([
                            ft.Text("Add", color=ft.Colors.BLACK54, size=12, weight=ft.FontWeight.BOLD),
                            ft.Icon(ft.Icons.ADD, size=14, color=ft.Colors.BLACK)
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)
                ),
                # Imagen flotante
                ft.Image(
                    src=donut.image_url,
                    width=160,
                    height=160,
                    left=30,
                    top=0,
                    # CORRECCIÓN AQUÍ: ft.Animation en lugar de ft.animation.Animation
                    animate_scale=ft.Animation(300, ft.AnimationCurve.BOUNCE_OUT)
                )
            ])
        )

    # --- VISTAS ---

    def home_view():
        return ft.View(
            "/",
            padding=0,
            controls=[
                ft.Container(
                    padding=20,
                    content=ft.Column([
                        # Header
                        ft.Row([
                            ft.Icon(ft.Icons.MENU, color=ft.Colors.BLACK),
                            ft.Icon(ft.Icons.SEARCH, color=ft.Colors.BLACK),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Container(height=20),
                        
                        ft.Text("Donuts Shop", size=32, font_family="Cursive", weight=ft.FontWeight.BOLD),
                        ft.Text("Sweet & Delicious", size=16, color=ft.Colors.GREY),
                        
                        ft.Container(height=40),
                        
                        # Carrusel Horizontal
                        ft.Row(
                            [BuildDonutCard(d) for d in donuts_data],
                            scroll=ft.ScrollMode.AUTO,
                            height=350
                        )
                    ])
                )
            ]
        )

    def details_view():
        return ft.View(
            "/details",
            padding=0,
            bgcolor=current_donut.color_theme,
            controls=[
                ft.Stack([
                    # Botón de regreso
                    ft.Container(
                        top=40, left=20,
                        content=ft.IconButton(ft.Icons.ARROW_BACK_IOS, on_click=lambda _: page.go("/")),
                    ),
                    
                    # Título Header
                    ft.Container(
                        top=40, right=20, left=60,
                        content=ft.Text(current_donut.name, size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
                    ),

                    # Contenido Principal
                    ft.Column([
                        ft.Container(height=100), # Espacio superior
                        
                        # Imagen Gigante Rotatoria (Simulada)
                        ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Image(
                                src=current_donut.image_url,
                                width=280,
                                height=280,
                                fit=ft.ImageFit.CONTAIN,
                                # CORRECCIÓN AQUÍ: ft.Animation en lugar de ft.animation.Animation
                                animate_scale=ft.Animation(800, "elasticOut")
                            )
                        ),

                        ft.Container(height=20),

                        # Panel de Información
                        ft.Container(
                            expand=True,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=ft.border_radius.only(top_left=40, top_right=40),
                            padding=30,
                            content=ft.Column([
                                # Stats Nutricionales
                                ft.Row([
                                    ft.Column([
                                        NutritionItem("Salt", current_donut.nutrition['Salt'], "3", ft.Colors.BLUE),
                                        ft.Container(height=5),
                                        NutritionItem("Sugar", current_donut.nutrition['Sugar'], "8", ft.Colors.PINK),
                                    ], expand=True),
                                    ft.Container(width=10),
                                    ft.Column([
                                        NutritionItem("Fat", current_donut.nutrition['Fat'], "12", ft.Colors.ORANGE),
                                        ft.Container(height=5),
                                        NutritionItem("Energy", current_donut.nutrition['Energy'], "40", ft.Colors.GREEN),
                                    ], expand=True)
                                ]),

                                ft.Container(expand=True), # Spacer

                                # Sección de Compra
                                ft.Row([
                                    # Selector de Cantidad
                                    ft.Container(
                                        padding=5,
                                        border_radius=30,
                                        bgcolor=ft.Colors.GREY_100,
                                        content=ft.Row([
                                            ft.IconButton(ft.Icons.REMOVE, icon_size=16, on_click=lambda e: change_qty(e, -1)),
                                            ft.Text(str(qty_value), ref=cart_qty, weight=ft.FontWeight.BOLD),
                                            ft.IconButton(ft.Icons.ADD, icon_size=16, on_click=lambda e: change_qty(e, 1)),
                                        ], spacing=0)
                                    ),
                                    
                                    ft.Container(width=20),

                                    # Botón de Añadir
                                    ft.Container(
                                        expand=True,
                                        height=60,
                                        bgcolor=ft.Colors.BLACK,
                                        border_radius=30,
                                        on_click=add_to_cart,
                                        padding=ft.padding.symmetric(horizontal=20),
                                        content=ft.Row([
                                            ft.Text("Add to Cart", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                            ft.Text(f"${current_donut.price:.2f}", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                            ])
                        )
                    ], expand=True)
                ], expand=True)
            ]
        )

    def route_change(route):
        page.views.clear()
        page.views.append(home_view())
        if page.route == "/details":
            page.views.append(details_view())
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)