Pasos a seguir:
Inicialización: Crea un repositorio público en GitHub con un archivo main.py para la ejecución del pipeline y una carpeta src/ para los módulos de lógica.
Extracción: Implementa una función que lea un dataset (puedes usar un archivo CSV público de Kaggle o similar) asegurando el uso correcto de tipos de datos para optimizar la memoria.
Transformación: Crea un script de limpieza que elimine duplicados, gestione valores nulos de forma justificada y normalice nombres de columnas. Separa esta lógica en una función independiente dentro de tu módulo de transformaciones.
Carga: Simula la carga de datos procesados exportando el resultado a un archivo Parquet, justificando por qué este formato es más eficiente para Machine Learning.
Documentación: El archivo README.md debe explicar cómo ejecutar el código y describir cada etapa del pipeline desarrollado.
