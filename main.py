import os
import csv


def validar_texto(texto):
	"""
	Valida que el texto no sea vacío o contenga solo espacios en blanco.
	Retorna:
		- True: si el texto es válido
		- False: si el texto es inválido
	"""
	if not texto or texto.strip() == '':
		return False
	return True


def validar_y_parsear_opcion_menu(opcion):
	"""
	Valida que la opción no sea vacía o contenga solo espacios en blanco, y que sea un número válido.
	Retorna:
		- int: si la opción es válida
		- None: si la opción es inválida
	"""
	opcion = opcion.strip()

	if not opcion.isdigit():
		return None

	return int(opcion)


def validar_y_parsear_numero(texto, tipo=int):
	"""
	Valida que el número no sea vacío o contenga solo espacios en blanco, y que sea un número válido.
	Retorna:
		- int o float: si el número es válido
		- False: si el número es inválido
	"""
	if not validar_texto(texto):
		return False
	
	texto = texto.strip()
	
	if not texto.replace('.', '').isdigit():
		return False

	numero = float(texto)
	if tipo == int:
		return int(numero)
	return numero


def validar_y_parsear_registro(registro):
	"""
	Valida y parsea un registro del dataset.
	Retorna:
		- dict: si el registro es válido
		- None: si el registro es inválido
	"""
	nombre = registro.get('nombre')
	continente = registro.get('continente')
	poblacion = registro.get('poblacion')
	area = registro.get('area')

	es_valido = validar_texto(nombre) and validar_texto(continente) and validar_y_parsear_numero(poblacion, int) and validar_y_parsear_numero(area, float)

	if not es_valido:
		return None

	return {
		'nombre': nombre,
		'continente': continente,
		'poblacion': int(poblacion),
		'area': float(area)
	}


def parsear_nombre(nombre):
	"""
	Reemplaza acentos por sus equivalentes sin acentos.\n
	Retorna:
		- str: el nombre sin acentos en minúsculas
	"""
	nombre = nombre.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
	return nombre


def crear_archivo(dataset):
	"""
	Crea un archivo CSV vacío.
	"""
	with open(dataset, 'w') as archivo:
		writer = csv.DictWriter(archivo, fieldnames=['nombre', 'continente', 'poblacion', 'area'])
		writer.writeheader()
		print(f"ℹ️  Archivo {dataset} creado correctamente.")
	return


def agregar_pais_en_archivo(dataset, registro):
	"""
	Agrega un pais al archivo CSV.
	"""
	with open(dataset, 'a') as archivo:
		writer = csv.DictWriter(archivo, fieldnames=registro.keys())
		writer.writerow(registro)
		print(f"ℹ️  Pais agregado correctamente.")
	return


def cargar_paises(dataset):
	"""
	Carga los paises desde el dataset.
	Retorna:
		- Lista de paises (dict: nombre, continente, poblacion, area)
	"""
	paises = []

	if os.path.exists(dataset):
		with open(dataset, 'r') as archivo:
			reader = csv.DictReader(archivo)
			for indice, registro in enumerate(reader):
				pais = validar_y_parsear_registro(registro)
				if pais:
					paises.append(pais)
				else:
					print(f"⚠️  Registro inválido en la fila {indice + 2}")
		print(f"ℹ️  Se cargaron {len(paises)} paises")
	else:
		print(f"🚨 Error al cargar los paises: {dataset} no existe. Creando archivo...")
		crear_archivo(dataset)

	return paises


def mostrar_pais(pais):
	print(f"➡️  {pais['nombre']} - {pais['continente']} - {pais['poblacion']} hab. - {pais['area']} km^2")


def mostrar_paises(paises):
	"""
	Lista los paises.
	"""
	if not paises:
		print("🚨 No hay paises para listar")
		return

	print(f"🌎 Lista de {len(paises)} paises:")
	print("-" * 60)
	for pais in paises:
		mostrar_pais(pais)
	print("-" * 60)


def agregar_pais(paises, dataset):
	"""
	Agrega un pais al dataset.
	"""
	nombre = input("Ingrese el nombre del pais: ").strip()
	es_nombre_valido = validar_texto(nombre)
	if not es_nombre_valido:
		print("🚨 Nombre inválido")
		return

	continente = input("Ingrese el continente del pais: ").strip()
	es_continente_valido = validar_texto(continente)
	if not es_continente_valido:
		print("🚨 Continente inválido")
		return

	poblacion = input("Ingrese la población del pais: ")
	poblacion_parseada = validar_y_parsear_numero(poblacion, int)
	if not poblacion_parseada:
		print("🚨 Población inválida")
		return
		
	area = input("Ingrese el área del pais: ")
	area_parseada = validar_y_parsear_numero(area, float)
	if not area_parseada:
		print("🚨 Área inválida")
		return

	pais = {
		'nombre': nombre,
		'continente': continente,
		'poblacion': str(poblacion_parseada),
		'area': str(area_parseada)
	}

	if os.path.exists(dataset):
		agregar_pais_en_archivo(dataset, pais)
	else:
		print(f"🚨 Error al agregar el pais. Error: {dataset} no existe. Creando archivo...")
		crear_archivo(dataset)
		agregar_pais_en_archivo(dataset, pais)

	paises.append(pais)
	return


