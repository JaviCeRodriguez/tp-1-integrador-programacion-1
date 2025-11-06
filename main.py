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
	"""
	Busca un pais en la lista de paises.
	Retorna:
		- Pais: si el pais es encontrado
		- None: si el pais no es encontrado
	"""
	pais_buscado = input("Ingrese el nombre del país que desea buscar: ").strip().title()

	for i, pais in enumerate(paises):
		if parsear_nombre(pais_buscado) in parsear_nombre(pais["nombre"]):
			print(f"El país buscado '{pais_buscado}' fue encontrado en el índice {i}")
			return pais, i

	return None


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


def obtener_nombre(pais):
	"""
	Obtiene el nombre de un pais.
	Retorna:
		- str: el nombre del pais
	"""
	return pais["nombre"]


def obtener_poblacion(pais):
	"""
	Obtiene la población de un pais.
	Retorna:
		- int: la población del pais
	"""
	return pais["poblacion"]


def obtener_superficie(pais):
	"""
	Obtiene la superficie de un pais.
	Retorna:
		- float: la superficie del pais
	"""
	return pais["area"]


def ordenar_por_nombre(paises):
	"""
	Ordena los paises por nombre.
	"""
	paises_ordenados = sorted(paises, key=obtener_nombre)
	for pais in paises_ordenados:
		mostrar_pais(pais)
	return paises_ordenados


def ordenar_por_poblacion(paises):
	"""
	Ordena los paises por población.
	"""
	poblacion=sorted(paises,key=obtener_poblacion)
	for pais in poblacion:
		mostrar_pais(pais)
	return poblacion	


def ordenar_por_superficie(paises, descendente=True):
	"""
	Ordena los paises por superficie de forma ascendente o descendente.
	"""
	superficie=sorted(paises,key=obtener_superficie,reverse=descendente)
	for pais in superficie:
		mostrar_pais(pais)
	return superficie


def ordenar_paises(paises):
	"""
	Ordena los paises por nombre, población o superficie.
	"""
	print("""
	📚 Ordenar paises por:
	1) Nombre
	2) Población
	3) Superficie (ascendente)
	4) Superficie (descendente)
	5) Volver al menu principal
	""")


	while True:
		opcion = validar_y_parsear_opcion_menu(input("Ingrese la opción de ordenamiento: "))
		match opcion:
			case 1:
				ordenar_por_nombre(paises)
				break
			case 2:
				ordenar_por_poblacion(paises)
				break
			case 3:
				ordenar_por_superficie(paises, descendente=False)
				break
			case 4:
				ordenar_por_superficie(paises, descendente=True)
				break
			case 5:
				break
			case _:
				print("🚨 Opción inválida")


def estadistica_mayor_y_menor_poblacion(paises):
	"""
	Calcula el país con mayor y menor población.
	"""
	mayor_poblacion = None
	menor_poblacion = None

	for pais in paises:
		if mayor_poblacion is None or pais['poblacion'] > mayor_poblacion['poblacion']:
			mayor_poblacion = pais
		if menor_poblacion is None or pais['poblacion'] < menor_poblacion['poblacion']:
			menor_poblacion = pais

	print(f"El país con mayor población es {mayor_poblacion['nombre']} con {mayor_poblacion['poblacion']} habitantes")
	print(f"El país con menor población es {menor_poblacion['nombre']} con {menor_poblacion['poblacion']} habitantes")


def estadistica_promedio_poblacion(paises):
	"""
	Calcula el promedio de población de los países.
	"""
	total_poblacion = 0
	for pais in paises:
		total_poblacion += pais['poblacion']
	promedio_poblacion = total_poblacion / len(paises)
	print(f"El promedio de población de los países es {promedio_poblacion:.2f} habitantes")


def estadistica_promedio_superficie(paises):
	"""
	Calcula el promedio de superficie de los países.
	"""
	total_superficie = 0
	for pais in paises:
		total_superficie += pais['area']
	promedio_superficie = total_superficie / len(paises)
	print(f"El promedio de superficie de los países es {promedio_superficie:.2f} km^2")


def estadistica_cantidad_paises_por_continente(paises):
	"""
	Calcula la cantidad de países por continente.
	"""
	cantidad_paises_por_continente = {}
	for pais in paises:
		cantidad_paises_por_continente[pais['continente']] = cantidad_paises_por_continente.get(pais['continente'], 0) + 1
	
	for continente, cantidad in cantidad_paises_por_continente.items():
		print(f"{continente} tiene {cantidad} países")


def mostrar_estadisticas(paises):
	opcion = None

	print("""
	📊 Mostrar estadísticas:
	1) País con mayor y menor población
	2) Promedio de población
	3) Promedio de superficie
	4) Cantidad de países por continente
	5) Volver al menu principal
	""")
	
	while True:
		opcion = validar_y_parsear_opcion_menu(input("Ingrese la opción de estadística: "))
		match opcion:
			case 1:
				estadistica_mayor_y_menor_poblacion(paises)
				break
			case 2:
				estadistica_promedio_poblacion(paises)
				break
			case 3:
				estadistica_promedio_superficie(paises)
				break
			case 4:
				estadistica_cantidad_paises_por_continente(paises)
				break
			case 5:
				break
			case _:
				print("🚨 Opción inválida")


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