# Detección y Representación de Navegaciones Agresivas en Buques

## Descripción
Este repositorio contiene el código de software desarrollado para el Trabajo Fin de Grado (TFG) titulado "Herramienta de geometría variable para la detección y representación de navegaciones agresivas en buques".
El proyecto implementa un modelo matemático dinámico basado en una elipse de seguridad de geometría variable para mejorar la evaluación del riesgo en la navegación marítima. A partir del procesamiento masivo de datos AIS, la herramienta identifica encuentros peligrosos en los que un buque invade el área de seguridad de otro.

## Estructura del Proyecto
* **`main.py`**: Script de ejecución principal que coordina la carga de configuración, la consulta a la base de datos y el cálculo de colisiones.
* **`config.json`**: Archivo de configuración con parámetros como rango de tiempo, factor de elipse y velocidad mínima.
* **`ellipse_size.py`**: Módulo matemático que calcula las dimensiones y orientación de la elipse de seguridad en función de la cinemática del buque.
* **`sql_request.py`**: Encargado de establecer la conexión con MySQL y extraer los datos AIS mediante ventanas temporales.
* **`test_collisions.py`**: Ejecuta las operaciones matriciales para comprobar si los centros de las elipses de los buques intersecan entre sí y exporta los resultados.
* **`map.py`**: Interfaz gráfica desarrollada con Tkinter para representar cartográficamente los encuentros detectados en el mapa.

## Flujo de trabajo
1. **Configuración**: Modificar los parámetros deseados (fechas, velocidad, rango temporal) en el archivo `config.json`.
2. **Cálculo de colisiones**: Ejecutar `main.py` para extraer los datos de la base de datos y procesar matemáticamente las elipses. Esto generará un archivo de texto con los resultados.
3. **Visualización**: Ejecutar el script del mapa pasando por argumento el archivo de texto generado. Por ejemplo: `python map.py "2020-01-01_13-45-00_2020-01-01_14-15-00_15.txt"`.

## Autores
* **Pablo Manuel Martín Isabel**
