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
    control["req7"] = gr.newGraph(datastructure="ADJ_LIST", directed=True)
    control["arbol1"] = om.newMap(omaptype="RBT", cmpfunction=comparar_fechas)
    control["arbol2"] = om.newMap(omaptype="RBT", cmpfunction=comparar_fechas)
    control["mapa_eventos"] = mp.newMap(numelements=100, maptype="PROBING", loadfactor=0.5)
    control["mapa_arcos"] = mp.newMap(numelements=100, maptype="PROBING", loadfactor=0.5)
    control["mapa_individuos" ]= mp.newMap(numelements=100, maptype="PROBING", loadfactor=0.5)
    control["mapa_req7"]= mp.newMap(numelements=100, maptype="PROBING", loadfactor=0.5)
    control["mtps"] = lt.newList(datastructure="ARRAY_LIST")
    
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
    fecha = info["timestamp"]
    timestamp = datetime.datetime.strptime(fecha.replace("+00",""), "%Y-%m-%d %H:%M")
    entry = om.get(control["arbol1"], timestamp)
    if entry:
        lista = me.getValue(entry)
    else:
        lista = lt.newList("ARRAY_LIST")
    lt.addLast(lista, info)
    om.put(control["arbol1"], timestamp, lista)
    
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
def cantidad_mpts(data_structs):

    mapa_eventos = data_structs["mapa_eventos"]
    posiciones = mp.keySet(mapa_eventos)

    for posicion in lt.iterator(posiciones):
        pareja = mp.get(mapa_eventos, posicion)
        lista = me.getValue(pareja)
        if lt.size(lista) > 1:
            lt.addLast(data_structs["mtps"], posicion)
            
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
        primer_evento = lt.getElement(tracks, 1)
        idprimer = puntos_de_seguimiento(primer_evento["location-long"], primer_evento["location-lat"])
        id_compuesto = idprimer+"_"+identificador_compuesto(primer_evento["individual-local-identifier"], primer_evento["tag-local-identifier"])
        if gr.containsVertex(grafoD, idprimer):
            gr.addEdge(grafoD, id_compuesto, idprimer)
            gathering_edges += 1
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
                    gr.addEdge(grafoD, id1, id_compuesto2)
                elif mtp1 == True and mtp2 == True:
                    gr.addEdge(grafoD, id1, id2, distancia)
                    gr.addEdge(grafoD, id1, id_compuesto2, distancia)
                    gr.addEdge(grafoD, id_compuesto2, id2)
                    gathering_edges += 2
                    def2 += 1
                elif mtp1 == False and mtp2 == True:
                    gr.addEdge(grafoD, id_compuesto1, id_compuesto2)
                    gr.addEdge(grafoD, id_compuesto2, id2)
                    gathering_edges += 1
                    def3 += 1
                elif mtp1 == False and mtp2 == False:
                    gr.addEdge(grafoD, id_compuesto1, id_compuesto2)
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
    
    return camino
    

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
    #NO ENTIENDO XQ IDSCC TIENE COMO LLAVE CADA VERTICE Y COMO VALOR EL COMPONENTE AL QUE PERTENECE. SIRVE MUCHO MÁS SI ESTÁ AL REVES.
    Kosaraju = scc.KosarajuSCC(data_structs["tracksD"])
    total_componentes = scc.connectedComponents(Kosaraju)
    por_componentes = mp.newMap(numelements= 1663)
    final = lt.newList("ARRAY_LIST")
    keyset = mp.keySet(Kosaraju["idscc"])
    for i in lt.iterator(keyset):
        componente = me.getValue(mp.get(Kosaraju["idscc"], i))
        entry = mp.get(por_componentes, componente)
        if entry:
            valor = me.getValue(entry)
            valor["cantidad"] = valor["cantidad"]+1
            lista = valor["lista"]
            lt.addLast(lista, i)
            valor["lista"] = lista
            mp.put(por_componentes, componente, valor)
        else:
            lista = lt.newList("ARRAY_LIST")
            lt.addLast(lista, i)
            valor = {
                "componente": componente,
                "cantidad": 0,                
                "lista": lista
            }
            mp.put(por_componentes, componente, valor)
    temp = mp.valueSet(por_componentes)
    merg.sort(temp, cmp_cant_vert)
    if lt.size(temp) >= 5:
        x = lt.getElement(temp, 1)
        lt.addLast(final, x)
        x = lt.getElement(temp, 2)
        lt.addLast(final, x)
        x = lt.getElement(temp, 3)
        lt.addLast(final, x)
        x = lt.getElement(temp, 4)
        lt.addLast(final, x)
        x = lt.getElement(temp, 5)
        lt.addLast(final, x)
    else:
        final = temp
    entrega = lt.newList("ARRAY_LIST")
    for manada in lt.iterator(final):
        min_lat = 1000
        min_long = 1000
        max_lat = 0
        max_long = 0
        lobos = lt.newList("ARRAY_LIST")
        info_lobos = lt.newList("ARRAY_LIST")
        for n in lt.iterator(manada["lista"]):
            if len(n.split("_")) > 2:
                lobo = (n.split("_",2)[2])
                if lt.isPresent(lobos, lobo) == 0:
                    lt.addLast(lobos, lobo)
                    temp_info = me.getValue(mp.get(data_structs["mapa_individuos"], lobo))
                    sexo = temp_info["animal-sex"]
                    life_stage = temp_info["animal-life-stage"]
                    comments = temp_info["deployment-comments"]
                    if sexo == "":
                        sexo = "unknown"
                    if life_stage == "":
                        life_stage = "unknown"
                    if comments == "":
                        comments = "unknown"
                    info_lobo = {
                        "individual-id": lobo,
                        "animal-sex": sexo,
                        "animal-life-stage": life_stage,
                        "study-site": temp_info["study-site"],
                        "deployment-comments": comments
                    }
                    lt.addLast(info_lobos, info_lobo)
            lat = float(((n.split("_"))[1]).replace("p",".").replace("m", "-"))
            long = float(((n.split("_"))[0]).replace("p",".").replace("m", "-"))
            if lat < min_lat:
                min_lat = lat
            if lat > max_lat:
                max_lat = lat
            if long < min_long:
                min_long = long
            if long > max_long:
                max_long = long
        y = {
            "SCC": manada["componente"],
            "Node IDs": manada["lista"]["elements"],
            "SCC size": manada["cantidad"],
            "min-long": min_long,
            "min-lat": min_lat,
            "max-long": max_long,
            "max-lat": max_lat,
            "wolf count": lt.size(lobos),
            "wolf details": info_lobos["elements"]
        }
        lt.addLast(entrega, y)
    return entrega, total_componentes


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



