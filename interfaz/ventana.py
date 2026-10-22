import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from pathlib import Path

from procesos.frecuencias import calcular_frecuencias
from interfaz.componentes import crear_tarjeta
from procesos.proceso import leer_archivo
from procesos.analisis import analizar_encuesta
from graficas.graficos import generar_grafico


def iniciar_aplicacion():
    # Ventana principal
    ventana = ttk.Window(
        title="Estadística | Sistema de Análisis",
        themename="darkly"
    )

    ventana.state("zoomed")
    ventana.minsize(1000, 650)

    # Datos cargados actualmente
    datos_actuales = {
        "datos": None,
        "analisis": None,
        "tipos_variables": {}
    }

    # Contenedor general
    contenedor = ttk.Frame(ventana)
    contenedor.pack(fill=BOTH, expand=True)

    menu_lateral = ttk.Frame(
        contenedor,
        width=250,
        bootstyle="secondary"
    )
    menu_lateral.pack(side=LEFT, fill=Y)
    menu_lateral.pack_propagate(False)

    ttk.Label(
        menu_lateral,
        text="ESTADÍSTICA",
        font=("Segoe UI", 20, "bold"),
        bootstyle="inverse-secondary"
    ).pack(pady=(35, 5), padx=20)

    ttk.Label(
        menu_lateral,
        text="Sistema de análisis de datos",
        font=("Segoe UI", 10),
        bootstyle="inverse-secondary"
    ).pack(pady=(0, 35))

    ttk.Label(
        menu_lateral,
        text="MENÚ PRINCIPAL",
        font=("Segoe UI", 9, "bold"),
        bootstyle="inverse-secondary"
    ).pack(anchor=W, padx=25, pady=(5, 15))

    # =====================================
    # ÁREA PRINCIPAL
    # =====================================

    area_principal = ttk.Frame(
        contenedor,
        padding=30
    )
    area_principal.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )

    encabezado = ttk.Frame(area_principal)
    encabezado.pack(fill=X, pady=(0, 25))

    titulo_seccion = ttk.Label(
        encabezado,
        text="Panel de inicio",
        font=("Segoe UI", 26, "bold")
    )
    titulo_seccion.pack(side=LEFT)

    ttk.Label(
        encabezado,
        text="PROYECTO ESTADÍSTICO",
        font=("Segoe UI", 10, "bold"),
        bootstyle="info"
    ).pack(side=RIGHT, pady=10)

    # =====================================
    # PANEL DE BIENVENIDA
    # =====================================

    panel_bienvenida = ttk.Frame(
        area_principal,
        bootstyle="primary",
        padding=25
    )
    panel_bienvenida.pack(fill=X, pady=(0, 25))

    ttk.Label(
        panel_bienvenida,
        text="Bienvenido al sistema de análisis",
        font=("Segoe UI", 21, "bold"),
        bootstyle="inverse-primary"
    ).pack(anchor=W)

    ttk.Label(
        panel_bienvenida,
        text=(
            "Carga los datos de tu encuesta para generar tablas, "
            "gráficos y medidas estadísticas automáticamente."
        ),
        font=("Segoe UI", 12),
        bootstyle="inverse-primary",
        wraplength=900
    ).pack(anchor=W, pady=(10, 0))

    # =====================================
    # TARJETAS
    # =====================================

    panel_tarjetas = ttk.Frame(area_principal)
    panel_tarjetas.pack(fill=X, pady=(0, 25))

    tarjeta_encuestados, valor_encuestados = crear_tarjeta(
        panel_tarjetas,
        "Encuestados",
        "0",
        "Registros procesados"
    )
    tarjeta_encuestados.pack(
        side=LEFT,
        fill=BOTH,
        expand=True,
        padx=(0, 12)
    )

    tarjeta_variables, valor_variables = crear_tarjeta(
        panel_tarjetas,
        "Variables",
        "0",
        "Preguntas identificadas"
    )
    tarjeta_variables.pack(
        side=LEFT,
        fill=BOTH,
        expand=True,
        padx=(0, 12)
    )

    tarjeta_estado, valor_estado = crear_tarjeta(
        panel_tarjetas,
        "Estado del sistema",
        "Listo",
        "Esperando archivo"
    )
    tarjeta_estado.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )

    # =====================================
    # PANEL DE CARGA DE ARCHIVOS
    # =====================================

    panel_archivo = ttk.Frame(
        area_principal,
        padding=25,
        bootstyle="secondary"
    )
    panel_archivo.pack(fill=X, pady=(0, 20))

    ttk.Label(
        panel_archivo,
        text="Importar datos de la encuesta",
        font=("Segoe UI", 17, "bold"),
        bootstyle="inverse-secondary"
    ).pack(anchor=W, pady=(0, 10))

    ttk.Label(
        panel_archivo,
        text="Selecciona el archivo descargado desde Google Forms.",
        font=("Segoe UI", 11),
        bootstyle="inverse-secondary"
    ).pack(anchor=W, pady=(0, 15))

    etiqueta_archivo = ttk.Label(
        panel_archivo,
        text="Ningún archivo seleccionado",
        font=("Segoe UI", 10),
        bootstyle="inverse-secondary"
    )
    etiqueta_archivo.pack(anchor=W, pady=(5, 5))

    mensaje_archivo = ttk.Label(
        panel_archivo,
        text="Formatos permitidos: .xlsx y .csv",
        font=("Segoe UI", 10),
        bootstyle="inverse-secondary"
    )
    mensaje_archivo.pack(anchor=W, pady=(0, 10))

    # =====================================
    # PANEL DE VALIDACIÓN DE VARIABLES
    # =====================================

    panel_validacion = ttk.Labelframe(
        area_principal,
        text="Validación de preguntas y variables",
        padding=15
    )
    panel_validacion.pack(
        fill=BOTH,
        expand=True,
        pady=(0, 15)
    )

    ttk.Label(
        panel_validacion,
        text=(
            "Revisa las preguntas detectadas. Solo las variables "
            "que no se puedan clasificar automáticamente necesitan "
            "que indiques su tipo."
        ),
        wraplength=950,
        justify=LEFT
    ).pack(anchor=W, pady=(0, 12))

    columnas = (
        "pregunta",
        "detectado",
        "confirmado",
        "validas",
        "vacias",
        "diferentes"
    )

    tabla_variables = ttk.Treeview(
        panel_validacion,
        columns=columnas,
        show="headings",
        height=7
    )

    tabla_variables.heading("pregunta", text="Pregunta")
    tabla_variables.heading("detectado", text="Tipo detectado")
    tabla_variables.heading("confirmado", text="Tipo utilizado")
    tabla_variables.heading("validas", text="Respuestas válidas")
    tabla_variables.heading("vacias", text="Vacías")
    tabla_variables.heading("diferentes", text="Valores diferentes")

    tabla_variables.column("pregunta", width=280, minwidth=180)
    tabla_variables.column("detectado", width=130, anchor=CENTER)
    tabla_variables.column("confirmado", width=160, anchor=CENTER)
    tabla_variables.column("validas", width=110, anchor=CENTER)
    tabla_variables.column("vacias", width=80, anchor=CENTER)
    tabla_variables.column("diferentes", width=120, anchor=CENTER)

    barra_tabla = ttk.Scrollbar(
        panel_validacion,
        orient=VERTICAL,
        command=tabla_variables.yview
    )
    tabla_variables.configure(yscrollcommand=barra_tabla.set)

    tabla_variables.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )
    barra_tabla.pack(side=RIGHT, fill=Y)

    # =====================================
    # CONTROLES PARA CORREGIR CLASIFICACIÓN
    # =====================================

    panel_correccion = ttk.Frame(
        area_principal,
        padding=(0, 5, 0, 10)
    )
    panel_correccion.pack(fill=X)

    ttk.Label(
        panel_correccion,
        text="Tipo de variable para la pregunta seleccionada:"
    ).pack(anchor=W, pady=(0, 8))

    opciones_tipos = [
        "Cualitativa nominal",
        "Cualitativa ordinal",
        "Cuantitativa discreta",
        "Cuantitativa continua"
    ]

    selector_tipo = ttk.Combobox(
        panel_correccion,
        values=opciones_tipos,
        state="disabled",
        width=30
    )
    selector_tipo.pack(side=LEFT, padx=(0, 10))

    boton_guardar_tipo = ttk.Button(
        panel_correccion,
        text="Confirmar tipo",
        bootstyle="info",
        state="disabled"
    )
    boton_guardar_tipo.pack(side=LEFT)

    etiqueta_validacion = ttk.Label(
        panel_correccion,
        text="Carga una encuesta para comenzar.",
        wraplength=500
    )
    etiqueta_validacion.pack(
        side=LEFT,
        padx=15,
        fill=X,
        expand=True
    )

    # =====================================
    # FUNCIONES DE LA INTERFAZ
    # =====================================

    def actualizar_tabla(resultado):
        # Limpiar la tabla anterior
        for elemento in tabla_variables.get_children():
            tabla_variables.delete(elemento)

        for _, fila in resultado.iterrows():
            pregunta = str(fila["Pregunta"])
            tipo_detectado = str(fila["Tipo sugerido"])

            tipo_final = datos_actuales["tipos_variables"].get(
                pregunta,
                tipo_detectado
            )

            tabla_variables.insert(
                "",
                END,
                iid=pregunta,
                values=(
                    pregunta,
                    tipo_detectado,
                    tipo_final,
                    int(fila["Respuestas validas"]),
                    int(fila["Datos vacios"]),
                    int(fila["Valores diferentes"])
                )
            )

    def al_seleccionar_variable(event=None):
        seleccion = tabla_variables.selection()

        if not seleccion:
            selector_tipo.set("")
            selector_tipo.configure(state="disabled")
            boton_guardar_tipo.configure(state="disabled")
            etiqueta_validacion.config(
                text="Selecciona una pregunta de la tabla."
            )
            return

        pregunta = seleccion[0]
        fila = tabla_variables.item(pregunta, "values")

        tipo_detectado = fila[1]
        tipo_actual = fila[2]

        if tipo_detectado == "Revisar tipo":
            selector_tipo.configure(state="readonly")
            boton_guardar_tipo.configure(state="normal")

            if tipo_actual in opciones_tipos:
                selector_tipo.set(tipo_actual)
            else:
                selector_tipo.set("")

            etiqueta_validacion.config(
                text=(
                    "El sistema no pudo determinar el tipo. "
                    "Selecciona el correcto y pulsa Confirmar tipo."
                )
            )
        else:
            selector_tipo.set("")
            selector_tipo.configure(state="disabled")
            boton_guardar_tipo.configure(state="disabled")

            etiqueta_validacion.config(
                text=(
                    "El sistema clasificó esta variable como "
                    f"{tipo_detectado}. No requiere corrección "
                    "en esta etapa."
                )
            )

    def guardar_tipo():
        seleccion = tabla_variables.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selecciona una pregunta",
                "Primero selecciona una variable de la tabla.",
                parent=ventana
            )
            return

        pregunta = seleccion[0]
        nuevo_tipo = selector_tipo.get()

        if nuevo_tipo not in opciones_tipos:
            messagebox.showwarning(
                "Tipo no seleccionado",
                "Selecciona un tipo de variable válido.",
                parent=ventana
            )
            return

        datos_actuales["tipos_variables"][pregunta] = nuevo_tipo

        valores = list(tabla_variables.item(pregunta, "values"))
        valores[2] = nuevo_tipo
        tabla_variables.item(pregunta, values=valores)

        etiqueta_validacion.config(
            text=f"Tipo confirmado para: {pregunta}"
        )

        messagebox.showinfo(
            "Tipo confirmado",
            (
                f"Pregunta: {pregunta}\n"
                f"Tipo seleccionado: {nuevo_tipo}\n\n"
                "La selección se conservará mientras el programa "
                "esté abierto y los datos actuales sigan cargados."
            ),
            parent=ventana
        )

    tabla_variables.bind(
        "<<TreeviewSelect>>",
        al_seleccionar_variable
    )
    boton_guardar_tipo.configure(command=guardar_tipo)

    def cargar_archivo():
        ruta = filedialog.askopenfilename(
            title="Seleccionar encuesta",
            filetypes=[
                ("Archivos compatibles", "*.xlsx *.csv"),
                ("Archivos CSV", "*.csv"),
                ("Archivos Excel", "*.xlsx"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not ruta:
            return

        try:
            datos = leer_archivo(ruta)

            columnas_temporales = [
                columna for columna in datos.columns
                if str(columna).strip().casefold() in (
                    "marca temporal",
                    "marca de tiempo",
                    "timestamp"
                )
            ]

            datos = datos.drop(columns=columnas_temporales)

            resultado_analisis = analizar_encuesta(datos)

            datos_actuales["datos"] = datos
            datos_actuales["analisis"] = resultado_analisis
            datos_actuales["tipos_variables"] = {}

            actualizar_tabla(resultado_analisis)

            valor_encuestados.config(text=str(len(datos)))
            valor_variables.config(text=str(len(datos.columns)))
            valor_estado.config(text="Cargado")

            etiqueta_archivo.config(text=Path(ruta).name)

            mensaje_archivo.config(
                text=(
                    f"Archivo cargado: {len(datos)} registros y "
                    f"{len(datos.columns)} variables."
                ),
                bootstyle="success"
            )

            print("\nANÁLISIS DE LA ENCUESTA\n")
            print(resultado_analisis.to_string(index=False))

            cantidad_revision = int(
                (
                    resultado_analisis["Tipo sugerido"]
                    == "Revisar tipo"
                ).sum()
            )

            if cantidad_revision > 0:
                etiqueta_validacion.config(
                    text=(
                        f"Se encontraron {cantidad_revision} variables "
                        "que necesitan revisión manual."
                    )
                )
            else:
                etiqueta_validacion.config(
                    text=(
                        "El sistema clasificó automáticamente las "
                        "variables que pudo identificar."
                    )
                )

            messagebox.showinfo(
                "Archivo cargado",
                (
                    "El archivo se leyó correctamente.\n\n"
                    f"Registros: {len(datos)}\n"
                    f"Variables: {len(datos.columns)}\n"
                    f"Variables por revisar: {cantidad_revision}"
                ),
                parent=ventana
            )

        except Exception as error:
            messagebox.showerror(
                "Error al cargar archivo",
                f"No se pudo leer o analizar el archivo.\n\n{error}",
                parent=ventana
            )

    # Botón para cargar archivo
    ttk.Button(
        panel_archivo,
        text="Seleccionar archivo Excel o CSV",
        bootstyle="success",
        command=cargar_archivo
    ).pack(anchor=W, ipady=8)

    # =====================================
    # TABLAS DE FRECUENCIA
    # =====================================

    def mostrar_tablas_frecuencia():
        if datos_actuales["datos"] is None:
            messagebox.showwarning(
                "Sin datos",
                "Primero debes cargar una encuesta.",
                parent=ventana
            )
            return

        datos = datos_actuales["datos"]

        ventana_tabla = ttk.Toplevel(ventana)
        ventana_tabla.title("Tablas de frecuencia")
        ventana_tabla.geometry("950x600")
        ventana_tabla.minsize(750, 450)

        contenedor_tabla = ttk.Frame(
            ventana_tabla,
            padding=20
        )
        contenedor_tabla.pack(fill=BOTH, expand=True)

        ttk.Label(
            contenedor_tabla,
            text="Tablas de frecuencia",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor=W, pady=(0, 15))

        ttk.Label(
            contenedor_tabla,
            text="Selecciona la pregunta que deseas analizar:"
        ).pack(anchor=W)

        panel_selector = ttk.Frame(contenedor_tabla)
        panel_selector.pack(anchor=W, fill=X, pady=8)

        selector_pregunta = ttk.Combobox(
            panel_selector,
            values=list(datos.columns),
            state="readonly",
            width=50
        )
        selector_pregunta.pack(side=LEFT, padx=(0, 12))

        boton_generar = ttk.Button(
            panel_selector,
            text="GENERAR TABLA",
            bootstyle="success",
            command=lambda: generar_tabla(),
            width=22
        )
        boton_generar.pack(side=LEFT, ipady=5)

        opcion_agrupar = ttk.BooleanVar(
            master=ventana_tabla,
            value=False
        )

        check_agrupar = ttk.Checkbutton(
            contenedor_tabla,
            text="Agrupar datos numéricos en intervalos",
            variable=opcion_agrupar,
            bootstyle="round-toggle"
        )
        check_agrupar.pack(anchor=W, pady=8)

        ttk.Label(
            contenedor_tabla,
            text=(
                "Utiliza la agrupación cuando la variable cuantitativa "
                "tenga muchos valores diferentes."
            ),
            wraplength=850
        ).pack(anchor=W, pady=(0, 12))

        columnas_tabla = (
            "valor",
            "absoluta",
            "acumulada",
            "relativa",
            "porcentaje"
        )

        tabla = ttk.Treeview(
            contenedor_tabla,
            columns=columnas_tabla,
            show="headings",
            height=15
        )

        encabezados = {
            "valor": "Valor / intervalo",
            "absoluta": "Frecuencia absoluta",
            "acumulada": "Frecuencia acumulada",
            "relativa": "Frecuencia relativa",
            "porcentaje": "Porcentaje"
        }

        for columna in columnas_tabla:
            tabla.heading(
                columna,
                text=encabezados[columna]
            )
            tabla.column(
                columna,
                width=150,
                anchor=CENTER
            )

        tabla.column("valor", width=280, anchor=W)

        barra = ttk.Scrollbar(
            contenedor_tabla,
            orient=VERTICAL,
            command=tabla.yview
        )
        tabla.configure(yscrollcommand=barra.set)

        tabla.pack(
            side=LEFT,
            fill=BOTH,
            expand=True,
            pady=(5, 0)
        )
        barra.pack(side=LEFT, fill=Y, pady=(5, 0))

        resumen = ttk.Label(
            contenedor_tabla,
            text="Selecciona una pregunta y pulsa Generar tabla."
        )
        resumen.pack(anchor=W, pady=10)

        def generar_tabla():
            pregunta = selector_pregunta.get()

            if not pregunta:
                messagebox.showwarning(
                    "Selecciona una pregunta",
                    "Debes seleccionar una variable.",
                    parent=ventana_tabla
                )
                return

            analisis = datos_actuales["analisis"]
            fila = analisis[analisis["Pregunta"] == pregunta]

            tipo_sugerido = (
                str(fila.iloc[0]["Tipo sugerido"])
                if not fila.empty
                else "Revisar tipo"
            )

            tipo = datos_actuales["tipos_variables"].get(
                pregunta,
                tipo_sugerido
            )

            if tipo in ("Revisar tipo", "Sin datos"):
                messagebox.showwarning(
                    "Tipo pendiente",
                    (
                        "Esta variable necesita una clasificación "
                        "antes de generar su tabla. Selecciónala en "
                        "la sección de validación y confirma su tipo."
                    ),
                    parent=ventana_tabla
                )
                return

            es_cuantitativa = tipo in (
                "Cuantitativa",
                "Cuantitativa discreta",
                "Cuantitativa continua"
            )

            agrupar = opcion_agrupar.get()

            if agrupar and not es_cuantitativa:
                messagebox.showwarning(
                    "Agrupación no disponible",
                    "Solo puedes agrupar variables cuantitativas.",
                    parent=ventana_tabla
                )
                return

            try:
                resultado = calcular_frecuencias(
                    datos[pregunta],
                    agrupar=agrupar
                )

                for elemento in tabla.get_children():
                    tabla.delete(elemento)

                for _, registro in resultado.iterrows():
                    valor = str(registro.iloc[0])
                    absoluta = int(
                        registro["Frecuencia absoluta"]
                    )
                    acumulada = int(
                        registro["Frecuencia acumulada"]
                    )
                    relativa = float(
                        registro["Frecuencia relativa"]
                    )
                    porcentaje = float(
                        registro["Porcentaje"]
                    )

                    tabla.insert(
                        "",
                        END,
                        values=(
                            valor,
                            absoluta,
                            acumulada,
                            f"{relativa:.4f}",
                            f"{porcentaje:.2f}%"
                        )
                    )

                resumen.config(
                    text=(
                        f"Pregunta: {pregunta} | "
                        "Respuestas analizadas: "
                        f"{int(resultado['Frecuencia absoluta'].sum())}"
                    )
                )

            except Exception as error:
                messagebox.showerror(
                    "Error al calcular",
                    str(error),
                    parent=ventana_tabla
                )

        check_agrupar.configure(command=generar_tabla)

        if len(datos.columns) > 0:
            selector_pregunta.current(0)

    # =====================================
    # GRÁFICOS ESTADÍSTICOS
    # =====================================

    def mostrar_graficos():
        if datos_actuales["datos"] is None:
            messagebox.showwarning(
                "Sin datos",
                "Primero debes cargar una encuesta.",
                parent=ventana
            )
            return

        datos = datos_actuales["datos"]

        ventana_graficos = ttk.Toplevel(ventana)
        ventana_graficos.title("Gráficos estadísticos")
        ventana_graficos.geometry("900x650")
        ventana_graficos.minsize(700, 500)

        ttk.Label(
            ventana_graficos,
            text="Gráficos estadísticos",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        panel_selector = ttk.Frame(ventana_graficos)
        panel_selector.pack(fill=X, padx=20, pady=10)

        ttk.Label(
            panel_selector,
            text="Selecciona una pregunta:"
        ).pack(side=LEFT, padx=5)

        selector_grafico = ttk.Combobox(
            panel_selector,
            values=list(datos.columns),
            state="readonly",
            width=55
        )
        selector_grafico.pack(side=LEFT, padx=5)

        contenedor_grafico = ttk.Frame(ventana_graficos)
        contenedor_grafico.pack(
            fill=BOTH,
            expand=True,
            padx=20,
            pady=10
        )

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        lienzo = None

        def actualizar_grafico(event=None):
            nonlocal lienzo

            pregunta = selector_grafico.get()

            if not pregunta:
                return

            try:
                figura = generar_grafico(
                    datos[pregunta],
                    pregunta
                )

                if lienzo is not None:
                    lienzo.get_tk_widget().destroy()

                lienzo = FigureCanvasTkAgg(
                    figura,
                    master=contenedor_grafico
                )
                lienzo.draw()
                lienzo.get_tk_widget().pack(
                    fill=BOTH,
                    expand=True
                )

            except Exception as error:
                messagebox.showerror(
                    "Error al generar el gráfico",
                    str(error),
                    parent=ventana_graficos
                )

        selector_grafico.bind(
            "<<ComboboxSelected>>",
            actualizar_grafico
        )

        if len(datos.columns) > 0:
            selector_grafico.current(0)
            actualizar_grafico()

    # =====================================
    # NAVEGACIÓN DEL MENÚ
    # =====================================

    def mostrar_seccion(nombre):
        titulo_seccion.config(text=nombre)

        if nombre == "Inicio":
            mensaje_archivo.config(
                text="Panel principal del sistema."
            )

        elif nombre == "Cargar encuesta":
            mensaje_archivo.config(
                text="Selecciona un archivo Excel o CSV."
            )

        elif nombre == "Tablas de frecuencia":
            mostrar_tablas_frecuencia()

        elif nombre == "Gráficos estadísticos":
            mostrar_graficos()

        else:
            mensaje_archivo.config(
                text=(
                    f"Sección: {nombre}. "
                    "La funcionalidad se agregará en las siguientes etapas."
                )
            )

    # =====================================
    # BOTONES DEL MENÚ
    # =====================================

    opciones = [
        ("Inicio", "Inicio"),
        ("Cargar encuesta", "Cargar encuesta"),
        ("Tablas de frecuencia", "Tablas de frecuencia"),
        ("Gráficos estadísticos", "Gráficos estadísticos"),
        ("Medidas estadísticas", "Medidas estadísticas"),
        ("Informe de resultados", "Informe de resultados")
    ]

    for texto, seccion in opciones:
        ttk.Button(
            menu_lateral,
            text=texto,
            bootstyle="secondary",
            command=lambda s=seccion: mostrar_seccion(s)
        ).pack(
            fill=X,
            padx=15,
            pady=5,
            ipady=8
        )

    # Pie del menú
    ttk.Label(
        menu_lateral,
        text="PROYECTO FINAL\nEstadística I",
        font=("Segoe UI", 10),
        bootstyle="inverse-secondary",
        justify=CENTER
    ).pack(side=BOTTOM, pady=25)

    ventana.mainloop()
