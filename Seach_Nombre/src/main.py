import flet as ft
import os
import csv_handler
import datetime
import pandas as pd
import io

def main(page: ft.Page):
    page.title = "Buscador CSV"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 800
    page.padding = 50
    page.locale = "es-ES"

    # Fondo con degradado
    page.decoration = ft.BoxDecoration(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#8E2DE2", "#4A00E0"]
        )
    )
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE_PATH = os.path.join(BASE_DIR, "csv_datos", "usuarios.csv")

    # Leemos el texto como si fuera un archivo CSV real
    if os.path.exists(CSV_FILE_PATH):
        df = pd.read_csv(CSV_FILE_PATH)
        
        # 1. Mostrar los primeros 5
        print("--- Primeros registros ---")
        print(df.head())
        
        # 2. Algo de magia de Pandas (Estadísticas rápidas)
        if not df.empty and 'edad' in df.columns:
            print("\n--- Estadísticas de Edad ---")
            print(f"Edad promedio: {df['edad'].mean():.1f} años")
            print(f"Persona más joven: {df['edad'].min()} años")
            print(f"Persona más mayor: {df['edad'].max()} años")
            
            # 3. Filtrar: Mostrar solo los menores de 30 años
            print("\n--- Menores de 30 años ---")
            jovenes = df[df['edad'] < 30]
            print(jovenes[['nombre', 'apellido', 'edad']])

    # --- 1. Cargar datos del archivo .csv ---
    usuarios = [] # lista para almacenar los usuarios
    
    if os.path.exists(CSV_FILE_PATH):
        usuarios = csv_handler.load_csv(CSV_FILE_PATH)
    else:
        print("El archivo usuarios.csv no se encuentra.")

    # --- 2. Componentes de la Interfaz ---
    
    txt_search = ft.TextField(
        label="Buscar en base de datos",
        hint_text="Escribe un nombre...",
        prefix_icon=ft.Icons.SEARCH,
        autofocus=True,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        label_style=ft.TextStyle(color=ft.Colors.GREY_700),
    )

    # Definición de la tabla con estilos
    tabla_usuarios = ft.DataTable(
        width=1100,
        heading_row_color="#36304a",
        heading_row_height=60,
        data_row_min_height=50,
        divider_thickness=0,
        column_spacing=40,
        heading_text_style=ft.TextStyle(
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
            size=14,
        ),
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellido")),
            ft.DataColumn(ft.Text("Edad"), numeric=True),
            ft.DataColumn(ft.Text("Fecha de nacimiento")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )
    
    txt_mensaje = ft.Text("No se encontraron coincidencias", color="white", size=16, visible=False)

    # --- DatePickers ---
    def calculate_age(birth_date):
        if not birth_date:
            return "0"
        
        if isinstance(birth_date, str):
            try:
                birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
            except ValueError:
                return "0"

        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return str(age)

    def change_date_add(e):
        selected_date = date_picker_add.value
        if selected_date:
            txt_add_fecha_nacimiento.value = selected_date.strftime("%Y-%m-%d")
            lbl_add_edad_valor.value = calculate_age(selected_date)
            page.update()

    def change_date_edit(e):
        selected_date = date_picker_edit.value
        if selected_date:
            txt_edit_fecha_nacimiento.value = selected_date.strftime("%Y-%m-%d")
            lbl_edit_edad_valor.value = calculate_age(selected_date)
            page.update()

    date_picker_add = ft.DatePicker(
        on_change=change_date_add,
        first_date=datetime.datetime(1900, 1, 1),
        last_date=datetime.datetime.now(),
        date_picker_mode=ft.DatePickerMode.YEAR,
    )
    
    date_picker_edit = ft.DatePicker(
        on_change=change_date_edit,
        first_date=datetime.datetime(1900, 1, 1),
        last_date=datetime.datetime.now(),
        date_picker_mode=ft.DatePickerMode.YEAR,
    )

    page.overlay.append(date_picker_add)
    page.overlay.append(date_picker_edit)

    # --- 3. Lógica ---
    
    usuario_actual = [None]
    
    txt_edit_nombre = ft.TextField(label="Nombre")
    txt_edit_apellido = ft.TextField(label="Apellido")
    lbl_edit_edad_valor = ft.Text(size=16)
    txt_edit_fecha_nacimiento = ft.TextField(
        label="Fecha de nacimiento", 
        keyboard_type=ft.KeyboardType.DATETIME,
        suffix=ft.IconButton(
            icon=ft.Icons.CALENDAR_TODAY,
            on_click=lambda _: page.open(date_picker_edit)
        )
    )

    def abrir_editor(u):
        usuario_actual[0] = u
        txt_edit_nombre.value = u['nombre']
        txt_edit_apellido.value = u.get('apellido', '')
        # Calcular edad basada en la fecha de nacimiento para asegurar consistencia
        lbl_edit_edad_valor.value = calculate_age(u['fecha_nacimiento'])
        txt_edit_fecha_nacimiento.value = u['fecha_nacimiento']
        page.open(dlg_editor)

    def guardar_cambios(e):
        if usuario_actual[0]:
            usuario_actual[0]['nombre'] = txt_edit_nombre.value
            usuario_actual[0]['apellido'] = txt_edit_apellido.value
            usuario_actual[0]['fecha_nacimiento'] = txt_edit_fecha_nacimiento.value
            try:
                usuario_actual[0]['edad'] = int(lbl_edit_edad_valor.value)
            except ValueError:
                pass
            
            if csv_handler.save_csv(CSV_FILE_PATH, usuarios):
                page.snack_bar = ft.SnackBar(ft.Text("Cambios guardados correctamente"))
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al guardar cambios"))
                page.snack_bar.open = True

            page.close(dlg_editor)
            filtrar_usuarios(None)
            page.update()

    def cerrar_dialogo(e):
        page.close(dlg_editor)

    dlg_editor = ft.AlertDialog(
        title=ft.Text("Editar Usuario"),
        content=ft.Column([
            txt_edit_nombre,
            txt_edit_apellido,
            ft.Row([ft.Text("Edad:", weight="bold"), lbl_edit_edad_valor]),
            txt_edit_fecha_nacimiento
        ], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.TextButton("Guardar", on_click=guardar_cambios)
        ]
    )

    def eliminar_usuario(e):
        if usuario_actual[0]:
            usuarios.remove(usuario_actual[0])
            if csv_handler.save_csv(CSV_FILE_PATH, usuarios):
                page.snack_bar = ft.SnackBar(ft.Text("Usuario eliminado correctamente"))
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al eliminar usuario"))
                page.snack_bar.open = True
            
            page.close(dlg_confirm_delete)
            filtrar_usuarios(None)
            page.update()

    def cerrar_confirmacion(e):
        page.close(dlg_confirm_delete)

    dlg_confirm_delete = ft.AlertDialog(
        title=ft.Text("Confirmar eliminación"),
        content=ft.Text("¿Estás seguro de que deseas eliminar este usuario?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_confirmacion),
            ft.TextButton("Eliminar", on_click=eliminar_usuario, style=ft.ButtonStyle(color=ft.Colors.RED)),
        ]
    )

    def abrir_confirmacion_eliminar(u):
        usuario_actual[0] = u
        page.open(dlg_confirm_delete)

    # --- Dialogo Agregar Usuario ---
    txt_add_nombre = ft.TextField(label="Nombre")
    txt_add_apellido = ft.TextField(label="Apellido")
    lbl_add_edad_valor = ft.Text(size=16)
    txt_add_fecha_nacimiento = ft.TextField(
        label="Fecha de nacimiento", 
        keyboard_type=ft.KeyboardType.DATETIME,
        suffix=ft.IconButton(
            icon=ft.Icons.CALENDAR_TODAY,
            on_click=lambda _: page.open(date_picker_add)
        )
    )

    def cerrar_dialogo_agregar(e):
        page.close(dlg_agregar)

    def guardar_nuevo_usuario(e):
        if not txt_add_nombre.value or not lbl_add_edad_valor.value:
            page.snack_bar = ft.SnackBar(ft.Text("Nombre y Edad son obligatorios"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            nuevo_id = max([u['id'] for u in usuarios]) + 1 if usuarios else 1
            nuevo_usuario = {
                'id': nuevo_id,
                'nombre': txt_add_nombre.value,
                'apellido': txt_add_apellido.value,
                'edad': int(lbl_add_edad_valor.value),
                'fecha_nacimiento': txt_add_fecha_nacimiento.value
            }
            usuarios.append(nuevo_usuario)
            
            if csv_handler.save_csv(CSV_FILE_PATH, usuarios):
                page.snack_bar = ft.SnackBar(ft.Text("Usuario agregado correctamente"))
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al agregar usuario"))
                page.snack_bar.open = True
            
            page.close(dlg_agregar)
            filtrar_usuarios(None)
            page.update()
        except ValueError:
             page.snack_bar = ft.SnackBar(ft.Text("La edad debe ser un número"))
             page.snack_bar.open = True
             page.update()

    dlg_agregar = ft.AlertDialog(
        title=ft.Text("Agregar Usuario"),
        content=ft.Column([
            txt_add_nombre,
            txt_add_apellido,
            ft.Row([ft.Text("Edad:", weight="bold"), lbl_add_edad_valor]),
            txt_add_fecha_nacimiento
        ], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo_agregar),
            ft.TextButton("Guardar", on_click=guardar_nuevo_usuario)
        ]
    )

    def abrir_agregar_usuario(e):
        txt_add_nombre.value = ""
        txt_add_apellido.value = ""
        lbl_add_edad_valor.value = ""
        txt_add_fecha_nacimiento.value = ""
        page.open(dlg_agregar)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=abrir_agregar_usuario
    )

    def cargar_datos_tabla(lista_filtrada):
        tabla_usuarios.rows.clear()
        if not lista_filtrada:
            txt_mensaje.visible = True
            tabla_usuarios.visible = False
        else:
            txt_mensaje.visible = False
            tabla_usuarios.visible = True
            
            for i, u in enumerate(lista_filtrada):
                # Alternar colores de fila
                row_color = ft.Colors.WHITE if i % 2 == 0 else "#f5f5f5"
                btn_editar = ft.IconButton(
                    icon=ft.Icons.EDIT,
                    icon_color="grey",
                    tooltip="Editar usuario",
                    on_click=lambda e, usuario=u: abrir_editor(usuario)
                )

                btn_eliminar = ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color="red",
                    tooltip="Eliminar usuario",
                    on_click=lambda e, usuario=u: abrir_confirmacion_eliminar(usuario)
                )

                tabla_usuarios.rows.append(
                    ft.DataRow(
                        color=row_color,
                        cells=[
                            ft.DataCell(ft.Text(str(u['id']), color=ft.Colors.GREY_800)),
                            ft.DataCell(ft.Text(u['nombre'], color=ft.Colors.GREY_800)),
                            ft.DataCell(ft.Text(u.get('apellido', ''), color=ft.Colors.GREY_800)),
                            ft.DataCell(ft.Text(str(u['edad']), color=ft.Colors.GREY_800)), 
                            ft.DataCell(ft.Text(str(u['fecha_nacimiento']), color=ft.Colors.GREY_800)),
                            ft.DataCell(ft.Row([btn_editar, btn_eliminar], spacing=0)),
                        ]
                    )
                )
        page.update()

    def filtrar_usuarios(e):
        busqueda = txt_search.value.lower()
        resultado = list(
            filter(lambda u: u['nombre'].lower().startswith(busqueda) or u.get('apellido', '').lower().startswith(busqueda) or str(u.get('edad', '')).startswith(busqueda) or u.get('fecha_nacimiento', '').lower().startswith(busqueda), usuarios)
        )
        cargar_datos_tabla(resultado)

    txt_search.on_change = filtrar_usuarios

    # --- 4. Inicio ---
    cargar_datos_tabla(usuarios)

    # Contenedor principal estilo tarjeta
    contenedor_tabla = ft.Container(
        content=tabla_usuarios,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        padding=0,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 0),
        ),
    )
    cl = ft.Column(
        expand=True,
        controls=[
            ft.Text("Lectura desde CSV", size=30, weight="bold", color=ft.Container(bgcolor="#36304a"), text_align="center"),
            ft.Container(
                content=txt_search, 
                padding=ft.padding.only(bottom=20)
            ),
            ft.Column(
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,
                controls=[
                    txt_mensaje,
                    ft.Row([contenedor_tabla], scroll=ft.ScrollMode.ALWAYS),
                ]
            ),
            ft.Text("Version 1.3", size=10, weight="bold", color=ft.Colors.GREY_800, text_align="center")
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(cl)

if __name__ == '__main__':
    ft.app(target=main)