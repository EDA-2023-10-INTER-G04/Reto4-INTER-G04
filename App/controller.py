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
 """

import sys
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

def load_data(control, file, memflag=False):
    """
    Carga los datos del reto
    """
    start_time = get_time()
    
    # Inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = get_memory()
    
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
        model.add_data(control, info)
    
    for info in individuals_data:
        model.add_individual(control, info)
    
    x = model.anadir_nodos(control)
    vertices = x[0]
    MTPs = x[1]
    y = model.anadir_arcos(control)
    edges = y[0]
    gathering = y[1]
    grafo = model.carga(control)
    model.cantidad_mpts(control)
    
    # Toma el tiempo al final del proceso
    stop_time = get_time()
    # Calculando la diferencia en tiempo
    delta_t = delta_time(start_time, stop_time)
    
    # Finaliza el proceso para medir memoria
    mensaje = f"Tiempo: {delta_t}ms"
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # Calcula la diferencia de memoria
        delta_m = delta_memory(stop_memory, start_memory)
        # Respuesta con los datos de tiempo y memoria
        mensaje = f"Tiempo: {delta_t}ms, Memoria: {delta_m}kB"
    return vertices, MTPs, edges, gathering, grafo, mensaje
        
        
    


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


def req_1(control, mtp_inicio, mtp_destino):
    """
    Retorna el resultado del requerimiento 1
    """
    req1 = model.req_1(control, mtp_inicio, mtp_destino)
    return req1[0], req1[1], req1[2], req1[3], req1[4], req1[5]


def req_2(control, id_origen, id_destino, memflag= False):
    """
    Retorna el resultado del requerimiento 2
    """
    start_time = get_time()
    
    # Inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = get_memory()
    x = model.req_2(control, id_origen, id_destino)
     # Toma el tiempo al final del proceso
    stop_time = get_time()
    # Calculando la diferencia en tiempo
    delta_t = delta_time(start_time, stop_time)
    
    # Finaliza el proceso para medir memoria
    mensaje = f"Tiempo: {delta_t}ms"
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # Calcula la diferencia de memoria
        delta_m = delta_memory(stop_memory, start_memory)
        # Respuesta con los datos de tiempo y memoria
        mensaje = f"Tiempo: {delta_t}ms, Memoria: {delta_m}kB"
    return x, mensaje


def req_3(control, memflag= False):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = get_time()
    
    # Inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = get_memory()
        
    x = model.req_3(control)
     # Toma el tiempo al final del proceso
    stop_time = get_time()
    # Calculando la diferencia en tiempo
    delta_t = delta_time(start_time, stop_time)
    
    # Finaliza el proceso para medir memoria
    mensaje = f"Tiempo: {delta_t}ms"
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # Calcula la diferencia de memoria
        delta_m = delta_memory(stop_memory, start_memory)
        # Respuesta con los datos de tiempo y memoria
        mensaje = f"Tiempo: {delta_t}ms, Memoria: {delta_m}kB"
    return x, mensaje


def req_4(control, p_origen, p_destino):
    """
    Retorna el resultado del requerimiento 4
    """
    req4 = model.req_4(control, p_origen, p_destino)
    return req4


def req_5(control, inicio, distancia, puntos, mem):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    start_time = get_time()
    if mem == 1:
        tracemalloc.start()
        mem_ini = get_memory()
    resp = model.req_5(control, inicio, distancia, puntos)
    if mem == 1:
        mem_fin = get_memory()
        tracemalloc.stop()
        delta_m = delta_memory(mem_fin, mem_ini)
        return resp, delta_m
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return resp, delta_t

def req_6(control):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass

def req_7(control,templo, temphi, timelo, timehi, memflag= False):
    """
    Retorna el resultado del requerimiento 7
    """
    start_time = get_time()
    
    # Inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = get_memory()
    x = model.req_7(control, float(templo), float(temphi), timelo, timehi)
    # Toma el tiempo al final del proceso
    stop_time = get_time()
    # Calculando la diferencia en tiempo
    delta_t = delta_time(start_time, stop_time)
    
    # Finaliza el proceso para medir memoria
    mensaje = f"Tiempo: {delta_t}ms"
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # Calcula la diferencia de memoria
        delta_m = delta_memory(stop_memory, start_memory)
        # Respuesta con los datos de tiempo y memoria
        mensaje = f"Tiempo: {delta_t}ms, Memoria: {delta_m}kB"
    return x, mensaje


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
