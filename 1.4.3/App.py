##Code made by Miguel Cornejo y Nicolas Arellano
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from ER_AFND_AFD import Thomson, Conversion
from Visualizacion import Visualizador, Visualizador_2
from V_Busqueda import VisualizadorBusqueda
import os

# Configuración de apariencia
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# Configuración de colores
FONDO_COLOR = "#656A6F"
COLOR_BOTON = "#8D8C8C"
COLOR_ENTRADA = "#dcdcdc"
COLOR_VISUAL = "#b0b0b0"

class ERApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Programa Conversión ER")
        self.geometry("1120x700")
        self.configure(bg=FONDO_COLOR)
        
        # Manejar eventos after
        self.eventos_after = []

        # Establecer el evento de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Establecer un icono personalizado
        icon_path = os.path.join(os.path.dirname(__file__), "Imagenes/logo.ico")
        self.iconbitmap(icon_path)

        # Cargar imágenes
        base_path = os.path.dirname(__file__)
        ab_path = os.path.join(base_path, "Imagenes/a-b.png")
        abc_path = os.path.join(base_path, "Imagenes/abc.png")
        viz_path = os.path.join(base_path, "Imagenes/visualizacion.png")

        self.ab_img = ImageTk.PhotoImage(Image.open(ab_path).resize((60, 60), Image.Resampling.LANCZOS))
        self.abc_img = ImageTk.PhotoImage(Image.open(abc_path).resize((60, 60), Image.Resampling.LANCZOS))
        self.viz_img = ImageTk.PhotoImage(Image.open(viz_path).resize((400, 400), Image.Resampling.LANCZOS))

        # Instancias de conversión y visualización
        self.thomson = Thomson()
        self.converter = Conversion()
        self.visualizer = Visualizador(self)
        self.visualizer_2 = Visualizador_2(self)
        self.visualizador_busqueda = VisualizadorBusqueda(self)

        self.er = ctk.StringVar()
        self.text_input = ctk.StringVar()
        self.afnd_creado = False
        self.afd_creado = False
        self.er_ingresada = False
        self.cadena_ingresada = False

        self.crear_widgets()

    def crear_widgets(self):
        # Crear frames para organizar la disposición
        frame_superior = ctk.CTkFrame(self, fg_color=FONDO_COLOR)
        frame_superior.grid(row=0, column=0, columnspan=3, padx=22, pady=10, sticky="ew")

        frame_entrada = ctk.CTkFrame(self, fg_color=FONDO_COLOR)
        frame_entrada.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        frame_salida = ctk.CTkFrame(self, fg_color=FONDO_COLOR)
        frame_salida.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        frame_derecha = ctk.CTkFrame(self, fg_color=FONDO_COLOR, width=400, height=400)
        frame_derecha.grid(row=1, column=2, rowspan=2, padx=20, pady=10, sticky="nsew")


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Botones de navegación - Configuración
        self.btn_intro_er = self.crear_boton(frame_superior, "Introducir ER", self.introducir_er)
        self.btn_er_afnd = self.crear_boton(frame_superior, "ER -> AFND", self.convertir_er_a_afnd)
        self.btn_afnd_afd = self.crear_boton(frame_superior, "AFND -> AFD", self.convertir_afnd_a_afd)
        self.btn_buscar_texto = self.crear_boton(frame_superior, "Buscar ER en Texto", self.buscar_ocurrencias)
        self.btn_visual_afnd = self.crear_boton(frame_superior, "Visualizar AFND", self.visualizar_afnd)
        self.btn_visual_afd = self.crear_boton(frame_superior, "Visualizar AFD", self.visualizar_afd)
        self.btn_visual_busqueda = self.crear_boton(frame_superior, "Visualizar Búsqueda", self.visualizar_busqueda)


        # Entrada para ER con imagen al lado
        self.er_image_label = ctk.CTkLabel(frame_entrada, image=self.ab_img, text="", bg_color=FONDO_COLOR)
        self.er_image_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.er_entry = self.crear_entrada(frame_entrada, self.er, "Colocar la Expresión Regular")
        
        # Entrada para buscar texto con imagen al lado
        self.text_image_label = ctk.CTkLabel(frame_entrada, image=self.abc_img, text="", bg_color=FONDO_COLOR)
        self.text_image_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.text_input_entry = ctk.CTkTextbox(frame_entrada, wrap="word", height=100, corner_radius=10, fg_color=COLOR_ENTRADA)
        self.text_input_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

        # Texto "Salidas de resultados"
        self.label_salida = ctk.CTkLabel(frame_salida, text="Salidas de resultados", font=("Helvetica", 20, "bold"), bg_color=FONDO_COLOR, text_color="white", anchor="center")
        self.label_salida.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.text_output = ctk.CTkTextbox(frame_salida, height=300, width=400, corner_radius=10, fg_color=COLOR_ENTRADA)
        self.text_output.grid(row=1, column=0, padx=10, pady=(40, 20), sticky="nsew")

        # Botón "Limpiar Resultados"
        self.btn_limpiar = ctk.CTkButton(frame_salida, text="Limpiar Resultados", command=self.limpiar_resultados, width=100, height=35, corner_radius=10, fg_color=COLOR_BOTON, hover_color="#a0a0a0")
        self.btn_limpiar.grid(row=1, column=0, padx=10, pady=0, sticky="n")

        # Título "Salida visual de Conversión" en el frame derecho
        self.label_salida_visual = ctk.CTkLabel(frame_derecha, text="Salida visual de Conversión", font=("Helvetica", 20, "bold"), bg_color=FONDO_COLOR, text_color="white", anchor="center")
        self.label_salida_visual.grid(row=0, column=0, padx=(130, 0), pady=10, sticky="n")

        # Área de visualización ajustada en el frame_derecha
        self.visual_area = ctk.CTkFrame(frame_derecha, fg_color=FONDO_COLOR)
        self.visual_area.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Botón de proceso de simulación
        self.btn_simulacion = ctk.CTkButton(frame_derecha, text=" ", width=150, height=40, corner_radius=10, command=self.simular_proceso, fg_color=FONDO_COLOR, hover_color="#a0a0a0")
        self.btn_simulacion.grid(row=3, column=0, padx=(100, 0), pady=20, sticky="n")

    def crear_boton(self, frame, texto, comando, ancho=120, altura=40):
        boton = ctk.CTkButton(frame, text=texto, width=ancho, height=altura, corner_radius=10, fg_color=COLOR_BOTON, hover_color="#a0a0a0", command=comando)
        boton.grid(row=0, column=len(frame.winfo_children()), padx=15, pady=10)
        return boton

    def crear_entrada(self, frame, variable, placeholder):
        entrada = ctk.CTkEntry(frame, textvariable=variable, placeholder_text=placeholder, width=300, height=50, corner_radius=10, fg_color=COLOR_ENTRADA)
        entrada.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="ew")
        return entrada

    def introducir_er(self):
        er = self.er.get().strip()
        if not er:
            self.text_output.insert("end", "No hay introducido una expresión regular aún.\n\n")
            return
        if "ñ" in er or "Ñ" in er:
            self.mostrar_error("Expresión regular inválida: contiene 'ñ' o 'Ñ'.")
            return
        # Validar expresiones regulares vacías o incorrectas
        if er in ["0", "Φ"] or any(sub in er for sub in ["0.0", "Φ.Φ", "Φ.0", "0.Φ"]):
            self.mostrar_error("Expresión regular vacía o cadena inválida.")
            return
        # Validar caracteres permitidos en la ER
        if any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ|.*_0Φ \n" for char in er):
            self.mostrar_error("Solo se permite letras mayúsculas o minúsculas y operadores válidos (*, |, ., _, 0, Φ).")
            return

        # Reemplazar combinaciones válidas para procesarlas
        er = er.replace("0|", "_|").replace("|0", "|_").replace("Φ|", "_|").replace("|Φ", "|_")
        er = er.replace("0", "").replace("Φ", "")

        # Manejar 0* y Φ* como aceptación de toda la cadena
        cadena = self.text_input_entry.get("1.0", "end").strip()
        if "0*" in er or "Φ*" in er:
            if not cadena:
                self.mostrar_error("Debe ingresar una cadena para continuar.")
            else:
                self.text_output.insert("end", "Acepta toda la cadena.\n\n")
            return

        # Validar cadena para contener únicamente letras y épsilon
        if any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_" for char in cadena.replace("-", "").replace("\n", "")):
            self.mostrar_error("La cadena debe contener solo letras mayúsculas, minúsculas, '-' con enter y '_'.")
            return

        self.er_ingresada = True
        self.cadena_ingresada = True
        self.text_output.insert("end", "Se introdujo la expresión regular correctamente.\n\n")
        self.afnd_creado = False
        self.afd_creado = False
        self.thomson = Thomson()
        self.thomson.sigma(cadena)  # Generar diccionario con letras y '_'

        
    def convertir_er_a_afnd(self):
        if not self.er_ingresada or not self.cadena_ingresada:
            self.mostrar_error("Debe ingresar la expresión regular y la cadena antes de convertir.")
            return

        if "0*" in self.er.get() or "Φ*" in self.er.get():
            self.mostrar_error("No se puede generar el Automata Finito No Determinista (AFND) es una ER vacía.")
            return

        self.afnd_creado = True
        self.thomson = Thomson()  # Crear nueva instancia
        self.thomson.sigma(self.text_input_entry.get("1.0", "end").strip())  # Actualizar diccionario
        self.thomson.AFND(self.er.get())  # Generar AFND
        self.mostrar_resultados_afnd()


    def visualizar_afnd(self):
        if not self.afnd_creado:
            self.mostrar_error("Debe generar el AFND primero.")
        else:
            self.visualizer.mostrar_grafo(
                self.thomson.delta, 
                "AFND",
                estado_inicial=self.thomson.K[0],
                estados_finales=[self.thomson.K[-1]]
            )

    def visualizar_afd(self):
        if not self.afd_creado:
            self.mostrar_error("Debe generar primero el AFD.")
        else:
            # Preparar los datos del AFD
            transiciones_preparadas, estados_finales_preparados, estado_inicial_preparado = self.visualizer_2.preparar_datos_afd(
                self.converter.delta_min,
                self.converter.estados_finales,
                self.converter.estado_inicial
            )

            # Mostrar el grafo del AFD usando Visualizador_2
            self.visualizer_2.mostrar_grafo(
                transiciones_preparadas,
                "AFD",
                estado_inicial=estado_inicial_preparado,
                estados_finales=estados_finales_preparados
            )

    def convertir_afnd_a_afd(self):
        if not self.afnd_creado:
            self.mostrar_error("Debe generar primero el AFND.")
            return

        if "0*" in self.er.get() or "Φ*" in self.er.get():
            self.mostrar_error("No se puede generar el Automata Finito Determinista (AFD) es una ER vacía.")
            return

        self.afd_creado = True
        self.converter = Conversion(self.thomson.diccionario)  # Pasar el diccionario
        self.converter.clausuras(self.thomson.K, self.thomson.delta)
        self.mostrar_resultados_afd()

    def mostrar_resultados_afnd(self):
        self.text_output.insert("end", "———————————————— AFND —————————————————\n")
        self.text_output.insert("end", f"Estado Inicial: {self.thomson.K[0]}\n")
        self.text_output.insert("end", f"Estado final: {self.thomson.K[-1]}\n")
        self.text_output.insert("end", f"Estados: {self.thomson.K}\n")
        self.text_output.insert("end", f"Transiciones: {self.thomson.delta}\n")
        self.text_output.insert("end", f"Diccionario: {self.thomson.diccionario}\n")

    def mostrar_resultados_afd(self):
        self.text_output.insert("end", "———————————————— AFD —————————————————\n")
        self.text_output.insert("end", f"Clausulas Epsilon: {self.converter.clausura_estado}\n")
        self.text_output.insert("end", f"Estado Inicial: {self.converter.estado_inicial}\n")  # Mostrar 'q0'
        self.text_output.insert("end", f"Estados Finales: {self.converter.estados_finales}\n")
        self.text_output.insert("end", f"Estados Totales: {self.converter.estados_totales}\n")
        self.text_output.insert("end", f"Transiciones: {self.converter.delta_min}\n")
        self.text_output.insert("end", f"Diccionario: {self.converter.diccionario}\n")

    def buscar_ocurrencias(self):
        er = self.er.get().strip()
        texto = self.text_input_entry.get("1.0", "end").strip()

        if not er or not texto:
            self.mostrar_error("Debe ingresar la ER y la cadena antes de buscar.")
            return

        # Remover `_` del texto para la búsqueda
        texto = texto.replace("_", "")

        # Validar caracteres permitidos en la cadena de búsqueda
        if any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\n-" for char in texto.replace("-", "").replace("\n", "")):
            self.mostrar_error("La cadena debe contener solo letras mayúsculas o minúsculas, '_', '-' con Enter")
            return

        # Reemplazar en la ER los casos permitidos
        er = er.replace("0|", "_|").replace("|0", "|_").replace("Φ|", "_|").replace("|Φ", "|_")
        er = er.replace("0", "").replace("Φ", "")

        ocurrencias = self._encontrar_ocurrencias(er, texto)
        self.text_output.insert("end", "—————————————— Ocurrencias ———————————————\n")
        if ocurrencias:
            for linea, posiciones in ocurrencias.items():
                posiciones_str = ', '.join([f'{pos[0]} "{pos[1]}"' for pos in posiciones])
                self.text_output.insert("end", f"Línea {linea}: {posiciones_str}\n")
        else:
            self.text_output.insert("end", "No se encontraron ocurrencias.\n")




    def _encontrar_ocurrencias(self, er, texto):
        ocurrencias = {}
        lineas = texto.split("\n")

        # Define una función para procesar patrones con operadores básicos
        def match_pattern(pattern, cadena):
            # Manejo de unión
            if "|" in pattern:
                subpatterns = pattern.split("|")
                return any(match_pattern(sub, cadena) for sub in subpatterns)

            # Manejo de concatenación explícita
            if "." in pattern:
                partes = pattern.split(".")
                idx = 0
                for parte in partes:
                    if idx < len(cadena) and cadena[idx:idx + len(parte)] == parte:
                        idx += len(parte)
                    else:
                        return False
                return idx == len(cadena)

            # Manejo de Kleene (*)
            if len(pattern) > 1 and pattern[1] == "*":
                return match_pattern(pattern[2:], cadena) or (cadena and pattern[0] == cadena[0] and match_pattern(pattern, cadena[1:]))

            # Concatenación implícita
            if not pattern:
                return not cadena

            # Manejo de épsilon
            if pattern[0] == "_":
                return match_pattern(pattern[1:], cadena)

            # Coincidencia literal
            return cadena and pattern[0] == cadena[0] and match_pattern(pattern[1:], cadena[1:])

        # Procesa cada línea para encontrar coincidencias
        for idx, linea in enumerate(lineas, start=1):
            coincidencias = []
            for inicio in range(len(linea)):
                for fin in range(inicio + 1, len(linea) + 1):
                    subcadena = linea[inicio:fin]
                    if subcadena and match_pattern(er, subcadena):
                        coincidencias.append((inicio + 1, subcadena))
            if coincidencias:
                ocurrencias[idx] = coincidencias

        return ocurrencias

    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)

    def visualizar_busqueda(self):
        if not self.afnd_creado or not self.afd_creado:
            self.mostrar_error("Debe generar primero el AFND y el AFD antes de visualizar la búsqueda.")
            return

        cadena = self.text_input_entry.get("1.0", "end").strip()
        if not cadena:
            self.mostrar_error("Debe ingresar una cadena para simular el proceso.")
            return

        # Visualiza cómo el AFD procesa la cadena
        self.visualizador_busqueda.mostrar_resultado_busqueda(
            self.converter.delta_min,  # Transiciones del AFD
            self.converter.estado_inicial,  # Estado inicial
            self.converter.estados_finales,  # Estados finales
            cadena,
            "Simulación de Búsqueda en el AFD"
        )


    def limpiar_resultados(self):
        self.text_output.delete("1.0", "end")
        self.afnd_creado = False
        self.afd_creado = False
        self.er_ingresada = False
        self.cadena_ingresada = False
        self.thomson = Thomson()
        self.converter = Conversion()
        # Limpiar el área de visualización
        for widget in self.visual_area.winfo_children():
            widget.destroy()

    def simular_proceso(self):
        self.text_output.insert("end", "Iniciando el proceso de simulación...\n")

    def programar_evento(self, delay, funcion):
        evento_id = self.after(delay, funcion)
        self.eventos_after.append(evento_id)

    def cancelar_eventos(self):
        for evento_id in self.eventos_after:
            try:
                self.after_cancel(evento_id)
            except Exception:
                pass
        self.eventos_after.clear()

    def on_closing(self):
        self.cancelar_eventos()
        self.destroy()

if __name__ == "__main__":
    app = ERApp()
    app.mainloop()

