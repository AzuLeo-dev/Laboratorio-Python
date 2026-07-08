import os

#=========================================
#           CONSTANTES
#=========================================

MULTA_DIA = 500

ARCHIVO_USUARIOS = "usuarios.txt"
ARCHIVO_LIBROS = "libros.txt"
ARCHIVO_PRESTAMOS = "prestamos.txt"

#=========================================
#      CREAR ARCHIVOS SI NO EXISTEN
#=========================================

def inicializar_archivos():

    archivos = [
        ARCHIVO_USUARIOS,
        ARCHIVO_LIBROS,
        ARCHIVO_PRESTAMOS
    ]

    for archivo in archivos:

        if not os.path.exists(archivo):

            nuevo = open(archivo, "w")
            nuevo.close()

#=========================================
#         CALCULAR MULTA
#=========================================

def calcular_multa(vencimiento, entrega):

    if entrega > vencimiento:

        dias = entrega - vencimiento

        return dias * MULTA_DIA

    return 0        

#=========================================
#        EXISTE USUARIO
#=========================================

def existe_usuario(dni):

    with open(ARCHIVO_USUARIOS, "r") as archivo:

        for linea in archivo:

            datos = linea.strip().split(";")

            if len(datos) > 0:

                if datos[0] == dni:

                    return True

    return False

#=========================================
#         EXISTE LIBRO
#=========================================

def existe_libro(id_libro):

    with open(ARCHIVO_LIBROS, "r") as archivo:

        for linea in archivo:

            datos = linea.strip().split(";")

            if len(datos) > 0:

                if datos[0] == id_libro:

                    return True

    return False

#=========================================
#        BUSCAR USUARIO
#=========================================

def buscar_usuario(dni):

    with open(ARCHIVO_USUARIOS, "r") as archivo:

        for linea in archivo:

            datos = linea.strip().split(";")

            if datos[0] == dni:

                return datos

    return None

#=========================================
#          BUSCAR LIBRO
#=========================================

def buscar_libro(id_libro):

    with open(ARCHIVO_LIBROS, "r") as archivo:

        for linea in archivo:

            datos = linea.strip().split(";")

            if datos[0] == id_libro:

                return datos

    return None

#=========================================
#        LISTAR USUARIOS
#=========================================

def listar_usuarios():

    print("\n========== USUARIOS ==========\n")

    with open(ARCHIVO_USUARIOS, "r") as archivo:

        hay = False

        for linea in archivo:

            datos = linea.strip().split(";")

            print(
                "DNI:", datos[0],
                "|", datos[1],
                datos[2],
                "| Cel:", datos[3]
            )

            hay = True

        if not hay:

            print("No existen usuarios registrados.")

#=========================================
#        REGISTRAR USUARIO
#=========================================

def registrar_usuario():

    print("\n=== REGISTRAR USUARIO ===")

    dni = input("DNI: ")

    if existe_usuario(dni):

        print("\nEse usuario ya existe.\n")
        return

    apellido = input("Apellido: ")
    nombre = input("Nombre: ")
    celular = input("Celular: ")

    with open(ARCHIVO_USUARIOS, "a") as archivo:

        archivo.write(
            f"{dni};{apellido};{nombre};{celular}\n"
        )

    print("\nUsuario registrado correctamente.\n")

#=========================================
#          REGISTRAR LIBRO
#=========================================

def cargar_libro():

    print("\n=== REGISTRAR LIBRO ===")

    id_libro = input("ID: ")

    if existe_libro(id_libro):

        print("\nEse libro ya existe.\n")
        return

    titulo = input("Titulo: ")

    with open(ARCHIVO_LIBROS, "a") as archivo:

        archivo.write(
            f"{id_libro};{titulo};True;0\n"
        )

    print("\nLibro agregado correctamente.\n")

#=========================================
#          MOSTRAR LIBROS
#=========================================

