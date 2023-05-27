"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
import datetime
import math
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    
    # TraksD = Grafo Dirigido
    
    control = {}
    
    control["tracksD"] = gr.newGraph(datastructure="ADJ_LIST", directed=True)
    control["tracksND"] = gr.newGraph(datastructure="ADJ_LIST", directed=False)
    control["mapa_eventos"] = mp.newMap(numelements=100, maptype="PROBING", loadfactor=0.5)
    control["mapa_arcos"] = mp.newMap(numelements=100, maptype="PROBING", loadfactor=0.5)
    control["mapa_individuos" ]= mp.newMap(numelements=100, maptype="PROBING", loadfactor=0.5)
    
    # TracksND = Grafo No Dirigido
    
    return control



# Funciones para agregar informacion al modelo

def add_individual(control, info):
    individuo = identificador_compuesto(info["animal-id"], info["tag-id"])
    mp.put(control["mapa_individuos"], individuo, info)

def add_data(control, info):
    """
    Función para agregar nuevos elementos a la lista
    """
    posicion = puntos_de_seguimiento(info["location-long"], info["location-lat"])
    individuo = identificador_compuesto(info["individual-local-identifier"], info["tag-local-identifier"])
    if mp.contains(control["mapa_eventos"], posicion):
            
        pareja = mp.get(control["mapa_eventos"], posicion)
        lista = me.getValue(pareja)
        if lt.isPresent(lista, individuo) == 0:
            lt.addLast(lista, individuo)    
    else:
        temp_lista = lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(temp_lista, individuo)
        mp.put(control["mapa_eventos"], posicion, temp_lista)
        
    if mp.contains(control["mapa_arcos"], individuo):
        pareja_arcos = mp.get(control["mapa_arcos"], individuo)
        lista_eventos = me.getValue(pareja_arcos)
        lt.addLast(lista_eventos, info)
    else:
        temp_lista = lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(temp_lista, info)
        mp.put(control["mapa_arcos"], individuo, temp_lista)


# Funciones para creacion de datos

def anadir_nodos(data_structs):
    """
    Crea una nueva estructura para modelar los datos
    """
    grafoD = data_structs["tracksD"]
    mapa_hash = data_structs["mapa_arcos"]
    llaves = mp.keySet(mapa_hash)
    for llave in lt.iterator(llaves):
        pareja = mp.get(mapa_hash, llave)
        lista = me.getValue(pareja)
        for evento in lt.iterator(lista):
            id1 = puntos_de_seguimiento(evento["location-long"], evento["location-lat"])
            id1= id1+"_"+identificador_compuesto(evento["individual-local-identifier"], evento["tag-local-identifier"])
            if not(gr.containsVertex(grafoD, id1)):
                gr.insertVertex(grafoD, id1)
    mapa_mtps = data_structs["mapa_eventos"]
    posiciones = mp.keySet(mapa_mtps)
    MTPs = 0
    for posicion in lt.iterator(posiciones):
        pareja = mp.get(mapa_mtps, posicion)
        lista = me.getValue(pareja)
        if lt.size(lista) > 1:
            gr.insertVertex(grafoD, posicion)
            MTPs += 1
    tracking_points = gr.numVertices(data_structs["tracksD"])
    return tracking_points, MTPs



