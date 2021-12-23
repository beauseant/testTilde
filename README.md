# testTilde

Script de python que se encarga de probar la API de Neural Machine Translation Systems. Para ello se utiliza el corpus de Semantic Scholar de la siguiente manera:

1) El script carga de forma aleatoria el número solicitado de archivos de SC, y de esos archivos, también de forma aleatoria, carga un número de artículos de manera aleatoria también.
2) Lanza contra la API el abstract de esos artículos y solicita la traducción de inglés a español y graba el resultado en el archivo indicado como parámetro.

El script permite pasar, además, un número de hilos de ejecución para usarlo en modo paralelo. Al realizarse todo en la misma máquina y usarse python no se producen muchas mejoras.

### Uso:

1) Debe generarse un fichero de texto llamado token que contenga solamente el token provisto por la empresa.
2) Para lanzarlo: python3 main.py -t scolar -p /export/data_ml4ds/FuentesDatos/Scholar2019/scolar/ -n 1  -na 500 -th 1 -o data/output/prueba_prueba

El comando anterior indica que queremos hacer las pruebas con scolar (es la única forma disponible ahora mismo), con -p se le indica la ruta donde se encuentra el corpus, con n el número de archivos json del corpus que usará, con na el número de artículos a tomar de cada corpus, con th el número de hilos y con o donde se grabará la salida.