def mostrar_libros():

    print("\n=========== LIBROS ===========\n")

    with open(ARCHIVO_LIBROS, "r") as archivo:

        hay = False

        for linea in archivo:

            datos = linea.strip().split(";")

            estado = "Disponible"

            if datos[2] == "False":

                estado = "Prestado"

            print(

                "ID:", datos[0],
                "|", datos[1],
                "|", estado,
                "| Prestamos:", datos[3]

            )

            hay = True

        if not hay:

            print("No existen libros.")

def prestar_libro():

    print("\n=== PRESTAR LIBRO ===")

    dni = input("DNI: ")

    if not existe_usuario(dni):

        print("Usuario inexistente.")
        return

    id_libro = input("ID Libro: ")

    if not existe_libro(id_libro):

        print("Libro inexistente.")
        return

    entrada = open(ARCHIVO_LIBROS,"r")
    salida = open("aux_libros.txt","w")

    prestado = False

    for linea in entrada:

        datos = linea.strip().split(";")

        if datos[0] == id_libro:

            if datos[2] == "False":

                print("Ese libro ya esta prestado.")

                salida.write(linea)

            else:

                datos[2] = "False"

                datos[3] = str(int(datos[3])+1)

                salida.write(";".join(datos)+"\n")

                prestado = True

        else:

            salida.write(linea)

    entrada.close()
    salida.close()

    os.remove(ARCHIVO_LIBROS)
    os.rename("aux_libros.txt",ARCHIVO_LIBROS)

    if prestado:

        fecha = input("Fecha vencimiento (AAAAMMDD): ")

        with open(ARCHIVO_PRESTAMOS,"a") as archivo:

            archivo.write(
                f"{id_libro};{dni};{fecha};0\n"
            )

        print("Prestamo registrado.")

def devolver_libro():

    print("\n=== DEVOLVER LIBRO ===")

    dni = input("DNI: ")

    id_libro = input("ID Libro: ")

    fecha = int(input("Fecha entrega (AAAAMMDD): "))

    entrada = open(ARCHIVO_PRESTAMOS,"r")
    salida = open("aux_prestamos.txt","w")

    multa = 0

    encontrado = False

    for linea in entrada:

        datos = linea.strip().split(";")

        if datos[0]==id_libro and datos[1]==dni and datos[3]=="0":

            multa = calcular_multa(
                int(datos[2]),
                fecha
            )

            datos[3]=str(fecha)

            salida.write(";".join(datos)+"\n")

            encontrado=True

        else:

            salida.write(linea)

    entrada.close()
    salida.close()

    os.remove(ARCHIVO_PRESTAMOS)
    os.rename("aux_prestamos.txt",ARCHIVO_PRESTAMOS)

    if not encontrado:

        print("Prestamo inexistente.")
        return

    entrada=open(ARCHIVO_LIBROS,"r")
    salida=open("aux_libros.txt","w")

    for linea in entrada:

        datos=linea.strip().split(";")

        if datos[0]==id_libro:

            datos[2]="True"

        salida.write(";".join(datos)+"\n")

    entrada.close()
    salida.close()

    os.remove(ARCHIVO_LIBROS)
    os.rename("aux_libros.txt",ARCHIVO_LIBROS)

    print(f"Multa: ${multa}")

#=========================================
#            ESTADISTICAS
#=========================================

def estadisticas():

    print("\n========= ESTADISTICAS =========\n")

    total_libros = 0
    disponibles = 0
    prestados = 0

    mayor = -1
    libro_mas = ""

    with open(ARCHIVO_LIBROS, "r") as archivo:

        for linea in archivo:

            datos = linea.strip().split(";")

            total_libros += 1

            if datos[2] == "True":

                disponibles += 1

            else:

                prestados += 1

            cantidad = int(datos[3])

            if cantidad > mayor:

                mayor = cantidad
                libro_mas = datos[1]

    print("Total libros:", total_libros)
    print("Disponibles:", disponibles)
    print("Prestados:", prestados)
    print("Total prestamos realizados:", mayor if mayor != -1 else 0)

    if libro_mas != "":

        print("Libro mas solicitado:", libro_mas)

