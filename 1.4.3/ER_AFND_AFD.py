class Thomson:
    def __init__(self):
        self.K = []  # Lista de estados
        self.delta = []  # Lista de transiciones
        self.lista_er = []  # Lista de la expresión regular
        self.estado = 0  # Contador para los estados
        self.primera_iteracion = True
        self.cadena = []
        self.diccionario = []

    def juntar(self, er, agregar=""):
        return er.replace("-", "") + agregar.replace("-", "")

    def juntar_cadena(self, cadena, agregar=""):
        return cadena.replace("-", "") + agregar.replace("-", "")

    def crear_estado(self):
        if self.primera_iteracion and self.estado != 0:
            self.estado -= 1
            estado = "q" + str(self.estado)
            self.primera_iteracion = False
            self.estado += 1
            return estado
        elif self.estado == 0:
            estado = "q" + str(self.estado)
            self.estado += 1
            self.primera_iteracion = False
            return estado
        else:
            estado = "q" + str(self.estado)
            self.estado += 1
            return estado

    def agregar_estado(self, *estados):
        for estado in estados:
            if estado not in self.K:
                self.K.append(estado)

    def simplificacion_er(self, er):
        resultado = ""
        i = 0
        while i < len(er):
            char = er[i]
            if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ*|.0Φ_":
                print(f"Carácter inválido '{char}' eliminado.")
                i += 1
                continue
            if char in "|*." and resultado and resultado[-1] in "|*.":
                print(f"Operador consecutivo '{resultado[-1]}{char}' corregido a '{char}'.")
                resultado = resultado[:-1] + char
            else:
                resultado += char
            i += 1
        if resultado.endswith("|") or resultado.endswith("."):
            print(f"Operador '{resultado[-1]}' al final eliminado.")
            resultado = resultado[:-1]
        return resultado or "Φ"

    def AFND(self, er):
        if "-" in er:
            er = self.juntar(er)
        q_inicio = self.crear_estado()
        for simbolo in sorted(self.diccionario):  # Orden alfabético del diccionario
            self.delta.append([q_inicio, simbolo, q_inicio])
        self.primera_iteracion = True
        er = self.simplificacion_er(er)
        self.lista_er = list(er)
        i = 0
        while i < len(self.lista_er):
            if self.lista_er[i] not in ["Φ", "0"]:
                if i + 1 < len(self.lista_er) and self.lista_er[i + 1] == "*":
                    q0, q1, q2, q3 = [self.crear_estado() for _ in range(4)]
                    self.delta.extend([
                        [q0, "_", q1],
                        [q1, self.lista_er[i], q2],
                        [q2, "_", q1],
                        [q2, "_", q3],
                        [q0, "_", q3]
                    ])
                    self.agregar_estado(q0, q1, q2, q3)
                    i += 2
                    self.primera_iteracion = True
                elif self.lista_er[i] == "_":
                    q0 = self.crear_estado()
                    q1 = self.crear_estado()
                    self.delta.append([q0, "_", q1])
                    self.agregar_estado(q0, q1)
                    i += 1
                    self.primera_iteracion = True
                elif i + 3 < len(self.lista_er) and self.lista_er[i + 1] == "|" and self.lista_er[i + 3] == "*":
                    q0, q1, q2, q3, q4, q5, q6, q7 = [self.crear_estado() for _ in range(8)]
                    self.delta.extend([
                        [q0, "_", q1],
                        [q1, self.lista_er[i], q2],
                        [q2, "_", q7],
                        [q0, "_", q3],
                        [q3, "_", q4],
                        [q4, self.lista_er[i + 2], q5],
                        [q5, "_", q4],
                        [q5, "_", q6],
                        [q3, "_", q6],
                        [q6, "_", q7]
                    ])
                    self.agregar_estado(q0, q1, q2, q3, q4, q5, q6, q7)
                    i += 4
                    self.primera_iteracion = True
                elif i + 1 < len(self.lista_er) and self.lista_er[i + 1] == "|":
                    q0, q1, q2, q3, q4, q5 = [self.crear_estado() for _ in range(6)]
                    self.delta.extend([
                        [q0, "_", q1],
                        [q1, self.lista_er[i], q2],
                        [q2, "_", q5],
                        [q0, "_", q3],
                        [q3, self.lista_er[i + 2], q4],
                        [q4, "_", q5]
                    ])
                    self.agregar_estado(q0, q1, q2, q3, q4, q5)
                    if i + 3 < len(self.lista_er) and self.lista_er[i + 3] == "|":
                        i += 2
                    else:
                        i += 3
                    self.primera_iteracion = True
                else:
                    q0 = self.crear_estado()
                    q1 = self.crear_estado()
                    self.delta.append([q0, self.lista_er[i], q1])
                    self.agregar_estado(q0, q1)
                    if i + 1 < len(self.lista_er) and self.lista_er[i + 1] == ".":
                        i += 2
                    else:
                        i += 1
                    self.primera_iteracion = True
            else:
                q_sumidero = self.crear_estado()
                for simbolo in self.diccionario:
                    self.delta.append([q_sumidero, simbolo, q_sumidero])
                i = len(self.lista_er)

    def sigma(self, cadena):
        # Limpiar cadena eliminando separadores innecesarios
        cadena_limpia = cadena.replace("-", "").replace("\n", "")

        # Validar caracteres en el diccionario (permitir '_' como epsilon)
        if any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_" for char in cadena_limpia):
            raise ValueError("El diccionario debe contener solo letras mayúsculas, minúsculas y '_'.")
        
        # Crear diccionario único y ordenado
        self.diccionario = sorted(set(cadena_limpia))  # Incluye '_'


