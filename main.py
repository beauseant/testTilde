import glob
import argparse
import random
import json
import re
import multiprocessing


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
            data = list(filter (lambda articulo : articulo['paperAbstract'] != '', readJson (f)[:12000]))
            listAbstract = random.sample (data, argus.abstract)
            print ('finish with %s' % file)
    except Exception as E:
        print ('error leyendo %s, %s' % file, str(E))

    return listAbstract

def translate (articulo ):
    return len(re.findall(r'\w+', articulo['paperAbstract']))




if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Script en python para pasar openaire a psql')
    parser.add_argument('-t','--type', help='Tipo de textos a probar, scolar', required=True, choices=['scolar'])
    parser.add_argument('-p','--path', help='Ruta con los ficheros', required=True )
    parser.add_argument('-n','--numero', help='Número de archivos a procesar', required=True, type=int)
    parser.add_argument('-na','--abstract', help='Número de abstract de cada archivo a procesar', required=True, type=int)
    parser.add_argument('-th','--threads', required=True, type=int, help='hilos de ejecución a lanzar,1 secuencial')
    argus = parser.parse_args()




    token = 'u-fc6f1588-4dc0-4358-aa48-106749f327af'
    url = 'https://www.letsmt.eu/ws/service.svc/json/GetSystemList?appID=myappid'


    '''
    post_params = { 'client-id' : token }

    query_string = urllib.parse.urlencode( post_params ) 

    data = query_string.encode( "ascii" )    

 
    url = url + "?" + query_string 

 
    with urllib.request.urlopen( url ) as response: 
        data = response.read() 

    '''

    import urllib3

    http = urllib3.PoolManager()
    myHeaders = urllib3.util.make_headers(basic_auth='client-id:u-fc6f1588-4dc0-4358-aa48-106749f327af')
    resp = http.request('GET', url, headers=myHeaders)
    data = resp.data.decode('utf-8')

    


    

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


    with multiprocessing.Pool(processes= int(argus.threads)) as pool:
        results = pool.starmap(translate, zip(listAbstract))

    import ipdb ; ipdb.set_trace()



    



