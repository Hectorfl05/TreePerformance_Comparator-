import string
import re
import time
import os
import pandas as pd
from avl2 import AVL2
from node import Node
from bplus import BPlusTree
from arbolb import TreeB
from bstar import BStarTree
import shutil


def Tiempo_Actual():
    
    #Obtiene la hora actual en formato HH:MM:SS.

    tiempo_actual = time.time()
    tiempo_struct = time.localtime(tiempo_actual)
    hora_actual = time.strftime("%H:%M:%S", tiempo_struct)
    return hora_actual


def solicitar_ruta_archivo():
    
    #Solicita la ruta del archivo de operaciones

    while True:
        ruta = input("Por favor, ingrese la ruta del archivo de operaciones (.txt): ")
        if os.path.isfile(ruta):
            return ruta
        else:
            print("La ruta ingresada no es válida o el archivo no existe. Por favor, intente de nuevo.")


def read_log(file_path):

    #Lee un archivo de log en formato CSV y convierte la columna 'Tiempo(ms)' a tipo float.
    
    data = pd.read_csv(file_path)
    data['Tiempo(ms)'] = data['Tiempo(ms)'].astype(float)
    return data


def TopStatistics(data):

    #Calcula estadísticas (top 10 tiempos más rápidos y lentos, tiempo promedio y total) 
    #para operaciones de inserción, búsqueda y eliminación de cada estructura.

    operations = ['Insercion', 'Busqueda', 'Eliminacion']
    statistics = {}
    
    for op in operations:
        op_data = data[data['Tipo de operacion'] == op]
        if not op_data.empty:
            top_10_fastest = op_data.nsmallest(10, 'Tiempo(ms)')
            top_10_slowest = op_data.nlargest(10, 'Tiempo(ms)')
            avg_time = op_data['Tiempo(ms)'].mean()
            total_time = op_data['Tiempo(ms)'].sum()
            statistics[op] = {
                'Top_10_Rapidos': top_10_fastest,
                'Top_10_Lentos': top_10_slowest,
                'Tiempo_Promedio': avg_time,
                'Tiempo_Total': total_time
            }
    
    return statistics

def add_positions(df):

    #Añade una columna de posiciones al Dataframe del log en formato CSV, para facilitar la identificacion del Top 10.
    
    df = df.reset_index(drop=True)
    df.index += 1
    return df

def print_statistics(tree_name, statistics, file_path):

    #Imprime y guarda las estadísticas de operaciones de una estructura de árbol específica.

   # Abre el archivo en modo append ('a') para agregar las estadísticas al final del archivo existente
    with open(file_path, 'a') as fileStatistics:
        
        # Imprime y escribe en el archivo el nombre de la estructura del árbol
        print(f"Estadisticas de la estructura {tree_name}:\n")
        fileStatistics.write(f"Estadisticas de la estructura {tree_name}:\n")
        
        # Recorre cada operación y sus estadísticas en el diccionario
        for op, stats in statistics.items():

            # Imprime y escribe en el archivo el nombre de la operación
            print(f"Operacion: {op}\n")
            fileStatistics.write(f"Operacion: {op}\n")
            
            # Obtiene los 10 tiempos más rápidos y los 10 más lentos, agregando posiciones a los datos
            top_10_rapidos = add_positions(stats['Top_10_Rapidos'][['Tiempo(ms)', 'Id', 'Nombre']])
            top_10_lentos = add_positions(stats['Top_10_Lentos'][['Tiempo(ms)', 'Id', 'Nombre']])
            
            # Imprime los 10 tiempos más rápidos
            print("Top 10 Tiempos mas rapidos:\n")
            print(top_10_rapidos)
            
            # Imprime los 10 tiempos más lentos
            print("\nTop 10 Tiempos mas lentos:\n")
            print(top_10_lentos)
            
            # Imprime el tiempo promedio y el tiempo total
            print(f"\nTiempo Promedio: {stats['Tiempo_Promedio']:.5f} ms\n")
            print(f"Tiempo Total: {stats['Tiempo_Total']:.5f} ms\n")
            print("\n\n")

            # Escribe los 10 tiempos más rápidos en el archivo
            fileStatistics.write("Top 10 Tiempos mas rapidos:\n")
            fileStatistics.write(top_10_rapidos.to_string())
            
            # Escribe los 10 tiempos más lentos en el archivo
            fileStatistics.write("\nTop 10 Tiempos mas lentos:\n")
            fileStatistics.write(top_10_lentos.to_string())
            
            # Escribe el tiempo promedio y el tiempo total en el archivo
            fileStatistics.write(f"\nTiempo Promedio: {stats['Tiempo_Promedio']:.5f} ms\n")
            fileStatistics.write(f"Tiempo Total: {stats['Tiempo_Total']:.5f} ms\n")
            fileStatistics.write("\n\n")