class Conversion:
    def __init__(self, diccionario=None):
        self.clausura_estado = []
        self.delta_min = []
        self.estados_finales = []
        self.estados_totales = []
        self.diccionario = sorted(diccionario) if diccionario else []
        self.estado_inicial = "q0"  # Forzar el estado inicial a ser 'q0'

    def clausuras(self, estados, transiciones):
        for m in range(len(estados)):
            clausura_temporal = [estados[m]]
            for transicion in transiciones:
                if estados[m] == transicion[0] and transicion[1] == "_":
                    clausura_temporal.append(transicion[2])
            # Remueve duplicados y ordena para consistencia
            clausura_temporal = list(dict.fromkeys(clausura_temporal))
            if len(clausura_temporal) > 1:
                clausura_temporal.insert(1, "U")  # Inserta 'U' solo si hay transiciones epsilon
            self.clausura_estado.append(clausura_temporal)
        self.AFD(transiciones, estados)

    def AFD(self, transiciones, estados):
        estados_2 = [[self.estado_inicial]]
        diccionario = sorted([t[1] for t in transiciones if t[1] != "_"])
        procesados = set()
        self.delta_min = []
        estado_final_original = estados[-1]  # Estado final original del AFND

        while estados_2:
            estado_actual = estados_2.pop(0)
            estado_actual_tuple = tuple(sorted(estado_actual))
            if estado_actual_tuple in procesados:
                continue
            procesados.add(estado_actual_tuple)
            for c in diccionario:
                t = set()
                for estado in estado_actual:
                    for transicion in transiciones:
                        if estado == transicion[0] and transicion[1] == c:
                            destino = transicion[2]
                            for clausura in self.clausura_estado:
                                if clausura[0] == destino:
                                    t.update([s for s in clausura if s != "U"])
                t = list(t) or ["Φ"]
                t = sorted(t, key=lambda x: x if isinstance(x, str) else x[0])

                # Verificar si hay transiciones válidas y si la transición no es redundante
                if len(t) > 1 or (len(t) == 1 and t[0] != "Φ"):
                    sorted_estado_actual = sorted(estado_actual)
                    if [sorted_estado_actual, c, t] not in self.delta_min:
                        self.delta_min.append([sorted_estado_actual, c, t])
                    if t not in estados_2 and t != ["Φ"]:
                        estados_2.append(t)

            # Identificar estados finales
            if any(estado_final_original in sub if isinstance(sub, list) else estado_final_original in estado_actual for sub in estado_actual):
                sorted_estado_actual = sorted(estado_actual)
                if sorted_estado_actual not in self.estados_finales:
                    self.estados_finales.append(sorted_estado_actual)

        # Corregir Estados Totales
        self.estados_totales = []
        for estado in procesados:
            sorted_estado = sorted(list(estado))
            # Filtrar redundantes y estados poco útiles
            if len(sorted_estado) > 1 or sorted_estado == ['q0']:
                self.estados_totales.append(sorted_estado)
                
    def buscar_ocurrencias(self, texto):
        ocurrencias = {}
        lineas = texto.split("\n")

        for idx, linea in enumerate(lineas, start=1):
            coincidencias = []
            n = len(linea)
            for inicio in range(n):
                estado_actual = self.estado_inicial
                subcadena = ""
                for fin in range(inicio, n):
                    caracter = linea[fin]
                    subcadena += caracter
                    estado_siguiente = self._obtener_siguiente_estado(estado_actual, caracter)
                    if estado_siguiente:
                        estado_actual = estado_siguiente
                        if estado_actual in self.estados_finales:
                            # Registrar coincidencia con posición corregida
                            coincidencias.append(f"{inicio + 2} {subcadena}")
                    else:
                        break  # Salir si no hay transición válida
                
            # Ordenar y eliminar duplicados
            coincidencias = list(dict.fromkeys(coincidencias))
            if coincidencias:
                ocurrencias[idx] = coincidencias
        
        return ocurrencias

    def _obtener_siguiente_estado(self, estado_actual, caracter):
        for origen, simbolo, destino in self.delta_min:
            if origen == estado_actual and simbolo == caracter:
                return destino
        return None