# Depende de buscar_pais
def actualizar_pais(paises, dataset):
	"""
	Actualiza un pais en el dataset.
	"""
	pais, indice = buscar_pais(paises)
	if not pais:
		print("Pais no encontrado")
		return
	
	poblacion = input("Ingrese la nueva población: ")
	poblacion_parseada = validar_y_parsear_numero(poblacion, int)
	if not poblacion_parseada:
		print("🚨 Población inválida")
		return
	
	area = input("Ingrese el nuevo área: ")
	area_parseada = validar_y_parsear_numero(area, float)
	if not area_parseada:
		print("🚨 Área inválida")
		return

	pais.update({'poblacion': str(poblacion_parseada), 'area': str(area_parseada)})

	if os.path.exists(dataset):
		paises[indice] = pais
		with open(dataset, 'w', newline='') as archivo:
			writer = csv.DictWriter(archivo, fieldnames=pais.keys())
			writer.writeheader()
			writer.writerows(paises)
		print(f"ℹ️  Pais actualizado correctamente")
	else:
		print(f"🚨 Error al actualizar el pais. Error: {dataset} no existe.")

	return


def buscar_pais(paises):
	
    print("---BUSCAR PAÍS---")
    pais_buscado = input("Ingrese el nombre del país que desea buscar: ").strip().title()

    # recorrer la lista de paises:
    for i, pais in enumerate(paises):
        if parsear_nombre(pais_buscado) in parsear_nombre(pais["nombre"]):
            print(f"El país buscado '{pais_buscado}' fue encontrado en el índice {i}")
            return pais, i

    return None
    
 
	# TODO: Debe devolver pais e indice! Usar enumerate
	# El pais buscado debe ser igual o parcialmente igual al nombre ingresado por el usuario


def filtrar_por_continente(paises):
	
	"""
	Filtra los paises por continente.
	Retorna:
		- Lista de paises
	"""
	continente = input("Ingrese el continente: ")
	es_continente_valido = validar_texto(continente)
	if not es_continente_valido:
		print("🚨 Continente inválido")
		return
	
	continente = parsear_nombre(continente)

	paises_filtrados = []
	for pais in paises:
		if parsear_nombre(pais['continente']) == continente:
			paises_filtrados.append(pais)
	return paises_filtrados


def filtrar_por_rango_poblacion(paises):
	"""
	Filtra los paises por rango de población.
	Retorna:
		- Lista de paises
	"""
	poblacion_minima = input("Ingrese la población mínima: ")
	poblacion_maxima = input("Ingrese la población máxima: ")

	poblacion_minima_parseada = validar_y_parsear_numero(poblacion_minima, int)
	if not poblacion_minima_parseada:
		print("🚨 Población mínima inválida")
		return

	poblacion_maxima_parseada = validar_y_parsear_numero(poblacion_maxima, int)
	if not poblacion_maxima_parseada:
		print("🚨 Población máxima inválida")
		return

	if poblacion_minima_parseada > poblacion_maxima_parseada:
		print("🚨 Población mínima debe ser menor a la población máxima")
		return

	paises_filtrados = []
	for pais in paises:
		if pais['poblacion'] >= poblacion_minima_parseada and pais['poblacion'] <= poblacion_maxima_parseada:
			paises_filtrados.append(pais)

	return paises_filtrados


def filtrar_por_rango_superficie(paises):
	"""
	Filtra los paises por rango de superficie.
	Retorna:
		- Lista de paises
	"""
	area_minima = input("Ingrese la superficie mínima: ")
	area_maxima = input("Ingrese la superficie máxima: ")
	
	area_minima_parseada = validar_y_parsear_numero(area_minima, float)
	if not area_minima_parseada:
		print("🚨 Superficie mínima inválida")
		return

	area_maxima_parseada = validar_y_parsear_numero(area_maxima, float)
	if not area_maxima_parseada:
		print("🚨 Superficie máxima inválida")
		return

	if area_minima_parseada > area_maxima_parseada:
		print("🚨 Superficie mínima debe ser menor a la superficie máxima")
		return

	paises_filtrados = []
	for pais in paises:
		if pais['area'] >= area_minima_parseada and pais['area'] <= area_maxima_parseada:
			paises_filtrados.append(pais)

	return paises_filtrados


