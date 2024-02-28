import os
import re
import csv
import json
import xml.etree.ElementTree as ET

class Archivo:
    def __init__(self, ruta):
        self.ruta = ruta

    def contar_palabra(self, palabra):
        try:
            with open(self.ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
                cantidad = len(re.findall(r'\b{}\b'.format(palabra), contenido, re.IGNORECASE))
                return cantidad
        except Exception as e:
            print(f"No se pudo leer el archivo {self.ruta}: {e}")
            return 0

    def es_txt(self):
        return self.ruta.endswith('.txt')

    def es_csv(self):
        return self.ruta.endswith('.csv')

    def es_json(self):
        return self.ruta.endswith('.json')

    def es_xml(self):
        return self.ruta.endswith('.xml')

class Carpeta:
    def __init__(self, ruta):
        self.ruta = ruta

    def listar_archivos(self):
        archivos = []
        for archivo in os.listdir(self.ruta):
            ruta_completa = os.path.join(self.ruta, archivo)
            if os.path.isfile(ruta_completa):
                archivos.append(Archivo(ruta_completa))
        return archivos

    def buscar_palabra(self, palabra):
        if not os.path.exists(self.ruta):
            return print("La carpeta no existe.")
        total = 0
        archivos = self.listar_archivos()
        for archivo in archivos:
            cantidad = 0
            if archivo.es_txt():
                cantidad = archivo.contar_palabra(palabra)
            elif archivo.es_csv():
                with open(archivo.ruta, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    contenido = ' '.join([','.join(row) for row in reader])
                    cantidad = len(re.findall(r'\b{}\b'.format(palabra), contenido, re.IGNORECASE))
            elif archivo.es_json():
                with open(archivo.ruta, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    contenido = json.dumps(data)
                    cantidad = len(re.findall(r'\b{}\b'.format(palabra), contenido, re.IGNORECASE))
            elif archivo.es_xml():
                tree = ET.parse(archivo.ruta)
                root = tree.getroot()
                contenido = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
                cantidad = len(re.findall(r'\b{}\b'.format(palabra), contenido, re.IGNORECASE))
            else:
                print(f"No es posible leer el archivo {os.path.basename(archivo.ruta)}")
                continue
            print(f"En el archivo {os.path.basename(archivo.ruta)} la palabra '{palabra}' aparece {cantidad} veces.")
            total += cantidad
        print(f"\nEn total, la palabra '{palabra}' aparece {total} veces en todos los archivos de la carpeta.")
