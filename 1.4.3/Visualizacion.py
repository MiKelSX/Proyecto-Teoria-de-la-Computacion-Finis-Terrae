##Code made by Miguel Cornejo, Benjamin Sepulveda
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import random

class Visualizador:
    def __init__(self, parent):
        self.parent = parent
        self.tamano_nodos = 300
        self.color_nodo_inicio = 'lightgreen'  # Color para el estado inicial
        self.color_nodo_final = 'yellow'  # Color para los estados finales
        self.color_nodo_intermedio = 'lightblue'  # Color para los nodos intermedios
        self.curvatura_bucle = 0.3  # Curvatura para bucles
        self.curvatura_arista = 0.3  # Curvatura para aristas entre nodos diferentes

    def mostrar_grafo(self, transiciones, titulo, estado_inicial, estados_finales):
        grafo = nx.DiGraph()
        etiquetas_aristas = defaultdict(list)

        # Agregar transiciones al grafo
        for inicio, etiqueta, fin in transiciones:
            etiqueta = 'ε' if etiqueta == '_' else etiqueta  # Usar 'ε' para transiciones epsilon
            etiquetas_aristas[(inicio, fin)].append(etiqueta)

        print("\n=== Depuración de transiciones ===")
        for (inicio, fin), etiquetas in etiquetas_aristas.items():
            etiqueta_combinada = ",".join(sorted(set(etiquetas)))
            print(f"Inicio: {inicio}, Fin: {fin}, Etiqueta: {etiqueta_combinada}")
            grafo.add_edge(inicio, fin, label=etiqueta_combinada)

        # Configuración de colores para los nodos
        colores_nodos = [
            self.color_nodo_inicio if nodo == estado_inicial else
            self.color_nodo_final if nodo in estados_finales else
            self.color_nodo_intermedio
            for nodo in grafo.nodes()
        ]

        # Crear la figura para el grafo
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_title(titulo, fontsize=14)

        # Posicionar los nodos
        posicion = self._calcular_posicion(grafo, estado_inicial, estados_finales)

        # Dibujar nodos
        nx.draw(
            grafo, posicion, with_labels=True,
            node_size=self.tamano_nodos,
            node_color=colores_nodos,
            font_size=9,
            font_weight='bold',
            ax=ax
        )

        # Dibujar aristas
        for (u, v), etiquetas in list(etiquetas_aristas.items()):
            # Evitar dibujar la línea central en transiciones bidireccionales
            if (v, u) in etiquetas_aristas:
                etiqueta_u_v = ",".join(sorted(set(etiquetas_aristas.pop((u, v), []))))
                etiqueta_v_u = ",".join(sorted(set(etiquetas_aristas.pop((v, u), []))))

                # Dibujar flecha de u -> v
                nx.draw_networkx_edges(
                    grafo, posicion,
                    edgelist=[(u, v)],
                    connectionstyle=f'arc3,rad={self.curvatura_arista}',
                    ax=ax
                )
                x1, y1 = posicion[u]
                x2, y2 = posicion[v]
                x_offset_uv = (x1 + x2) / 2
                y_offset_uv = (y1 + y2) / 2 + 0.3  # Ajuste vertical para u -> v
                ax.text(
                    x_offset_uv, y_offset_uv, etiqueta_u_v,
                    fontsize=7, ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='none', pad=0.2)
                )

                # Dibujar flecha de v -> u
                nx.draw_networkx_edges(
                    grafo, posicion,
                    edgelist=[(v, u)],
                    connectionstyle=f'arc3,rad={-self.curvatura_arista}',
                    ax=ax
                )
                x_offset_vu = (x1 + x2) / 2
                y_offset_vu = (y1 + y2) / 2 - 0.3  # Ajuste vertical para v -> u
                ax.text(
                    x_offset_vu, y_offset_vu, etiqueta_v_u,
                    fontsize=7, ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='none', pad=0.1)
                )

            else:
                # Dibujar flechas normales para transiciones no bidireccionales
                estilo = self._determinar_estilo_arista(grafo, u, v)
                etiqueta_combinada = ",".join(sorted(set(etiquetas)))  # Combinar etiquetas sin duplicados
                nx.draw_networkx_edges(
                    grafo, posicion,
                    edgelist=[(u, v)],
                    connectionstyle=estilo,
                    ax=ax
                )
                x1, y1 = posicion[u]
                x2, y2 = posicion[v]
                x_offset = (x1 + x2) / 2
                y_offset = (y1 + y2) / 2
                ax.text(
                    x_offset, y_offset, etiqueta_combinada,
                    fontsize=7, ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='none', pad=0.2)
                )

        # Ajustar márgenes y mostrar
        ax.margins(0)
        plt.tight_layout()
        # Limpiar área de visualización antes de dibujar
        for widget in self.parent.visual_area.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, self.parent.visual_area)
        canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        canvas.draw()

    def _calcular_posicion(self, grafo, estado_inicial, estados_finales):
        nodos = list(grafo.nodes())
        posicion = {}
        espacio_horizontal = 6  # Espacio entre niveles horizontales
        espacio_vertical = 3  # Espacio entre nodos en el mismo nivel

        # Posicionar estado inicial
        posicion[estado_inicial] = (0, 0)

        # Posicionar nodos intermedios
        intermedios = [nodo for nodo in nodos if nodo not in [estado_inicial] + estados_finales]
        finales = estados_finales

        # Distribuir intermedios horizontalmente en el centro
        num_intermedios = len(intermedios)
        x_centro = len(nodos) * espacio_horizontal // 2  # Centrar horizontalmente
        for idx, nodo in enumerate(intermedios):
            x_offset = random.uniform(-13, 13)  # Pequeña aleatoriedad horizontal
            y_offset = random.uniform(-idx, idx)  # Evitar superposición vertical
            posicion[nodo] = (x_centro + x_offset, -idx * espacio_vertical + y_offset)

        # Posicionar nodos finales
        for idx, nodo in enumerate(finales):
            posicion[nodo] = (len(nodos) * espacio_horizontal, 0)

        return posicion

    def _determinar_estilo_arista(self, grafo, nodo1, nodo2):
        if nodo1 == nodo2:
            return f'arc3,rad={self.curvatura_bucle}'
        elif grafo.has_edge(nodo2, nodo1):
            return f'arc3,rad={self.curvatura_arista}'
        else:
            return 'arc3,rad=0.0'

    def set_tamano_nodos(self, tamano):
        self.tamano_nodos = tamano

    def set_color_nodo_inicio(self, color):
        self.color_nodo_inicio = color

    def set_color_nodo_final(self, color):
        self.color_nodo_final = color

    def set_color_nodo_intermedio(self, color):
        self.color_nodo_intermedio = color

    def set_curvatura_bucle(self, curvatura):
        self.curvatura_bucle = curvatura

    def set_curvatura_arista(self, curvatura):
        self.curvatura_arista = curvatura


