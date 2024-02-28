from reader.Classes import *

carpeta = input("Ingrese la ruta completa de la carpeta: ")
palabra = input("Ingrese la palabra que desea buscar: ")
carpeta_obj = Carpeta(carpeta)
carpeta_obj.buscar_palabra(palabra)