"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
import pandas as pd
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    return controller.new_controller()



def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    print ("1- small \n2-5pct \n3-10 pct \n4-20pct \n5-30pct \n6-50pct \n7-80pct \n8-large")
    resp = int(input("Seleccione el tamaño del archivo: "))

    x = controller.load_data(control, resp)
    print(x[0])
    print(x[1])
    print(x[2])
    print(x[3])
    #print(x[4])


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass


def puntos_de_seguimiento_inver(compuesto):
    
    lista = compuesto.replace("p", ".").replace("m", "-").split("_")
    long = lista[0]
    lat = lista[1]
    return long, lat

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    
    #m111p471_56p696
    #m111p165_56p701
    
    mtp_inicio = input("Inicio: ")
    mtp_destino = input("Destino: ")
    
    camino = controller.req_1(control, mtp_inicio, mtp_destino)
    
    print()
    print("============ Información Req 1 ============")
    print("Total nodos del camino recorrido: " + str(camino[2]))
    print("Puntos de encuentro en total: " + str(camino[4]))
    print("Total movimientos individuales: " + str(camino[5]))
    print("Distancia del camino: " + str(camino[1]) + "Km")
    print("Nodos del DFS: " + str(camino[2]))
    print("Arcos del DFS: " + str(camino[3]))
    
    info = camino[0]["elements"]
    for paso in info:
        
        long_lat = puntos_de_seguimiento_inver(paso["vertexA"])
        long = long_lat[0]
        lat = long_lat[1]
        
        paso["location-long-aprox"] = long
        paso["location-lat-aprox"] = lat
        
        paso["node-id"] = paso["vertexA"]
        del paso["vertexA"]
        paso["edge-to"] = paso["vertexB"]
        del paso["vertexB"]
        paso["edge-distance-km"] = paso["weight"]
        del paso["weight"]

    print(tabulate(info, headers="keys", tablefmt="simple_grid", maxcolwidths=20, maxheadercolwidths=20, showindex=False))
    
    #print(info)
    
    

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        try:
            if int(inputs) == 1:
                print("Cargando información de los archivos ....\n")
                data = load_data(control)
            elif int(inputs) == 2:
                print_req_1(control)

            elif int(inputs) == 3:
                print_req_2(control)

            elif int(inputs) == 4:
                print_req_3(control)

            elif int(inputs) == 5:
                print_req_4(control)

            elif int(inputs) == 6:
                print_req_5(control)

            elif int(inputs) == 7:
                print_req_6(control)

            elif int(inputs) == 8:
                print_req_7(control)

            elif int(inputs) == 9:
                print_req_8(control)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print("ERR:", exp)
            traceback.print_exc()
    sys.exit(0)
