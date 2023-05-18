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
 """

import config as cf
import model
import time
import csv
import tracemalloc
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    return model.new_data_structs()


# Funciones para la carga de datos

def load_data(control, file):
    """
    Carga los datos del reto
    """
    if file == 1:
        tracks = "BA-Grey-Wolf-tracks-utf8-small.csv"
        individuals = "BA-Grey-Wolf-individuals-utf8-small.csv"
    elif file ==2:
        tracks = "BA-Grey-Wolf-tracks-utf8-5pct.csv"
        individuals = "BA-Grey-Wolf-individuals-utf8-5pct.csv"
    elif file ==3:
        tracks = "BA-Grey-Wolf-tracks-utf8-10pct.csv"
        individuals = "BA-Grey-Wolf-individuals-utf8-10pct.csv"
    elif file ==4:
        tracks = "BA-Grey-Wolf-tracks-utf8-20pct.csv"
        individuals = "BA-Grey-Wolf-individuals-utf8-20pct.csv"
    elif file ==5:
        tracks = "BA-Grey-Wolf-tracks-utf8-30pct.csv"
        individuals = "BA-Grey-Wolf-individuals-utf8-30pct.csv"
    elif file ==6:
        tracks = "BA-Grey-Wolf-tracks-utf8-50pct.csv"
        individuals = "BA-Grey-Wolf-individuals-utf8-50pct.csv"
    elif file == 7:
        tracks = "BA-Grey-Wolf-tracks-utf8-80pct.csv"
        individuals = "BA-Grey-Wolf-individuals-utf8-80pct.csv"
    elif file == 8:
        tracks = "BA-Grey-Wolf-tracks-utf8-large.csv"
        individuals = "BA-Grey-Wolf-individuals-utf8-large.csv"
        
    datafile_individuals = cf.data_dir + individuals
    individuals_data = csv.DictReader(open(datafile_individuals, encoding="utf-8"))
    
    datafile_tracks = cf.data_dir + tracks
    tracks_data = csv.DictReader(open(datafile_tracks, encoding="utf-8"))
    
    
    
    for info in tracks_data:
        posicion = model.puntos_de_seguimiento(info["location-long"], info["location-lat"])
        individuo = model.identificador_compuesto(info["individual-local-identifier"], info["tag-local-identifier"])
        if mp.contains(control["mapa_eventos"], posicion):
            pareja = mp.get(control["mapa_eventos"], posicion)
            lista = me.getValue(pareja)
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
    model.anadir_arcos(control)
    return control
        
        
    


# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "file")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