class Visualizador_2:
    def __init__(self, parent):
        self.parent = parent
        self.tamano_nodos = 300
        self.color_nodo_inicio = 'lightgreen'  # Color para el estado inicial
        self.color_nodo_siguiente = 'limegreen'  # Color para el nodo siguiente al inicial
        self.color_nodo_final = 'yellow'  # Color para los estados finales
        self.color_nodo_intermedio = 'lightblue'  # Color para los nodos intermedios
        self.curvatura_bucle = 0.3  # Curvatura para bucles
        self.curvatura_arista = 0.3  # Curvatura para aristas entre nodos diferentes

    def mostrar_grafo(self, transiciones, titulo, estado_inicial, estados_finales):
        grafo = nx.DiGraph()
        etiquetas_aristas = defaultdict(list)

        # Agregar transiciones al grafo
        for inicio, etiqueta, fin in transiciones:
            etiqueta = 'ε' if etiqueta == '_' else etiqueta  # Usar 'ε' para transiciones epsilon
            etiquetas_aristas[(tuple(inicio), tuple(fin))].append(etiqueta)

        # Asegurar que todos los estados están en el grafo
        for transicion in transiciones:
            grafo.add_node(tuple(transicion[0]))
            grafo.add_node(tuple(transicion[2]))

        # Identificar el nodo siguiente al inicial
        nodo_siguiente = None
        for transicion in transiciones:
            if tuple(transicion[0]) == tuple(estado_inicial):
                nodo_siguiente = tuple(transicion[2]) if isinstance(transicion[2], list) else transicion[2]
                break

        # Configuración de colores para los nodos
        colores_nodos = [
            self.color_nodo_inicio if nodo == tuple(estado_inicial) else
            self.color_nodo_siguiente if nodo == nodo_siguiente else
            self.color_nodo_final if nodo in [tuple(final) for final in estados_finales] else
            self.color_nodo_intermedio
            for nodo in grafo.nodes()
        ]

        # Crear la figura para el grafo
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_title(titulo, fontsize=14)

        # Posicionar los nodos
        posicion = self._calcular_posicion(grafo, tuple(estado_inicial), [tuple(final) for final in estados_finales])

        # Dibujar nodos
        nx.draw(
            grafo, posicion, with_labels=True,
            node_size=self.tamano_nodos,
            node_color=colores_nodos,
            font_size=8,
            font_weight='bold',
            ax=ax
        )

        # Dibujar aristas
        for (u, v), etiquetas in list(etiquetas_aristas.items()):
            estilo = self._determinar_estilo_arista(grafo, u, v)
            etiqueta_combinada = ",".join(sorted(set(etiquetas)))  # Combinar etiquetas sin duplicados
            nx.draw_networkx_edges(
                grafo, posicion,
                edgelist=[(u, v)],
                connectionstyle=estilo,
                ax=ax
            )
            x1, y1 = posicion[u]
            x2, y2 = posicion[v]
            x_offset = (x1 + x2) / 2
            y_offset = (y1 + y2) / 2 + 0.5 if u == v else (y1 + y2) / 2  # Etiquetas de bucles más arriba
            ax.text(
                x_offset, y_offset, etiqueta_combinada,
                fontsize=8, ha='center', va='center',
                bbox=dict(facecolor='white', edgecolor='none', pad=0.1)
            )

        # Ajustar márgenes y mostrar
        ax.margins(0.1)
        plt.tight_layout()

        # Limpiar área de visualización antes de dibujar
        for widget in self.parent.visual_area.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, self.parent.visual_area)
        canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        canvas.draw()

    def _calcular_posicion(self, grafo, estado_inicial, estados_finales):
        nodos = list(grafo.nodes())
        posicion = {}
        espacio_horizontal = 4  # Espacio horizontal entre nodos
        espacio_vertical = 4  # Espacio vertical entre nodos

        # Posicionar estado inicial
        posicion[estado_inicial] = (0, 0)

        # Posicionar nodos con aleatoriedad
        intermedios = [nodo for nodo in nodos if nodo not in [estado_inicial] + estados_finales]
        for nodo in intermedios:
            while True:
                x_random = random.uniform(-len(nodos), len(nodos)) * espacio_horizontal
                y_random = random.uniform(-len(nodos), len(nodos)) * espacio_vertical
                overlap = any(
                    (x_random, y_random) == posicion.get(n) for n in posicion
                )
                if not overlap:
                    posicion[nodo] = (x_random, y_random)
                    break

        # Posicionar nodos finales
        for idx, nodo in enumerate(estados_finales):
            posicion[nodo] = (len(nodos) * espacio_horizontal, idx * espacio_vertical)

        return posicion

    def _determinar_estilo_arista(self, grafo, nodo1, nodo2):
        if nodo1 == nodo2:
            return f'arc3,rad={self.curvatura_bucle}'
        elif grafo.has_edge(nodo2, nodo1):
            return f'arc3,rad={self.curvatura_arista}'
        else:
            return 'arc3,rad=0.1'

    def preparar_datos_afd(self, transiciones, estados_finales, estado_inicial):
        transiciones_preparadas = []
        for inicio, etiqueta, fin in transiciones:
            inicio_hashable = tuple(inicio) if isinstance(inicio, list) else inicio
            fin_hashable = tuple(fin) if isinstance(fin, list) else fin
            transiciones_preparadas.append((inicio_hashable, etiqueta, fin_hashable))

        estados_finales_preparados = [tuple(estado) if isinstance(estado, list) else estado for estado in estados_finales]
        estado_inicial_preparado = tuple(estado_inicial) if isinstance(estado_inicial, list) else estado_inicial

        return transiciones_preparadas, estados_finales_preparados, estado_inicial_preparado