def solicitar_grado():

    # Solicita al usuario ingresar el grado del árbol y verifica que sea un entero mayor que 1.
    while True:
        try:
            grado = int(input("Ingrese el grado del árbol (debe ser un entero mayor que 1): "))
            if grado > 1:
                return grado
            else:
                print("El grado debe ser mayor que 1. Por favor, intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")
    







# Apertura de los archivos .txt para lectura y escritura

# Solicita la ruta del archivo al usuario
ruta_archivo_op = solicitar_ruta_archivo()


# Abre el archivo proporcionado por el usuario
with open(ruta_archivo_op, 'r') as file:
    lines = file.readlines()



# Crea la carpeta de logs y output si no existe
os.makedirs('logs', exist_ok=True)
os.makedirs('output', exist_ok=True)



# Crea los archivos de log en la carpeta de logs
fileAvl = open('logs/logAvl.txt', 'w')
fileBtree = open('logs/logBtree.txt', 'w')
fileBtreeplus = open('logs/logBtreeplus.txt', 'w')
fileBtreestar = open('logs/logBtreestar.txt', 'w')

# Diccionario para mapear tipos de árboles con sus archivos de log
log_files = {
    'AVL': 'logs/logAvl.txt',
    'Arbol B': 'logs/logBtree.txt',
    'Arbol B+': 'logs/logBtreeplus.txt',
    'Arbol B*': 'logs/logBtreestar.txt'
}

#Formateo del archivo.txt recibido de las operaciones a realizar

patternInsert = re.compile(r'Insert:\{id:(\d+),nombre:"([A-Za-z-]+)"\}')

patternSearch = re.compile(r'Search:\{id:(\d+)\}')

patternDelete = re.compile(r'Delete:\{id:(\d+)\}')

# Solicitud del grado del árbol B al usuario
degree = solicitar_grado()
print("\n")


# Instancia de los diferentes tipos de estructura de datos

TreeAVL = AVL2()

TreeBplus = BPlusTree(degree)

BTree = TreeB(degree)

starTree = BStarTree(degree)
 

#Formateo del encabezado de los archivos log de cada estructura
header = "Tipo de operacion,Hora de inicio,Hora de fin,Tiempo(ms),Id,Encontrado(Busqueda/Eliminacion),Nombre\n"
fileAvl.write(header)
fileBtree.write(header)
fileBtreeplus.write(header)
fileBtreestar.write(header)




