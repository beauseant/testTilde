import glob
import argparse
import random
import json
import re
import multiprocessing
import sys
import time


sys.path.append('./includes')
from Rosetta import Rosetta


def readJson (f):

    response = f.read()
    response = response.replace('\n', '')
    response = response.replace('}{', '},{')
    response = "[" + response + "]" 
    return json.loads(response)



def loadFile (file):
    listAbstract = list ()
    try:
        with open( file ) as f:
            #data = list(filter (lambda articulo : articulo['paperAbstract'] != '', readJson (f)[:12000]))
            data = list(filter (lambda articulo : articulo['paperAbstract'] != '', readJson (f)))
            listAbstract = random.sample (data, argus.abstract)
            print ('finish with %s' % file)
    except Exception as E:
        print ('error leyendo %s, %s' % file, str(E))

    return listAbstract

def translate (articulo ):
    myR = Rosetta (token = 'u-fc6f1588-4dc0-4358-aa48-106749f327af', translate = 'English - Spanish (NMT) Lynx')
    
    if myR.connect()[0] == 200:
        text = articulo['paperAbstract']
        textTrans = myR.translate (text)
    else:
        print ('error')

    return [articulo['paperAbstract'], textTrans[1], len(re.findall(r'\w+', articulo['paperAbstract']))]




if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Script en python para pasar openaire a psql')
    parser.add_argument('-t','--type', help='Tipo de textos a probar, scolar', required=True, choices=['scolar'])
    parser.add_argument('-p','--path', help='Ruta con los ficheros', required=True )
    parser.add_argument('-n','--numero', help='Número de archivos a procesar', required=True, type=int)
    parser.add_argument('-na','--abstract', help='Número de abstract de cada archivo a procesar', required=True, type=int)
    parser.add_argument('-th','--threads', required=True, type=int, help='hilos de ejecución a lanzar,1 secuencial')
    parser.add_argument('-o','--output', required=True, type=str, help='directorio de salida')
    argus = parser.parse_args()

    

    if argus.type == 'scolar':

        #creamos una lista con todos los ficheros de scolar:
        scopusFiles = glob.glob( argus.path + '/*corpus*' )
        #tomamos una muestra aleatoria sin repetirlos:
        selectScopusFiles = random.sample( scopusFiles , k=argus.numero)


        listAbstract = list()

        with multiprocessing.Pool(processes= int(argus.threads)) as pool:
            listAbstract = pool.starmap(loadFile, zip(selectScopusFiles))
        listAbstract = [item for sublist in listAbstract for item in sublist]


        numWords = map (lambda articulo : len(re.findall(r'\w+', articulo['paperAbstract'])), listAbstract)
        print ('número de articulos procesados: %s' % len (listAbstract))
        print ('número de palabras totales: %s' % sum(numWords))


    start_time = time.time()
    with multiprocessing.Pool(processes= int(argus.threads)) as pool:
        results = pool.starmap(translate, zip(listAbstract))
    end_time = time.time()

    for i, res in enumerate (results):
        file = argus.output + '/' + str(i)
        with open( file, 'w') as f:
            f.write (res[0])
            f.write('\n ---------------------------------------- \n')
            f.write (res[1])
            f.write('\n ---------------------------------------- \n')
            f.write (str(res[2]))

        
        file = argus.output + '/resumen.txt' 
        with open( file, 'w') as f:
            f.write (str(end_time - start_time))






    



