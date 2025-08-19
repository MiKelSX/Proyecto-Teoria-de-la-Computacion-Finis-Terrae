# Proyecto Teoría de la Computación

<h3>Conversión de Expresiones Regulares a Autómatas Finito Determinista</h3>

Este repositorio contiene la implementación de un programa en Python que convierte expresiones regulares (ER) en Autómatas Finitos No Deterministas (AFND) utilizando el método de Thomson y luego determina estos AFND en Autómatas Finitos Deterministas (AFD). Además, el proyecto incluye la visualización gráfica de los autómatas generados y la detección de patrones en texto.

## 📋 Características

- **Conversión Automática:**
  - De ER a AFND (Método de Thomson).
  - De AFND a AFD.
- **Visualización Gráfica:** Representación interactiva de los autómatas generados.
- **Detección de Patrones:** Análisis de cadenas de texto para buscar coincidencias con expresiones regulares.
- **Cliente Interactivo:** Interfaz gráfica para la interacción y configuración del programa.

## 📑 Contenido del Proyecto

1. **Introducción:** Contexto y objetivos.
2. **Análisis del Problema:** Desafíos técnicos en la construcción y determinización de autómatas.
3. **Solución del Problema:** Implementación de los métodos y diseño modular del programa.
4. **Visualización y Ejemplos:** Ilustración gráfica del funcionamiento y resultados del programa.
5. **Conclusión:** Principales hallazgos y aplicaciones futuras.

## 🛠️ Tecnologías Utilizadas

- **Lenguaje de Programación:** Python 3.7 o superior.
- **Interfaz Gráfica:** CustomTkinter.
- **Visualización:** Graphviz para la representación gráfica de los autómatas.

## 🚀 Funcionalidades

### Métodos de Conversión
- **ER a AFND:** Uso del método de Thomson para construir estados y transiciones.
- **AFND a AFD:** Determinización basada en clausuras epsilon y transiciones mínimas.

### Cliente Interactivo
- Entrada de expresiones regulares y cadenas de texto.
- Visualización gráfica de autómatas.
- Búsqueda de patrones en texto con resultados detallados.

### Visualización
- Grafos interactivos para representar la estructura de AFND y AFD.
- Resaltado de estados iniciales, finales y transiciones.

## 📂 Estructura del Proyecto
├── 1.0.1 (Primera entrega)/ 
  
  │     -  -   └─── 
ER a AFND a AFD.py
  
├── 1.4.3/
  
  │     -  -  ├── App.py
  
  │     -  -  ├── ER_AFND_AFD.py
  
  │     -  -  ├── V_Busqueda.py
  
  │     -  -  ├── Visualizacion.py
  
  │     -  -  ├── Imagenes/
  
  │     -  -   │     -  -   ├── a-b.png
  
  │     -  -   │     -  -   ├── abc.png
  
  │     -  -   │     -  -   ├── logo.ico
  
  │     -  -   │     -  -   ├── logo.png
  
  │     -  -   │     -  -   └── visualizacion.png
  
  └── Proyecto Teoría de la Computación final.pdf

## 👥 Autores

- **Nicolás Arellano**
- **Miguel Cornejo**

## 🗓️ Fecha de Entrega
24 de noviembre de 2024

## ⚠️ Advertencia y Licencia

Este proyecto ha sido desarrollado con fines educativos para ilustrar conceptos y técnicas en el diseño de bases de datos. **No se autoriza el uso directo de este material para implementaciones reales sin una evaluación técnica y contextual adecuada.**

### Términos de Uso
1. Los autores no se hacen responsables por el uso indebido, modificaciones o riesgos asociados derivados de este proyecto.
2. Este repositorio está disponible públicamente para promover el aprendizaje. Si se utiliza como base para otros trabajos, **se debe dar el debido crédito a al autor o autores originales citando este repositorio como referencia.**
3. Cualquier implementación que derive de este código o diseño debe cumplir con los estándares éticos y legales aplicables en el contexto de uso.

Se recomienda estudiar el código y adaptar cualquier implementación según las necesidades específicas, siempre evaluando su viabilidad y seguridad.