def req_7(data_structs, templo= -17.3, temphi= 9.7, timelo="2012-11-28 00:00", timehi="2014-05-17 23:59"):
    """
    Función que soluciona el requerimiento 7
    """
    timelo = datetime.datetime.strptime(timelo.replace("+00",""), "%Y-%m-%d %H:%M")
    timehi = datetime.datetime.strptime(timehi.replace("+00",""), "%Y-%m-%d %H:%M")
    filtro1 = om.values(data_structs["arbol1"], timelo, timehi)
    inrange = lt.newList()
    for n in lt.iterator(filtro1):
        for x in lt.iterator(n):
            if int(templo) <= float(x["external-temperature"]) <= int(temphi):
                lt.addLast(inrange, x)
    mapa_recorridos = data_structs["mapa_req7"]
    for info in lt.iterator(inrange):
        individuo = identificador_compuesto(info["individual-local-identifier"], info["tag-local-identifier"])
        if mp.contains(mapa_recorridos, individuo):
            pareja_arcos = mp.get(mapa_recorridos, individuo)
            lista_eventos = me.getValue(pareja_arcos)
            lt.addLast(lista_eventos, info)
        else:
            temp_lista = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(temp_lista, info)
            mp.put(mapa_recorridos, individuo, temp_lista)
    anadir_nodos_alt(data_structs, inrange)
    anadir_arcos_alt(data_structs)
    Kosaraju = scc.KosarajuSCC(data_structs["req7"])
    total_componentes = scc.connectedComponents(Kosaraju)
    por_componentes = mp.newMap(numelements= 1663)
    final = lt.newList("ARRAY_LIST")
    keyset = mp.keySet(Kosaraju["idscc"])
    for i in lt.iterator(keyset):
        componente = me.getValue(mp.get(Kosaraju["idscc"], i))
        entry = mp.get(por_componentes, componente)
        if entry:
            valor = me.getValue(entry)
            valor["cantidad"] = valor["cantidad"]+1
            lista = valor["lista"]
            lt.addLast(lista, i)
            valor["lista"] = lista
            mp.put(por_componentes, componente, valor)
        else:
            lista = lt.newList("ARRAY_LIST")
            lt.addLast(lista, i)
            valor = {
                "componente": componente,
                "cantidad": 0,                
                "lista": lista
            }
            mp.put(por_componentes, componente, valor)
    temp = mp.valueSet(por_componentes)
    merg.sort(temp, cmp_cant_vert)
    if lt.size(temp) >= 6:
        x = lt.getElement(temp, 1)
        lt.addLast(final, x)
        x = lt.getElement(temp, 2)
        lt.addLast(final, x)
        x = lt.getElement(temp, 3)
        lt.addLast(final, x)
        x = lt.getElement(temp, lt.size(temp))
        lt.addLast(final, x)
        x = lt.getElement(temp, lt.size(temp)-1)
        lt.addLast(final, x)
        x = lt.getElement(temp, lt.size(temp)-2)
        lt.addLast(final, x)
    else:
        final = temp
    entrega = lt.newList("ARRAY_LIST")
    for manada in lt.iterator(final):
        min_lat = 1000
        min_long = 1000
        max_lat = 0
        max_long = 0
        max_dist = 0
        max_lp = None
        lp_path = {"elements": None}
        lobos = lt.newList("ARRAY_LIST")
        info_lobos = lt.newList("ARRAY_LIST")
        mst = prim.PrimMST(data_structs["req7"], lt.getElement(manada["lista"], 1))
        for n in lt.iterator(manada["lista"]):
            distancia = me.getValue(mp.get(mst["distTo"], n))
            if distancia >= max_dist:
                max_dist = distancia
                max_lp = n
            if len(n.split("_")) > 2:
                lobo = (n.split("_",2)[2])
                if lt.isPresent(lobos, lobo) == 0:
                    lt.addLast(lobos, lobo)
                    temp_info = me.getValue(mp.get(data_structs["mapa_individuos"], lobo))
                    sexo = temp_info["animal-sex"]
                    life_stage = temp_info["animal-life-stage"]
                    comments = temp_info["deployment-comments"]
                    if sexo == "":
                        sexo = "unknown"
                    if life_stage == "":
                        life_stage = "unknown"
                    if comments == "":
                        comments = "unknown"
                    info_lobo = {
                        "individual-id": lobo,
                        "animal-sex": sexo,
                        "animal-life-stage": life_stage,
                        "study-site": temp_info["study-site"],
                        "deployment-comments": comments
                    }
                    lt.addLast(info_lobos, info_lobo)
            
            lat = float(((n.split("_"))[1]).replace("p",".").replace("m", "-"))
            long = float(((n.split("_"))[0]).replace("p",".").replace("m", "-"))
            if lat < min_lat:
                min_lat = lat
            if lat > max_lat:
                max_lat = lat
            if long < min_long:
                min_long = long
            if long > max_long:
                max_long = long
        if max_lp != None:
            lp_path = pathTo(mst["edgeTo"], lt.newList("ARRAY_LIST"), max_lp)
        y = {
            "SCC": manada["componente"],
            "Node IDs": manada["lista"]["elements"],
            "SCC size": manada["cantidad"],
            "min-long": min_long,
            "min-lat": min_lat,
            "max-long": max_long,
            "max-lat": max_lat,
            "wolf count": lt.size(lobos),
            "wolf details": info_lobos["elements"],
            "LP distance": max_dist,
            "LP path": lp_path["elements"]
        }
        lt.addLast(entrega, y)
        
        
        
    return entrega, total_componentes
    