# Itera sobre cada línea en la lista de líneas
for line in lines:
    
    # Busca coincidencias en la línea para las operaciones de inserción, búsqueda y eliminación
    matchInsert = patternInsert.search(line)
    matchSearch = patternSearch.search(line)
    matchDelete = patternDelete.search(line)

    if matchInsert:
        # Extrae id y nombre para la inserción
        id_value = int(matchInsert.group(1)) 
        name_value = matchInsert.group(2)

        # Inserción en el árbol AVL
        Hora_Inicio = Tiempo_Actual() 
        start_time = time.time() #Se guardan  los tiempos de inicio
        time.sleep(0.0000005)  # Pausa para simular tiempo de procesamiento y obtener mejores resultados

        TreeAVL.insert(id_value, name_value)

        end_time = time.time()
        elapsed_timer_ms_Insert = (end_time - start_time) * 1000
        Hora_Final = Tiempo_Actual() #Se guardan los tiempos de finalizacion y el tiempo de la operacion

        # Registra los resultados en el archivo de AVL
        fileAvl.write(f"Insercion,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Insert:.5f},{id_value},NA,{name_value}\n")


        # Inserción en el árbol B
        Hora_Inicio = Tiempo_Actual()
        start_time = time.time()
        time.sleep(0.0000005)

        BTree.insert(id_value, name_value)

        end_time = time.time()
        elapsed_timer_ms_Insert = (end_time - start_time) * 1000
        Hora_Final = Tiempo_Actual()

        # Registra los resultados en el archivo de B Tree
        fileBtree.write(f"Insercion,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Insert:.5f},{id_value},NA,{name_value}\n")

        # Inserción en el árbol B+
        Hora_Inicio = Tiempo_Actual()
        start_time = time.time()
        time.sleep(0.0000005)

        TreeBplus.insert(id_value, name_value)

        end_time = time.time()
        elapsed_timer_ms_Insert = (end_time - start_time) * 1000
        Hora_Final = Tiempo_Actual()

        # Registra los resultados en el archivo de B+ Tree
        fileBtreeplus.write(f"Insercion,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Insert:.5f},{id_value},NA,{name_value}\n")

        # Inserción en el árbol B*
        Hora_Inicio = Tiempo_Actual()
        start_time = time.time()
        time.sleep(0.0000005)

        starTree.insert(id_value, name_value)

        end_time = time.time()
        elapsed_timer_ms_Insert = (end_time - start_time) * 1000
        Hora_Final = Tiempo_Actual()

        # Registra los resultados en el archivo de B* Tree
        fileBtreestar.write(f"Insercion,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Insert:.5f},{id_value},NA,{name_value}\n")

    elif matchSearch:
        # Extrae id para la búsqueda
        id_value = int(matchSearch.group(1))

        # Búsqueda en el árbol AVL
        Hora_Inicio = Tiempo_Actual()
        start_timeSearch = time.time()
        time.sleep(0.0000005)

        NodeR, found_AVL = TreeAVL.search(id_value)

        end_timeSearch = time.time()
        elapsed_timer_ms_Search = (end_timeSearch - start_timeSearch) * 1000
        Hora_Final = Tiempo_Actual()

        # Registra los resultados en el archivo de AVL, dependiendo si se encontró el elemento
        if found_AVL:
            fileAvl.write(f"Busqueda,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Search:.5f},{id_value},Si,{NodeR.name}\n")
        else:
            fileAvl.write(f"Busqueda,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Search:.5f},{id_value},No,NA\n")

        # Búsqueda en el árbol B
        Hora_Inicio = Tiempo_Actual()
        start_time = time.time()
        time.sleep(0.0000005)

        found_Btree = BTree.search(id_value)

        end_time = time.time()
        elapsed_timer_ms_Search = (end_time - start_time) * 1000
        Hora_Final = Tiempo_Actual()

        # Registra los resultados en el archivo de B Tree
        if found_Btree is not None:
            fileBtree.write(f"Busqueda,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Search:.5f},{id_value},Si,{found_Btree}\n")
        else:
            fileBtree.write(f"Busqueda,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Search:.5f},{id_value},No,NA\n")

        # Búsqueda en el árbol B+
        Hora_Inicio = Tiempo_Actual()
        start_timeSearch = time.time()
        time.sleep(0.0000005)

        found_Bplus = TreeBplus.search(id_value)

        end_timeSearch = time.time()
        elapsed_timer_ms_Search = (end_timeSearch - start_timeSearch) * 1000
        Hora_Final = Tiempo_Actual()

        # Registra los resultados en el archivo de B+ Tree
        if found_Bplus is not None:
            fileBtreeplus.write(f"Busqueda,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Search:.5f},{id_value},Si,{found_Bplus}\n")
        else:
            fileBtreeplus.write(f"Busqueda,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Search:.5f},{id_value},No,NA\n")

        # Búsqueda en el árbol B*
        Hora_Inicio = Tiempo_Actual()
        start_timeSearch = time.time()
        time.sleep(0.0000005)

        found_Bstar = starTree.search(id_value)

        end_timeSearch = time.time()
        elapsed_timer_ms_Search = (end_timeSearch - start_timeSearch) * 1000
        Hora_Final = Tiempo_Actual()

        # Registra los resultados en el archivo de B* Tree
        if found_Bstar is not None:
            fileBtreestar.write(f"Busqueda,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Search:.5f},{id_value},Si,{found_Bstar}\n")
        else:
            fileBtreestar.write(f"Busqueda,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Search:.5f},{id_value},No,NA\n")

    elif matchDelete:

        # Extrae id para la eliminación
        id_value = int(matchDelete.group(1))

        # Eliminación en el árbol AVL
        Hora_Inicio = Tiempo_Actual()
        start_time = time.time()
        time.sleep(0.0000005)

        NodeE, found = TreeAVL.delete(id_value)

        end_time = time.time()
        elapsed_timer_msDelete = (end_time - start_time) * 1000
        Hora_Final = Tiempo_Actual()

        # Registra los resultados en el archivo de AVL, dependiendo si se eliminó el elemento
        if found:
            fileAvl.write(f"Eliminacion,{Hora_Inicio},{Hora_Final},{elapsed_timer_msDelete:.5f},{id_value},Si,{NodeE.name}\n")
        else:
            fileAvl.write(f"Eliminacion,{Hora_Inicio},{Hora_Final},{elapsed_timer_msDelete:.5f},{id_value},No,NA\n")

        # Eliminación en el árbol B
        found_Btree = BTree.search(id_value)

        Hora_Inicio = Tiempo_Actual()
        start_timeSearch = time.time()
        time.sleep(0.0000005)

        BTree.delete(id_value)

        end_timeSearch = time.time()
        elapsed_timer_ms_Delete = (end_timeSearch - start_timeSearch) * 1000
        Hora_Final = Tiempo_Actual()
        confirm_found_Btree = BTree.search(id_value)

        # Registra los resultados en el archivo de B Tree
        if found_Btree != confirm_found_Btree:
            fileBtree.write(f"Eliminacion,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Delete:.5f},{id_value},Si,{found_Btree}\n")
        else:
            fileBtree.write(f"Eliminacion,{Hora_Inicio},{Hora_Final},{elapsed_timer_ms_Delete:.5f},{id_value},No,NA\n")

        # Eliminación en el árbol B+
        found_Bplus = TreeBplus.search(id_value)

        Hora_Inicio = Tiempo_Actual()
        start_time = time.time()
        time.sleep(0.0000005)

        TreeBplus.delete(id_value)

        end_time = time.time()
        Hora_Final = Tiempo_Actual()
        elapsed_timer_msDelete = (end_time - start_time) * 1000

        confirm_found_Bplus = TreeBplus.search(id_value)

        # Registra los resultados en el archivo de B+ Tree
        if found_Bplus == confirm_found_Bplus:
            fileBtreeplus.write(f"Eliminacion,{Hora_Inicio},{Hora_Final},{elapsed_timer_msDelete:.5f},{id_value},No,NA\n")
        else:
            fileBtreeplus.write(f"Eliminacion,{Hora_Inicio},{Hora_Final},{elapsed_timer_msDelete:.5f},{id_value},Si,{found_Bplus}\n")

        # Eliminación en el árbol B*
        found_Bstar = starTree.search(id_value)

        Hora_Inicio = Tiempo_Actual()
        start_time = time.time()
        time.sleep(0.0000005)

        starTree.delete(id_value)

        end_time = time.time()
        Hora_Final = Tiempo_Actual()
        elapsed_timer_msDelete = (end_time - start_time) * 1000

        confirm_found_Bstar = starTree.search(id_value)

        # Registra los resultados en el archivo de B* Tree
        if found_Bstar != confirm_found_Bstar:
            fileBtreestar.write(f"Eliminacion,{Hora_Inicio},{Hora_Final},{elapsed_timer_msDelete:.5f},{id_value},Si,{found_Bstar}\n")
        else:
            fileBtreestar.write(f"Eliminacion,{Hora_Inicio},{Hora_Final},{elapsed_timer_msDelete:.5f},{id_value},No,NA\n")


fileAvl.close()
fileBtree.close()
fileBtreeplus.close()
fileBtreestar.close()

# Crear un archivo de salida en la carpeta output
output_file_path = 'output/output_statistics.txt'

# Leer los archivos de log y calcular las estadísticas
for tree_name, log_file_path in log_files.items():
    data = read_log(log_file_path)
    statistics = TopStatistics(data)
    print_statistics(tree_name, statistics, output_file_path)

























