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


def validar_numero(numero):
	"""
	Valida que el número no sea vacío o contenga solo espacios en blanco, y que sea un número.
	Retorna:
		- True: si el número es válido
		- False: si el número es inválido
	"""
	return validar_texto(numero) and numero.isdigit()


def validar_y_parsear_registro(registro):
	"""
	Valida y parsea un registro del dataset.
	Retorna:
		- dict: si el registro es válido
		- None: si el registro es inválido
	"""
	nombre = registro.get('Country/Territory')
	continente = registro.get('Continent')
	poblacion = registro.get('2022 Population')
	area = registro.get('Area (km²)')

	es_valido = validar_texto(nombre) and validar_texto(continente) and validar_numero(poblacion) and validar_numero(area)

	if not es_valido:
		return None

	return {
		'nombre': nombre,
		'continente': continente,
		'poblacion': poblacion,
		'area': area
	}


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


def agregar_pais(paises):
	pass


def actualizar_pais(paises):
	pass


def buscar_pais(paises):
	# TODO: Revisar esta función
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
1) Buscar un pais
2) Filtrar paises por continente
3) Filtrar paises por rango de poblacion
4) Filtrar paises por rango de superficie
5) Ordenar paises por nombre
6) Ordenar paises por población
7) Ordenar paises por superficie
8) Mostrar estadísticas
0) Salir
	""")
	opcion = int(input("Ingrese una opcion: "))
	return opcion


def inicio():
	UBICACION_DATA = 'data/world_population.csv'
	paises = cargar_paises(UBICACION_DATA)

	while True:
		opc = menu()
		match opc:
			case 1:
				agregar_pais(paises)
			case 2:
				actualizar_pais(paises)
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