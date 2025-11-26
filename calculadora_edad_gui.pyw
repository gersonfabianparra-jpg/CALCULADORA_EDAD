import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date


# ---------------- LÓGICA DE NEGOCIO ---------------- #

def parse_fecha(fecha_str):
    """
    Intenta convertir un texto en una fecha.
    Soporta formatos:
    - DD-MM-YYYY
    - DD/MM/YYYY
    - YYYY-MM-DD
    """
    formatos = ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d")
    for fmt in formatos:
        try:
            return datetime.strptime(fecha_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(
        "Formato de fecha no válido.\nUsa por ejemplo 25-12-1995 o 25/12/1995."
    )


def calcular_edad(fecha_nac, hoy=None):
    """Calcula la edad en años cumplidos."""
    if hoy is None:
        hoy = date.today()

    edad = hoy.year - fecha_nac.year

    # Si aún no cumple años este año, restamos 1
    if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
        edad -= 1

    return edad


def dias_para_proximo_cumple(fecha_nac, hoy=None):
    """Calcula cuántos días faltan para el próximo cumpleaños."""
    if hoy is None:
        hoy = date.today()

    proximo_cumple = date(hoy.year, fecha_nac.month, fecha_nac.day)

    # Si el cumpleaños de este año ya pasó, usamos el año siguiente
    if proximo_cumple < hoy:
        proximo_cumple = date(hoy.year + 1, fecha_nac.month, fecha_nac.day)

    diferencia = proximo_cumple - hoy
    return diferencia.days


def dia_semana(fecha_nac):
    """Devuelve el día de la semana en español para la fecha de nacimiento."""
    dias = [
        "lunes", "martes", "miércoles",
        "jueves", "viernes", "sábado", "domingo"
    ]
    return dias[fecha_nac.weekday()]


# ---------------- INTERFAZ GRÁFICA (UI) ---------------- #

def crear_ventana():
    root = tk.Tk()
    root.title("Calculadora de Edad y Gestión de Personas")
    root.geometry("900x500")
    root.minsize(850, 450)

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # --------- Definición de temas (colores) --------- #
    THEMES = {
        "Azul": {
            "bg_main": "#0B1220",
            "fg_main": "#FFFFFF",
            "fg_hint": "#A0AEC0",
            "bg_widget": "#111827",
            "bg_button": "#1E293B",
            "bg_button_accent": "#2563EB",
            "border_color": "#374151",
        },
        "Verde": {
            "bg_main": "#022C22",
            "fg_main": "#ECFDF5",
            "fg_hint": "#6EE7B7",
            "bg_widget": "#064E3B",
            "bg_button": "#065F46",
            "bg_button_accent": "#10B981",
            "border_color": "#047857",
        },
        "Morado": {
            "bg_main": "#1F1029",
            "fg_main": "#F5F3FF",
            "fg_hint": "#A855F7",
            "bg_widget": "#2D0A3F",
            "bg_button": "#4C1D95",
            "bg_button_accent": "#7C3AED",
            "border_color": "#6D28D9",
        },
    }

    # ---------- Frame principal con grid flexible ---------- #
    main_frame = ttk.Frame(root, padding=15)
    main_frame.grid(row=0, column=0, sticky="nsew")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    main_frame.columnconfigure(0, weight=0)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(0, weight=0)
    main_frame.rowconfigure(1, weight=1)

    # ---------- Título global + selector de tema ---------- #
    header_frame = ttk.Frame(main_frame)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    header_frame.columnconfigure(0, weight=1)
    header_frame.columnconfigure(1, weight=0)

    titulo = ttk.Label(
        header_frame,
        text="Calculadora de Edad y Gestión de Personas",
        font=("Segoe UI", 18, "bold")
    )
    titulo.grid(row=0, column=0, sticky="w")

    tema_frame = ttk.Frame(header_frame)
    tema_frame.grid(row=0, column=1, sticky="e")

    lbl_tema = ttk.Label(tema_frame, text="Tema:")
    lbl_tema.grid(row=0, column=0, padx=(0, 5))

    combo_tema = ttk.Combobox(
        tema_frame,
        values=list(THEMES.keys()),
        state="readonly",
        width=12
    )
    combo_tema.grid(row=0, column=1)
    combo_tema.set("Azul")  # Tema por defecto

    # ---------- Sección formulario de entrada ---------- #
    form_frame = ttk.Labelframe(
        main_frame,
        text="Datos de la persona",
        padding=10,
    )
    form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

    lbl_nombre = ttk.Label(form_frame, text="Nombre completo:")
    lbl_nombre.grid(row=0, column=0, sticky="e", pady=5, padx=(0, 5))
    entry_nombre = ttk.Entry(form_frame, width=30)
    entry_nombre.grid(row=0, column=1, sticky="w", pady=5)

    lbl_direccion = ttk.Label(form_frame, text="Dirección:")
    lbl_direccion.grid(row=1, column=0, sticky="e", pady=5, padx=(0, 5))
    entry_direccion = ttk.Entry(form_frame, width=30)
    entry_direccion.grid(row=1, column=1, sticky="w", pady=5)

    lbl_fecha = ttk.Label(form_frame, text="Fecha de nacimiento:")
    lbl_fecha.grid(row=2, column=0, sticky="e", pady=5, padx=(0, 5))
    entry_fecha = ttk.Entry(form_frame, width=15)
    entry_fecha.grid(row=2, column=1, sticky="w", pady=5)

    hint_fecha = ttk.Label(
        form_frame,
        text="Formatos: DD-MM-YYYY, DD/MM/YYYY o YYYY-MM-DD"
    )
    hint_fecha.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 5))

    # ---------- Sección resultados ---------- #
    result_frame = ttk.Labelframe(
        form_frame,
        text="Resultado del cálculo",
        padding=10,
    )
    result_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

    lbl_result_edad = ttk.Label(result_frame, text="Edad: -")
    lbl_result_edad.grid(row=0, column=0, columnspan=2, sticky="w", pady=2)

    lbl_result_dia = ttk.Label(result_frame, text="Día en que nació: -")
    lbl_result_dia.grid(row=1, column=0, columnspan=2, sticky="w", pady=2)

    lbl_result_faltan = ttk.Label(
        result_frame,
        text="Días para el próximo cumpleaños: -"
    )
    lbl_result_faltan.grid(row=2, column=0, columnspan=2, sticky="w", pady=2)

    lbl_result_fecha = ttk.Label(result_frame, text="Fecha normalizada: -")
    lbl_result_fecha.grid(row=3, column=0, columnspan=2, sticky="w", pady=2)

    # Botones
    btn_calcular = ttk.Button(
        form_frame,
        text="Calcular y agregar persona"
    )
    btn_calcular.grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky="ew")

    btn_limpiar = ttk.Button(
        form_frame,
        text="Limpiar formulario"
    )
    btn_limpiar.grid(row=6, column=0, columnspan=2, pady=(5, 0), sticky="ew")

    # ---------- Sección tabla de personas ---------- #
    list_frame = ttk.Labelframe(
        main_frame,
        text="Personas registradas (memoria)",
        padding=10,
    )
    list_frame.grid(row=1, column=1, sticky="nsew")

    main_frame.rowconfigure(1, weight=1)
    list_frame.rowconfigure(0, weight=1)
    list_frame.columnconfigure(0, weight=1)

    columns = ("nombre", "edad", "fecha_nac", "direccion", "dias_cumple")

    tree = ttk.Treeview(
        list_frame,
        columns=columns,
        show="headings",
        height=15,
    )

    tree.heading("nombre", text="Nombre")
    tree.heading("edad", text="Edad")
    tree.heading("fecha_nac", text="Fecha Nac.")
    tree.heading("direccion", text="Dirección")
    tree.heading("dias_cumple", text="Días p/cumple")

    tree.column("nombre", width=160, anchor="w")
    tree.column("edad", width=50, anchor="center")
    tree.column("fecha_nac", width=90, anchor="center")
    tree.column("direccion", width=200, anchor="w")
    tree.column("dias_cumple", width=100, anchor="center")

    scroll_y = ttk.Scrollbar(
        list_frame,
        orient="vertical",
        command=tree.yview,
    )
    tree.configure(yscrollcommand=scroll_y.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")

    personas_registradas = []

    # ---------- FUNCIÓN PARA APLICAR TEMA ---------- #

    def aplicar_tema(nombre_tema: str):
        colors = THEMES.get(nombre_tema, THEMES["Azul"])

        bg_main = colors["bg_main"]
        fg_main = colors["fg_main"]
        fg_hint = colors["fg_hint"]
        bg_widget = colors["bg_widget"]
        bg_button = colors["bg_button"]
        bg_button_accent = colors["bg_button_accent"]
        border_color = colors["border_color"]

        # Fondo de la ventana principal
        root.configure(bg=bg_main)

        # Estilos generales
        style.configure("TFrame", background=bg_main)
        style.configure("TLabelframe", background=bg_main, foreground=fg_main)
        style.configure("TLabelframe.Label", background=bg_main, foreground=fg_main)

        style.configure("Title.TLabel",
                        font=("Segoe UI", 18, "bold"),
                        background=bg_main,
                        foreground=fg_main)

        style.configure("TLabel",
                        font=("Segoe UI", 10),
                        background=bg_main,
                        foreground=fg_main)

        # Labels especiales (hint)
        hint_fecha.configure(foreground=fg_hint, background=bg_main)

        # Botones
        style.configure("TButton",
                        font=("Segoe UI", 10),
                        background=bg_button,
                        foreground=fg_main)
        style.map("TButton",
                  background=[("active", bg_button_accent)])

        style.configure("Accent.TButton",
                        font=("Segoe UI", 10, "bold"),
                        background=bg_button_accent,
                        foreground=fg_main)
        style.map("Accent.TButton",
                  background=[("active", border_color)])

        # Treeview
        style.configure(
            "Treeview",
            background=bg_widget,
            foreground=fg_main,
            fieldbackground=bg_widget,
            bordercolor=border_color,
            rowheight=22
        )
        style.configure(
            "Treeview.Heading",
            background=bg_main,
            foreground=fg_main,
            bordercolor=border_color
        )

        # Scrollbar (según soporte)
        style.configure("Vertical.TScrollbar",
                        background=bg_main,
                        troughcolor=bg_widget,
                        bordercolor=border_color)

    # Botón principal con estilo de acento
    btn_calcular.configure(style="Accent.TButton")

    # Aplicar tema inicial
    aplicar_tema("Azul")

    # Cambio de tema desde el combobox
    def on_tema_cambiado(event):
        aplicar_tema(combo_tema.get())

    combo_tema.bind("<<ComboboxSelected>>", on_tema_cambiado)

    # ---------- Funciones internas de la UI ---------- #

    def limpiar_formulario():
        entry_nombre.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)
        lbl_result_edad.config(text="Edad: -")
        lbl_result_dia.config(text="Día en que nació: -")
        lbl_result_faltan.config(
            text="Días para el próximo cumpleaños: -"
        )
        lbl_result_fecha.config(text="Fecha normalizada: -")
        entry_nombre.focus()

    def calcular_y_agregar():
        nombre = entry_nombre.get().strip()
        direccion = entry_direccion.get().strip()
        fecha_str = entry_fecha.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Dato faltante",
                "Por favor, ingresa el nombre de la persona."
            )
            return

        if not fecha_str:
            messagebox.showwarning(
                "Dato faltante",
                "Por favor, ingresa la fecha de nacimiento."
            )
            return

        try:
            fecha_nac = parse_fecha(fecha_str)
        except ValueError as e:
            messagebox.showerror("Fecha inválida", str(e))
            return

        hoy = date.today()
        edad = calcular_edad(fecha_nac, hoy)
        dias_faltan = dias_para_proximo_cumple(fecha_nac, hoy)
        dia_naciste = dia_semana(fecha_nac)

        # Actualizar resultados en pantalla
        lbl_result_edad.config(text=f"Edad: {edad} años")
        lbl_result_dia.config(text=f"Día en que nació: {dia_naciste}")
        lbl_result_faltan.config(
            text=f"Días para el próximo cumpleaños: {dias_faltan}"
        )
        lbl_result_fecha.config(
            text=f"Fecha normalizada: {fecha_nac.strftime('%d-%m-%Y')}"
        )

        # Guardar en la estructura en memoria
        persona = {
            "nombre": nombre,
            "edad": edad,
            "fecha_nac": fecha_nac,
            "direccion": direccion,
            "dias_cumple": dias_faltan,
        }
        personas_registradas.append(persona)

        # Insertar en la tabla
        tree.insert(
            "",
            tk.END,
            values=(
                persona["nombre"],
                persona["edad"],
                persona["fecha_nac"].strftime("%d-%m-%Y"),
                persona["direccion"],
                persona["dias_cumple"],
            ),
        )

        # Mensaje especial si es cumpleaños
        if dias_faltan == 0:
            messagebox.showinfo(
                "¡Felicidades! 🎉",
                f"¡Hoy es el cumpleaños de {nombre}!"
            )

    # Asociar funciones a botones
    btn_calcular.config(command=calcular_y_agregar)
    btn_limpiar.config(command=limpiar_formulario)

    # Enter ejecuta calcular_y_agregar
    root.bind("<Return>", lambda event: calcular_y_agregar())

    # Foco inicial
    entry_nombre.focus()

    root.mainloop()


if __name__ == "__main__":
    crear_ventana()
