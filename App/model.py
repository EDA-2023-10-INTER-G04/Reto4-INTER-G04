﻿"""
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
    # TracksND = Grafo No Dirigido
    
    control = {"TracksD": None,"TracksND": None, "Individuo": None, "MTPs": None, "Tracks": None}
    
    control["Individuo"]= mp.newMap(97, 
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    cmpfunction=compareID)
    
    control["TracksMap"]= mp.newMap(100000, 
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    cmpfunction=compareID) 
    
    control["TracksGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                    directed=True,
                                    size=10000000,
                                    cmpfunction=None)
    
    control["TracksTree"] = om.newMap(omaptype="RBT",
                                  cmpfunction= None)
    
    control["MTPs"] = om.newMap(omaptype="RBT",
                                  cmpfunction= None)
    
    
    return control



# Funciones para agregar informacion al modelo

def add_ind(data_structs, data):
    map = data_structs["Individuo"]
    key = data["tag-id"]
    mp.put(map, key, data)

def add_edges(control):
    for lobo in lt.iterator(mp.keySet(control["TracksMap"])):
        entry = mp.get(control["TracksMap"], lobo)
        if entry:
            recorridos = me.getValue(entry)
            recorridos = mpqlist(recorridos)
            for i in range(1, lt.size(recorridos)-1):
                data1 = lt.getElement(recorridos, i)
                data2 = lt.getElement(recorridos, i-1)
                id1 = (puntos_de_seguimiento(data1))
                id2 = (puntos_de_seguimiento(data2))
                if id1 not in control["MTPs"]:
                    id1 = id1+"_"+data1["individual-local-identifier"]
                if id2 not in control["MTPs"]:
                    id2 = id2+"_"+data2["individual-local-identifier"]
                if id1 != id2:
                    gr.addEdge(control["TracksGraph"], id1, id2, 0)

def mpqlist(minpq):
    lista = lt.newList()
    while not (mpq.isEmpty(minpq)):
        minn = mpq.delMin(minpq)
        lt.addLast(lista, minn)
    return lista

def add_vertex(control, track):
    identificador = puntos_de_seguimiento(track["location-long"], track["location-lat"])
    if om.contains(control["TracksTree"], identificador) and not (om.contains(control["MTPs"])):
        gr.insertVertex(control["TracksGraph"], identificador)
    elif not(om.contains(control["MTPs"])):
        gr.insertVertex(control["TracksGraph"], (identificador+ "_" + track["individual-local-identifier"]))

def add_tracks(track, control):
    identificador = puntos_de_seguimiento(track["location-long"], track["location-lat"])
    if om.contains(control["TracksTree"], identificador) and not (om.contains(control["MTPs"])):
        om.put(control["MTPs"], identificador, None)
    om.put(control["TracksTree"], identificador, None)
    lobo = mp.get(control["TracksMap"], track["individual-local-identifier"])
    if lobo:
        recorrido = me.getValue(lobo)
    else:
        recorrido = mpq.newMinPQ(cmp_fecha2)
    mpq.insert(recorrido, track)
    mp.put(control["TracksMap"], track["individual-local-identifier"], recorrido)

    
    
    

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def puntos_de_seguimiento(longitud, latitud):
    longitud = round(longitud, 4)
    latitud = round(latitud, 4)
    
    id_comp = str(longitud)+"_"+str(latitud)

    id_comp.replace(".", "p")
    id_comp.replace("-", "m")
    
    return id_comp

    

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


def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


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
