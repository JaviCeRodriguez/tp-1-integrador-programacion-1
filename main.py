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


def validar_y_parsear_numero(texto, tipo=int):
	"""
	Valida que el número no sea vacío o contenga solo espacios en blanco, y que sea un número válido.
	Retorna:
		- int o float: si el número es válido
		- False: si el número es inválido
	"""
	if not validar_texto(texto):
		return False
	
	try:
		# Primero intentamos convertir a float (acepta enteros y decimales)
		numero = float(texto)
		# Si el tipo solicitado es int, convertimos
		if tipo == int:
			return int(numero)
		return numero
	except ValueError:
		return False


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

	return registro


def cargar_paises(dataset):
	"""
	Carga los paises desde el dataset.
	Retorna:
		- Lista de paises (dict: nombre, continente, poblacion, area)
	"""
	paises = []

	try:
		with open(dataset, 'r') as archivo:
			reader = csv.DictReader(archivo)
			for indice, registro in enumerate(reader):
				pais = validar_y_parsear_registro(registro)
				if pais:
					paises.append(pais)
				else:
					print(f"⚠️  Registro inválido en la fila {indice + 2}")
	except Exception as e:
		print(f"🚨 Error al cargar los paises: {e}")
	finally:
		print(f"ℹ️  Se cargaron {len(paises)} paises")
	return paises


def mostrar_pais(pais):
	print(f"{pais['nombre']} - {pais['continente']}\n{pais['poblacion']} hab. - {pais['area']} km^2")


def agregar_pais(paises, dataset):
	"""
	Agrega un pais al dataset.
	"""
	nombre = input("Ingrese el nombre del pais: ")
	es_nombre_valido = validar_texto(nombre)
	if not es_nombre_valido:
		print("🚨 Nombre inválido")
		return

	continente = input("Ingrese el continente del pais: ")
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

	try:
		with open(dataset, 'a') as archivo:
			writer = csv.DictWriter(archivo, fieldnames=pais.keys())
			writer.writerow(pais)
		paises.append(pais)
		print(f"ℹ️  Pais agregado correctamente")
	except Exception as e:
		print(f"🚨 Error al agregar el pais. Error: {e}")

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
	
	try:
		paises[indice] = pais
		with open(dataset, 'w', newline='') as archivo:
			writer = csv.DictWriter(archivo, fieldnames=pais.keys())
			writer.writeheader()
			writer.writerows(paises)
		print(f"ℹ️  Pais actualizado correctamente")
	except Exception as e:
		print(f"🚨 Error al actualizar el pais. Error: {e}")
	return


def buscar_pais(paises):
	# TODO: Debe devolver pais e indice! Usar enumerate
	nombre = input("Ingrese el nombre del pais: ")
	encontrado = False
	for pais in paises:
		if pais['nombre'].lower() == nombre.lower():
			mostrar_pais(pais)
			encontrado = True
			break
	if not encontrado:
		print("Pais no encontrado")


def filtrar_continente(paises, continente):
	pass


def filtrar_poblacion(paises, rango):
	pass

def filtrar_superficie(paises, rango):
	pass


def filtrar_paises(paises):
	pass


def ordenar_por_nombre(paises):
	pass

def ordenar_por_poblacion(paises):
	pass


def ordenar_por_superficie(paises):
	pass


def ordenar_paises(paises):
	pass


def mostrar_estadisticas(paises):
	pass


def menu():
	print("""
1) Agregar un pais
2) Actualizar un pais
3) Buscar un pais
4) Filtrar paises
5) Ordenar paises
6) Mostrar estadísticas
7) Salir
	""")
	opcion = int(input("Ingrese una opcion: "))
	return opcion


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