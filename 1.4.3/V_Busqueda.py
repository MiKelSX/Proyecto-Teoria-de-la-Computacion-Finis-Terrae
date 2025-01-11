##Code made by Miguel Cornejo
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


class VisualizadorBusqueda:
    def __init__(self, parent):
        self.parent = parent
        self.tamano_nodos = 300
        self.color_nodo_inicio = 'lightgreen'  # Color del estado inicial
        self.color_nodo_final = 'yellow'  # Color de los estados finales
        self.color_nodo_intermedio = 'lightblue'  # Color para estados intermedios
        self.color_transicion = 'gray'  # Color de las transiciones
        self.curvatura_bucle = 0.3  # Curvatura para bucles
        self.curvatura_arista = 0.3  # Curvatura para aristas entre nodos diferentes

    def mostrar_resultado_busqueda(self, transiciones, estado_inicial, estados_finales, cadenas, titulo):
        """
        Visualiza el AFD y muestra cómo se aceptan o rechazan las cadenas según la ER.
        """
        if not transiciones or not estado_inicial or not estados_finales:
            raise ValueError("Transiciones, estado inicial y estados finales deben estar definidos.")

        # Realizar la depuración de cadenas
        self._depurar_cadenas(transiciones, estado_inicial, estados_finales, cadenas)

        grafo = nx.DiGraph()

        # Crear el grafo del AFD a partir de las transiciones
        for origen, simbolo, destino in transiciones:
            origen = tuple(origen) if isinstance(origen, list) else origen
            destino = tuple(destino) if isinstance(destino, list) else destino
            grafo.add_edge(origen, destino, label=simbolo)

        # Configurar colores para los nodos
        colores_nodos = [
            self.color_nodo_inicio if nodo == tuple(estado_inicial) else
            self.color_nodo_final if nodo in [tuple(f) for f in estados_finales] else
            self.color_nodo_intermedio
            for nodo in grafo.nodes()
        ]

        # Crear la figura del grafo
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_title(titulo, fontsize=14)

        # Generar posiciones aleatorias para los nodos
        posicion = self._generar_posiciones(grafo, tuple(estado_inicial), [tuple(f) for f in estados_finales])

        # Dibujar nodos
        nx.draw(
            grafo, posicion,
            with_labels=True,
            node_size=self.tamano_nodos,
            node_color=colores_nodos,
            font_size=8,
            font_weight='bold',
            ax=ax
        )

        # Dibujar etiquetas de las aristas
        etiquetas_aristas = nx.get_edge_attributes(grafo, 'label')
        nx.draw_networkx_edge_labels(
            grafo, posicion,
            edge_labels=etiquetas_aristas,
            font_size=10,
            label_pos=0.5
        )

        # Dibujar aristas
        nx.draw_networkx_edges(
            grafo, posicion,
            connectionstyle=f'arc3,rad={self.curvatura_arista}',
            edge_color=self.color_transicion,
            arrowsize=20,
            ax=ax
        )

        # Limpiar área de visualización y mostrar el grafo en el canvas de tkinter
        for widget in self.parent.visual_area.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, self.parent.visual_area)
        canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        canvas.draw()

    def _depurar_cadenas(self, transiciones, estado_inicial, estados_finales, cadenas):
        """
        Depura las cadenas mostrando cuáles son aceptadas y cuáles no.
        """
        print("\n=== Depuración de cadenas ===")
        for cadena in cadenas:
            estado_actual = tuple(estado_inicial)
            for simbolo in cadena:
                estado_siguiente = self._obtener_siguiente_estado(transiciones, estado_actual, simbolo)
                if estado_siguiente:
                    estado_actual = estado_siguiente
                else:
                    print(f"Cadena: {cadena} -> Rechazada (transición inválida en '{simbolo}')")
                    break
            else:
                if estado_actual in [tuple(f) for f in estados_finales]:
                    print(f"Cadena: {cadena} -> Aceptada (estado final: {estado_actual})")
                else:
                    print(f"Cadena: {cadena} -> Rechazada (estado no final: {estado_actual})")

    def _obtener_siguiente_estado(self, transiciones, estado_actual, simbolo):
        """
        Obtiene el siguiente estado dado el estado actual y el símbolo de entrada.
        """
        for origen, etiqueta, destino in transiciones:
            origen = tuple(origen) if isinstance(origen, list) else origen
            destino = tuple(destino) if isinstance(destino, list) else destino
            if origen == estado_actual and etiqueta == simbolo:
                return destino
        return None

    def _generar_posiciones(self, grafo, estado_inicial, estados_finales):
        """
        Genera posiciones aleatorias para los nodos, con variación por niveles.
        """
        nodos = list(grafo.nodes())
        posicion = {}
        x_inicial = 0
        y_inicial = 0

        # Posicionar el nodo inicial
        posicion[estado_inicial] = (x_inicial, y_inicial)

        # Posicionar nodos finales en una línea horizontal
        x_offset = 3  # Separación horizontal entre nodos finales
        for idx, nodo in enumerate(estados_finales):
            posicion[nodo] = (x_inicial + (idx + 1) * x_offset, y_inicial)

        # Posicionar nodos intermedios aleatoriamente
        intermedios = [nodo for nodo in nodos if nodo not in [estado_inicial] + estados_finales]
        for nodo in intermedios:
            while True:
                x_random = random.uniform(-len(nodos), len(nodos)) * x_offset
                y_random = random.uniform(-len(nodos), len(nodos))
                if (x_random, y_random) not in posicion.values():
                    posicion[nodo] = (x_random, y_random)
                    break

        return posicion