def pathTo(mst, lista, v):
    entry = mp.get(mst, v)
    origen = None
    if entry:
        origen = (me.getValue(entry))["vertexA"]
    if origen == None:
        return lista
    else:
        lt.addFirst(lista, origen)
        return pathTo(mst, lista, origen)
    
def anadir_nodos_alt(data_structs, inrange):
    """
    Crea una nueva estructura para modelar los datos
    """
    grafoD = data_structs["req7"]
    mapa_hash = data_structs["mapa_arcos"]
    llaves = mp.keySet(mapa_hash)
    for llave in lt.iterator(llaves):
        pareja = mp.get(mapa_hash, llave)
        lista = me.getValue(pareja)
        for evento in lt.iterator(lista):
            posicion = puntos_de_seguimiento(evento["location-long"], evento["location-lat"])
            id1= posicion+"_"+identificador_compuesto(evento["individual-local-identifier"], evento["tag-local-identifier"])
            if not(gr.containsVertex(grafoD, id1)) and evento in lt.iterator(inrange):
                gr.insertVertex(grafoD, id1) 
            if posicion in lt.iterator(data_structs["mtps"]) and evento in lt.iterator(inrange):
                gr.insertVertex(grafoD, posicion)

def anadir_arcos_alt(data_structs):
    grafoD = data_structs["req7"]
    mapa_hash = data_structs["mapa_req7"]
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
        primer_evento = lt.getElement(tracks, 1)
        idprimer = puntos_de_seguimiento(primer_evento["location-long"], primer_evento["location-lat"])
        id_compuesto = idprimer+"_"+identificador_compuesto(primer_evento["individual-local-identifier"], primer_evento["tag-local-identifier"])
        if gr.containsVertex(grafoD, idprimer):
            gr.addEdge(grafoD, id_compuesto, idprimer)
            gathering_edges += 1
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
                    gr.addEdge(grafoD, id_compuesto1, id_compuesto2, distancia)
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

def comparar_fechas(fecha_1, fecha_2):
    """
    Compara 2 fechas.

    Args:
        Fecha 1: _description_
        Fecha 2: _description_

    Returns:
        Retorna un valor numérico especifico dependiendo de la comparación correspondiente.
    """
    if (fecha_1 == fecha_2):
        return 0
    elif (fecha_1 > fecha_2):
        return 1
    else:
        return -1

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

def cmp_cant_vert(data1, data2):
    return data1["cantidad"]>data2["cantidad"]

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