def anadir_arcos(data_structs):
    """

    """
    grafoD = data_structs["tracksD"]
    mapa_hash = data_structs["mapa_arcos"]
    llaves = mp.keySet(mapa_hash)
    gathering_edges = 0
    def1 = 0
    def2 = 0
    def3 = 0
    def4 = 0
    for llave in lt.iterator(llaves):
        pareja = mp.get(mapa_hash, llave)
        tracks = me.getValue(pareja)
        
        quk.sort(tracks, cmp_fecha2)
        
        for i in range(1, lt.size(tracks)):
            event1 = lt.getElement(tracks, i)
            event2 = lt.getElement(tracks, i+1)
            id1 = puntos_de_seguimiento(event1["location-long"], event1["location-lat"])
            id_compuesto1 = id1+"_"+identificador_compuesto(event1["individual-local-identifier"], event1["tag-local-identifier"])
            id2 = puntos_de_seguimiento(event2["location-long"], event2["location-lat"])
            id_compuesto2 = id2+"_"+identificador_compuesto(event2["individual-local-identifier"], event2["tag-local-identifier"])
            y1 = float(((id1.split("_"))[1]).replace("p",".").replace("m", "-"))
            x1 = float(((id1.split("_"))[0]).replace("p",".").replace("m", "-"))
            y2 = float(((id2.split("_"))[1]).replace("p",".").replace("m", "-"))
            x2 = float(((id2.split("_"))[0]).replace("p",".").replace("m", "-"))
            distancia = (2*math.asin(math.sqrt((math.sin(math.radians((y1-y2))/2))**2)+(math.cos(math.radians(y1))*math.cos(math.radians(float(y2)))*(math.sin(math.radians((x1-float(x2))/2))**2))))*(6371)
            mtp1 = False
            mtp2 = False
            
            if gr.containsVertex(grafoD, id1):
                mtp1 = True
            if gr.containsVertex(grafoD, id2):
                mtp2 = True
            if id1 != id2:
                if mtp1 == True and mtp2 == False:
                    gr.addEdge(grafoD, id1, id_compuesto2, distancia)
                elif mtp1 == True and mtp2 == True:
                    gr.addEdge(grafoD, id1, id2, distancia)
                    gr.addEdge(grafoD, id1, id_compuesto2, distancia)
                    gr.addEdge(grafoD, id_compuesto2, id2)
                    gathering_edges += 2
                    def2 += 1
                elif mtp1 == False and mtp2 == True:
                    gr.addEdge(grafoD, id_compuesto1, id_compuesto2 ,distancia)
                    gr.addEdge(grafoD, id_compuesto2, id2)
                    gathering_edges += 1
                    def3 += 1
                elif mtp1 == False and mtp2 == False:
                    gr.addEdge(grafoD, id_compuesto1, id_compuesto2, distancia)
                    def4 += 1
            ultimo_evento = lt.getElement(tracks, lt.size(tracks))
            idultimo = puntos_de_seguimiento(ultimo_evento["location-long"], ultimo_evento["location-lat"])
            id_compuesto = idultimo+"_"+identificador_compuesto(ultimo_evento["individual-local-identifier"], ultimo_evento["tag-local-identifier"])
            if gr.containsVertex(grafoD, idultimo):
                gr.addEdge(grafoD, id_compuesto, idultimo)
                gathering_edges += 1
    edges = gr.numEdges(grafoD)    
    return  edges, gathering_edges
            
        
        
    

    
    
def puntos_de_seguimiento(longitud, latitud):
    longitud = round(float(longitud), 3)
    latitud = round(float(latitud), 3)
    
    id_comp = (str(longitud)+"_"+str(latitud)).replace(".", "p").replace("-", "m")
    
    return id_comp

def identificador_compuesto(individual, tag):
    compuesto = individual+"_"+tag
    return compuesto


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs, mtp_origen, mtp_destino):
    """
    mtp_origen: Identificador del punto de encuentro de origen.
                (corresponde al identificador único compuesto creado por la longitud-latitud de punto GPS)
    
    mtp_destino: Identificador del punto de encuentro de destino.
                 (corresponde al identificador único compuesto creado por la latitud-longitud del punto GPS)
    """

    estructura = dfs.DepthFirstSearch(data_structs["tracksD"], mtp_origen)
    camino = dfs.pathTo(estructura, mtp_destino)

    total_mtps = 0
    total_trackid = 0
    for vertice in lt.iterator(camino):
        if len(vertice) == 15:
            total_mtps += 1
        else:
            total_trackid += 1
        
    copia_camino = camino.copy()
    
    lista_vertices = lt.newList(datastructure="ARRAY_LIST")
    while not (st.isEmpty(copia_camino)):
        vertice = st.pop(copia_camino)
        lt.addLast(lista_vertices, vertice)
        
    distancia_total = 0
    lista_pesos = lt.newList(datastructure="ARRAY_LIST")
    temp = lt.newList(datastructure="ARRAY_LIST")
    for i in range(1, lt.size(lista_vertices)):
           vert1 = lt.getElement(lista_vertices, i)
           vert2 = lt.getElement(lista_vertices, i+1)
           arco = gr.getEdge(data_structs["tracksD"], vert1, vert2)
           lt.addLast(lista_pesos, arco["weight"])
           lt.addLast(temp, arco)
           distancia_total += float(arco["weight"])
    
    total_nodos = lt.size(camino)
    total_arcos = lt.size(lista_pesos)
    
    return temp, round(distancia_total, 3), total_nodos, total_arcos, total_mtps, total_trackid
    

def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def compareID(dato1, dato2):
    tag1 = int(dato1["tag-id"])
    tag2 = int(dato2["tag-id"])
    if tag1>tag2:
        return 1
    elif tag1 == tag2:
        return 0
    else:
        return -1

def cmp_fecha2(data_1, data_2):
    occurreddate1 = data_1["timestamp"]
    crimedate1 = datetime.datetime.strptime(occurreddate1.replace("+00",""), "%Y-%m-%d %H:%M")
    occurreddate2 = data_2["timestamp"]
    crimedate2 = datetime.datetime.strptime(occurreddate2.replace("+00",""), "%Y-%m-%d %H:%M")
    return crimedate1 < crimedate2

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