def filtrar_paises(paises):
	"""
	Filtrar paises por continente, rango de población o rango de superficie.
	"""
	opcion = None

	print("""
🔍 Filtrar paises por:
	1) Continente
	2) Rango de población
	3) Rango de superficie
	4) Volver al menu principal
""")
	
	while True:
		opcion = validar_y_parsear_opcion_menu(input("Ingrese la opción de filtrado: "))
		match opcion:
			case 1:
				paises_filtrados = filtrar_por_continente(paises)
				mostrar_paises(paises_filtrados)
				break
			case 2:
				paises_filtrados = filtrar_por_rango_poblacion(paises)
				mostrar_paises(paises_filtrados)
				break
			case 3:
				paises_filtrados = filtrar_por_rango_superficie(paises)
				mostrar_paises(paises_filtrados)
				break
			case 4:
				break
			case _:
				print("🚨 Opción inválida")


def obtener_nombre(pais):#función auxiliar para buscar la key"nombre" en la lista de diccionarios
	return pais["nombre"]


def ordenar_por_nombre(paises):
	print("---ORDENAR PAÍSES POR NOMBRE---")
	paises_ordenados=sorted(paises,key=obtener_nombre)
	for p in paises_ordenados:
		print(p)
	return paises_ordenados


def obtener_poblacion(pais):
	return pais["poblacion"]

def ordenar_por_poblacion(paises):
	print("---ORDENAR PAÍSES POR POBLACIÓN---")
	poblacion=sorted(paises,key=obtener_poblacion)
	for p in poblacion:
		print(p)
	return poblacion	

def obtener_superficie(pais):#función auxiliar para obtener la key"superficie" 
	return pais["area"]

def ordenar_por_superficie_ascendente(paises):
	print("---ORDENAR PAÍSES POR SUPERFICIE DE FORMA ASCENDENTE---")
	superficie=sorted(paises,key=obtener_superficie)
	for s in superficie:
		print(s)
	return superficie

def ordenar_por_superficie_descendente(paises):
	print("---ORDENAR PAÍSES POR SUPERFICIE DE FORMA DESCENDENTE---")
	superficie=sorted(paises,key=obtener_superficie,reverse=True)
	for s in superficie:
		print(s)
	return superficie	




def ordenar_paises(paises):
	print("---ORDENAR PAÍSES---\n")
	print("1.ORDENAR PAISES POR NOMBRE")
	
	print("2.ORDENAR PAISES POR POBLACIÓN")
	print("3.ORDENAR PAISES POR SUPERFICIE DE FORMA ASCENDENTE")
	print("4.ORDENAR PAISES POR SUPERFICIE DE FORMA DESCENDENTE")
	opcion=input("Eliga una opción :").strip()
	if opcion=="":
		print("La opción no puede estar vacía")
		return
	if opcion=="1":
		
		ordenar_por_nombre(paises)
	elif opcion=="2":
		
		ordenar_por_poblacion(paises)
	elif opcion=="3":
		
		ordenar_por_superficie_ascendente(paises)
	elif opcion=="4":
		
		ordenar_por_superficie_descendente(paises)	
	else:
		print("Opción inválida. Elija una de las opcines disponibles")
		return			


def mostrar_estadisticas(paises):

	pass




def menu():
	print("""
🔍 Menu principal:
---------------------------
1) 🆕 Agregar un pais
2) 🔄 Actualizar un pais
3) 🔍 Buscar un pais
4) 🪝 Filtrar paises
5) 📚 Ordenar paises
6) 📊 Mostrar estadísticas
7) 👋 Salir
	""")
	opcion = input("Ingrese una opcion: ")
	return validar_y_parsear_opcion_menu(opcion)


def inicio():
	UBICACION_DATA = 'data/world_population_acotado.csv'
	paises = cargar_paises(UBICACION_DATA)

	while True:
		opc = menu()
		match opc:
			case 1:
				agregar_pais(paises=paises, dataset=UBICACION_DATA)
			case 2:
				actualizar_pais(paises=paises, dataset=UBICACION_DATA)
			case 3:
				buscar_pais(paises)
			case 4:
				filtrar_paises(paises)
			case 5:
				ordenar_paises(paises)
				
			case 6:
				mostrar_estadisticas(paises)
			case 7:
				print("👋 ¡Hasta luego!")
				break
			case _:
				print("🚨 Opción inválida")


inicio()