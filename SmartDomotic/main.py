import flet as  ft
import math
class SmartDomotic(ft.Container):
    def create_icon_container(self, icon_data, color, tooltip_text=""):
        """Función auxiliar para crear un contenedor de ícono reutilizable."""
        return ft.Container(
            width=40,
            height=40,
            margin=ft.margin.only(top=20, left=10, right=10, bottom=20),
            border_radius=10,
            bgcolor=color,
            content=ft.IconButton(
                icon=icon_data,
                icon_color=ft.Colors.BLACK,
                tooltip=tooltip_text,
                on_click=lambda e: print(f"{tooltip_text} clicked!")
            ),
            alignment=ft.alignment.center,
        )
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.page = page
        self.page.title ="SmartDomotic"
        self.bg_color = "#ffffff"
        self.dark_white = "#e7e6e9"
        self.prey_color = "#a9acb6"
        self.yellow_color = "#ece5d5"
        self.page.bgcolor = self.bg_color

        # 1.1 Ícono Superior (Fijo: Mail)
        top_icon_control = self.create_icon_container(ft.Icons.MAIL, self.dark_white, "Mailbox")

        # 1.2 Lista de Íconos Centrales
        middle_icons_list = [
            ft.Icons.MENU_SHARP,
            ft.Icons.LIGHT_ROUNDED,
            ft.Icons.MUSIC_NOTE,
            ft.Icons.THERMOSTAT,
            ft.Icons.SECURITY_ROUNDED,
        ]

        data_controls = [
            (ft.Icons.THERMOSTAT, "23ºC"),
            (ft.Icons.FLASH_ON, "50W"),
            (ft.Icons.AIR, "80%"),
        ]
        # Aplicación de la optimización "mejor breve python for"
        # Esto genera la lista [Contenedor, Divisor, Contenedor, Divisor, ...]
        middle_menu_controls = [
            item for icon in middle_icons_list
            for item in (
                self.create_icon_container(icon, self.dark_white),
                ft.Divider(height=1, color=self.dark_white, thickness=1),
            )
        ][:-1] # Quitamos el último separador

        middle_column = ft.Column(
            controls=middle_menu_controls,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0 
        )
        # 1.3 Íconos Inferiores (Fijos: Estado y Avatar)
        bottom_column = ft.Column(
            controls=[
                self.create_icon_container(ft.Icons.CHECK_CIRCLE, self.dark_white, "Status Check"),
                # Placeholder para simular el avatar
                ft.Image(
                    src="assets/avatar.jpg", 
                    width=40, 
                    height=40, 
                    border_radius=20,
                    tooltip="User Profile"
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        self.menu = ft.Container(
            width=60,
            alignment=ft.alignment.center,
            content= ft.Column(
                alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                        top_icon_control,
                        middle_column,
                        bottom_column,
                ]
            )
        )
        self.colum_1 = ft.Column(
            expand=3,
            alignment= ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Stack(
                    expand=True,
                    alignment=ft.alignment.center,
                    controls=[
                        ft.Container(border_radius=15,
                                     expand=True,
                                     content=ft.Image(
                                         src="assets/foto.png",
                                         fit= ft.ImageFit.COVER,
                                         height=1000,
                                         width=1200,
                                     )
                                     ),
                        ft.Container(expand=True, bgcolor= ft.Colors.TRANSPARENT,
                                     border_radius=15, padding=10, margin=ft.margin.only(left=30),
                                     alignment= ft.alignment.top_center,
                                     content=ft.Row(
                                         alignment= ft.MainAxisAlignment.END,
                                         controls = [
                                             ft.Container(
                                                 height=30,
                                                 width=70,
                                                 border_radius=15,
                                                 bgcolor=self.dark_white, # Assume que self.dark_white está definido
                                                 content=ft.Row(
                                                     spacing=2,
                                                     alignment=ft.MainAxisAlignment.CENTER,
                                                     controls=[
                                                         ft.Icon(name=icon, color=ft.Colors.BLACK, size=20),
                                                         ft.Text(text, color=ft.Colors.BLACK, size=12)
                                                     ]
                                                 )
                                             )
                                             for icon, text in data_controls
                                            ]
                                     )
                                     )
                    ]
                ),
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(expand=True, bgcolor=self.dark_white,
                                     border_radius=15, padding=10,
                                     content= ft.Column(
                                         spacing=2,
                                         controls=[
                                             ft.Row(
                                                 alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                                                 controls=[
                                                     ft.Text("Domitorios", weight=ft.FontWeight.BOLD,
                                                             color=ft.Colors.BLACK),
                                                     ft.Switch(thumb_color= ft.Colors.BLACK,
                                                               active_track_color=ft.Colors.WHITE,
                                                               value=True,track_outline_color= ft.Colors.TRANSPARENT,
                                                               inactive_track_color= ft.Colors.WHITE,
                                                               )
                                                 ]),
                                                 ft.Text("Aspiradora robot", color= ft.Colors.with_opacity(0.5, ft.Colors.BLACK)),

                                                 ft.Container(
                                                     alignment=ft.alignment.center,
                                                     content=ft.Image(src=)
                                                 )
                                         ]
                                     )
                                     ),
                        ft.Container(expand=True, bgcolor=self.prey_color,
                                     border_radius=15,padding=10,
                                     )
                    ]
                )
            ]
        )

        self.colum_2 = ft.Column(
            expand=1, spacing=10,
            alignment= ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(expand=True, border_radius=15, padding=10,
                             gradient= ft.LinearGradient(
                                 rotation = math.radians(90),
                                 colors=[ft.Colors.with_opacity(0.5, self.prey_color),
                                         self.dark_white, self.yellow_color]
                             )
                ),
                ft.Container(
                    expand=True, border_radius=15, bgcolor=self.dark_white, padding=10,
                )
            ]
        )

        self.page.add(
            ft.Row(
                expand=True,
                controls=[
                    self.menu,
                    self.colum_1,
                    self.colum_2,
                ]
            )

        )
    

ft.app(target=SmartDomotic)