#=========================================
#         ELIMINAR USUARIO
#=========================================

def eliminar_usuario():

    dni = input("\nDNI del usuario: ")

    if not existe_usuario(dni):

        print("Ese usuario no existe.")
        return

    with open(ARCHIVO_PRESTAMOS, "r") as archivo:

        for linea in archivo:

            datos = linea.strip().split(";")

            if datos[1] == dni and datos[3] == "0":

                print("No puede eliminarse.")
                print("Tiene prestamos activos.")
                return

    entrada = open(ARCHIVO_USUARIOS, "r")
    salida = open("aux_usuarios.txt", "w")

    for linea in entrada:

        datos = linea.strip().split(";")

        if datos[0] != dni:

            salida.write(linea)

    entrada.close()
    salida.close()

    os.remove(ARCHIVO_USUARIOS)
    os.rename("aux_usuarios.txt", ARCHIVO_USUARIOS)

    print("Usuario eliminado.")

#=========================================
#          ELIMINAR LIBRO
#=========================================

def eliminar_libro():

    id_libro = input("\nID del libro: ")

    if not existe_libro(id_libro):

        print("Libro inexistente.")
        return

    entrada = open(ARCHIVO_LIBROS, "r")
    salida = open("aux_libros.txt", "w")

    eliminado = False

    for linea in entrada:

        datos = linea.strip().split(";")

        if datos[0] == id_libro:

            if datos[2] == "False":

                print("El libro esta prestado.")
                print("No puede eliminarse.")

                entrada.close()
                salida.close()

                os.remove("aux_libros.txt")

                return

            eliminado = True

            continue

        salida.write(linea)

    entrada.close()
    salida.close()

    os.remove(ARCHIVO_LIBROS)
    os.rename("aux_libros.txt", ARCHIVO_LIBROS)

    if eliminado:

        print("Libro eliminado.")

#=========================================
#      MOSTRAR PRESTAMOS ACTIVOS
#=========================================

def mostrar_prestamos_activos():

    print("\n====== PRESTAMOS ACTIVOS ======\n")

    hay = False

    with open(ARCHIVO_PRESTAMOS, "r") as archivo:

        for linea in archivo:

            datos = linea.strip().split(";")

            if datos[3] == "0":

                libro = buscar_libro(datos[0])

                usuario = buscar_usuario(datos[1])

                if libro and usuario:

                    print("-----------------------------")
                    print("Libro:", libro[1])
                    print("Usuario:", usuario[2], usuario[1])
                    print("DNI:", usuario[0])
                    print("Vence:", datos[2])

                    hay = True

    if not hay:

        print("No existen prestamos activos.")

#=========================================
#           MENU PRINCIPAL
#=========================================

def menu():

    while True:

        print("\n==============================")
        print(" SISTEMA DE BIBLIOTECA ")
        print("==============================")
        print("1 - Registrar usuario")
        print("2 - Registrar libro")
        print("3 - Mostrar libros")
        print("4 - Prestar libro")
        print("5 - Devolver libro")
        print("6 - Estadisticas")
        print("7 - Eliminar usuario")
        print("8 - Eliminar libro")
        print("9 - Mostrar prestamos activos")
        print("10 - Listar usuarios")
        print("0 - Salir")

        opcion = input("\nOpcion: ")

        if opcion == "1":

            registrar_usuario()

        elif opcion == "2":

            cargar_libro()

        elif opcion == "3":

            mostrar_libros()

        elif opcion == "4":

            prestar_libro()

        elif opcion == "5":

            devolver_libro()

        elif opcion == "6":

            estadisticas()

        elif opcion == "7":

            eliminar_usuario()

        elif opcion == "8":

            eliminar_libro()

        elif opcion == "9":

            mostrar_prestamos_activos()

        elif opcion == "10":

            listar_usuarios()

        elif opcion == "0":

            print("\nHasta luego.\n")
            break

        else:

            print("Opcion incorrecta.")

#=========================================
#              MAIN
#=========================================

inicializar_archivos()
menu()