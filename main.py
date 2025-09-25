import csv


def cargar_paises(dataset):
	paises = []
	with open(dataset, 'r') as file:
		reader = csv.reader(file)
		next(reader) # Me salteo el encabezado
		for row in reader:
			pais = {
				'nombre': row[2],
				'continente': row[4],
				'poblacion': row[5],
				'area': row[13]
			}
			paises.append(pais)
	return paises


def mostrar_pais(pais):
	print(f"{pais['nombre']} - {pais['continente']}\n{pais['poblacion']} hab. - {pais['area']} km^2")


def mostrar_paises_resumen(paises):
	for pais in paises[:3] + paises[-3:]:
		mostrar_pais(pais)
	print()


def buscar_pais(paises, nombre):
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


def ordenar_nombre(paises):
	pass

def ordenar_poblacion(paises):
	pass


def ordenar_superficie(paises):
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
	opc = None
	paises = cargar_paises('data/world_population.csv')

	while opc != 0:
		opc = menu()
		match opc:
			case 1:
				nombre = input("Ingrese el nombre del pais: ")
				buscar_pais(paises, nombre)
			case 2:
				continente = input("Ingrese el nombre del continente: ")
				filtrar_continente(paises, continente)
			case 3:
				rango = input("Ingrese el rango de poblacion (minimo, maximo): ")
				filtrar_poblacion(paises, rango)
			case 4:
				rango = input("Ingrese el rango de superficie (minimo, maximo): ")
				filtrar_superficie(paises, rango)
			case 5:
				ordenar_nombre(paises)
			case 6:
				ordenar_poblacion(paises)
			case 7:
				ordenar_superficie(paises)
			case 8:
				mostrar_estadisticas(paises)
			case 0:
				print("Saliendo...")
				break
			case _:
				print("Opcion no valida")
inicio()