import csv
import os.path

def cargarArchivo(archivos_usuario):
   

    archivos = ['clientes','viajes']   
    archivos_usuario = []
    #Validar que los archivos a procesar existan
    for archivo in archivos:
        validar = True # variable de corte para el while
        while validar:
            nombre_archivo = input(f"Ingrese el nombre del archivo {archivo}, sin extencion \n")
            nombre_archivo = nombre_archivo + ".csv"
            archivo_existe = os.path.isfile(nombre_archivo)
            if archivo_existe:
                validar = False # corto while
            else:
                print('El archivo no existe, ingrese un nombre valido')
                validar = True

            if archivo_existe and archivo == 'clientes':
                aux_clientes = open(nombre_archivo, encoding="utf8")
                archivo_clientes = csv.reader(aux_clientes)
                next(archivo_clientes) # paso la primera linea de encabezados
                clientes = next(archivo_clientes, None)

                # validacion para todos los clientes.
                while clientes:
                    # valida documento
                    if len(clientes[2]) < 7 or len(clientes[2]) > 8:
                        print("Existen Documentos Invalidos, Por favor cargar otro archivo \n")
                        validar = True
                    # valida campos vacios
                    if len(clientes[0]) == 0 or len(clientes[1]) == 0 or len(clientes[3]) == 0 or len(clientes[4]) == 0 or len(clientes[5]) == 0:
                        print("Existen campos vacios en el archivo, Por favor cargar otro archivo \n")
                        validar = True
                    # valida email
                    if '@' not in clientes[4] or '.' not in clientes[4]:
                        print("Existen Emails Erroneos, Por favor cargar otro archivo \n")
                        validar = True

                    clientes = next(archivo_clientes, None)
            
            if archivo_existe and archivo == 'viajes':
                aux_viajes = open(nombre_archivo, encoding="utf8")
                archivo_viajes = csv.reader(aux_viajes)
                next(archivo_viajes) # paso la primera linea de encabezados 
                viajes = next(archivo_viajes, None)

                #Validar Campos vacios, precio 2 decimales - Archivo Viajes
                while viajes:
                    if len(viajes[0]) == 0 or len(viajes[1]) == 0 or len(viajes[2]) == 0:
                        print("Existen campos vacios en el archivo, Por favor cargar otro archivo \n")
                        validar = True # continuo pidiendo un archivo

                    try:
                        descomponer_monto = viajes[2].split('.')
                        if len(descomponer_monto[1]) != 2:
                            print(f"El precio {viajes[2]} no contiene 2 decimales, Por favor cargar otro archivo \n")
                            validar = True # continuo pidiendo un archivo
                    except IndexError:
                        print(f"El precio {viajes[2]} no contiene 2 decimales, Por favor cargar otro archivo \n")
                        validar = True # continuo pidiendo un archivo
                    

                    viajes = next(archivo_viajes, None)

            #Archivo Valido
            if archivo_existe and validar == False:
                print('Archivo Valido \n')
                archivos_usuario.append(nombre_archivo)
    
    return archivos_usuario
   



def archivosCargados(archivos_usuario):
    
    if len(archivos_usuario) > 0:
        return True
    else:
        print('No hay archivos cargado, por favor cargue los archivos \n')
        return False


def buscarCliente(archivos_usuario):
    if  (archivos_usuario):
        busqueda = input("Ingresa el nombre o parte del nombre a buscar: ")
        busqueda = busqueda.lower()
        resultados = []

        aux_clientes = open(archivos_usuario[0], encoding="utf8")
        archivo_clientes = csv.reader(aux_clientes)
        next(archivo_clientes) # paso la primera linea de encabezados
        clientes = next(archivo_clientes, None)

        while clientes:
            result = clientes[0].lower().find(busqueda)
            if(result != -1):
                resultados.append(clientes)

            clientes = next(archivo_clientes, None)

        #Imprimiendo resultados
        if len(resultados) == 0:
            print('El cliente que intentas buscar no existe \n')
        else :
            for cliente in resultados:
                print(cliente)  


def usuariosPorEmpresa(archivos_usuario):
    #agregar validacion lower en empresa para que busque en may y min
    if archivosCargados(archivos_usuario):
        buqueda_empresa = input("Ingresa el nombre de la empresa: ")
        resultados = []        

        aux_clientes = open(archivos_usuario[0], encoding="utf8")
        archivo_clientes = csv.reader(aux_clientes)
        next(archivo_clientes)
        clientes = next(archivo_clientes, None)     

        while clientes:
            if buqueda_empresa.lower() == clientes[5].lower():               
                resultados.append(clientes)

            clientes = next(archivo_clientes, None)
        
        if len(resultados) > 0:
            print(f"\nEmpresa {buqueda_empresa} \nTotal de usuarios: {len(resultados)} \n-----------------------------------------------------------------------")
            print("Nombre, dirección, documento, fecha de alta, correo electrónico, empresa")
            for cliente in resultados:
                print(cliente)
            print("\n")
        else: 
            print('La empresa que intentas buscar no existe \n')


def viajesPorEmpresa(archivos_usuario):
    if archivosCargados(archivos_usuario):
        empresa = input("Ingresa el nombre de la empresa: ")
        monto_total = 0
        existe_empresa = False

        aux_clientes = open(archivos_usuario[0], encoding="utf8")
        archivo_clientes = csv.reader(aux_clientes)
        next(archivo_clientes)
        clientes = next(archivo_clientes, None)

        while clientes:
            if empresa.lower() == clientes[5].lower():
                existe_empresa = True
                aux_viajes = open(archivos_usuario[1], encoding="utf8")
                archivo_viajes = csv.reader(aux_viajes)
                next(archivo_viajes)
                viajes = next(archivo_viajes, None)

                while viajes:
                    if clientes[2] == viajes[0]:
                        #Convertimos de string a float
                        monto_total += float(viajes[2])

                    viajes = next(archivo_viajes, None)

            clientes = next(archivo_clientes, None)
        
        if monto_total > 0:
            print(f"\n{empresa}: {monto_total:.2f} \n")
        elif existe_empresa and monto_total == 0:
            print("La empresa no tiene monto en viajes")
        else: 
            print('La empresa que intentas buscar no existe \n')


def viajesPorDocumento(archivos_usuario):
    if archivosCargados(archivos_usuario):
        documento = input("Ingresa el documento: ")
        datos_cliente = []
        registro_viajes = []      
        monto_total = 0
        documento_existe = False

        aux_clientes = open(archivos_usuario[0], encoding="utf8")
        archivo_clientes = csv.reader(aux_clientes)
        next(archivo_clientes)
        clientes = next(archivo_clientes, None)

        while clientes:
            if documento == clientes[2]:
                datos_cliente.append(clientes)

                documento_existe = True
                aux_viajes = open(archivos_usuario[1], encoding="utf8")
                archivo_viajes = csv.reader(aux_viajes)
                next(archivo_viajes)
                viajes = next(archivo_viajes, None)

                while viajes:
                    if clientes[2] == viajes[0]:                      
                        monto_total += float(viajes[2])
                        registro_viajes.append(viajes)

                    viajes = next(archivo_viajes, None)

            clientes = next(archivo_clientes, None)
        
        if monto_total > 0:
            print(f"\nDocumento: {documento}\n--------------------------------------------------------------------------\n[Nombre, dirección, documento, fecha de alta, correo electrónico, empresa]\n{datos_cliente}\n--------------------------------------------------------------------------")
            print(f"Total de viajes: {len(registro_viajes)}, Monto Total: {monto_total}\n--------------------------------------------------------------------------")
            for registro in registro_viajes:
                print(registro)
            print("\n")
        elif documento_existe and monto_total == 0:
            print("El cliente no tiene viajes")
        else: 
            print('El cliente que intentas buscar no existe \n')


def logger(accion):
    try:
        archivo = 'logs.csv'
        archivo_existe = os.path.isfile(archivo)
        with open(archivo, 'a', newline='') as file:
            fieldnames = ['Accion']
            file_logger = csv.DictWriter(file, fieldnames=fieldnames)

            if not archivo_existe:
                file_logger.writeheader()

            file_logger.writerow({'Accion': accion})
            return
    except IOError:
        print("Ocurrio un error con el archivo")


def opcion():
   while True:
       print("Elija una opcion: \n 1. Cargar Archivo \n 2. Buscar cliente por nombre" +
        "\n 3. Total de usuarios por empresa \n 4. Total de dinero de viajes por empresa" +
        "\n 5. Cantidad total de viajes por documento \n 6. Salir")
       opcion = input("")
       try:
           opcion = int(opcion)
           return opcion
       except ValueError:
           print("La opcion es incorrecta: escribe un numero entero \n")

def menu():
    archivos_usuario = []
    while True:
        logger('Menu')
        entrada = opcion()

        if entrada == 1:
            logger('Cargar Archivo')
            archivos_usuario = cargarArchivo(archivos_usuario)
        elif entrada == 2:
            logger('Busqueda de cliente por nombre')
            buscarCliente(archivos_usuario)
        elif entrada == 3:
            logger('Total de usuarios por empresa')
            usuariosPorEmpresa(archivos_usuario)
        elif entrada == 4:
            logger('Total de dinero de viajes por empresa')
            viajesPorEmpresa(archivos_usuario)
        elif entrada == 5:
            logger('Cantidad total de viajes por documento')
            viajesPorDocumento(archivos_usuario)
        elif entrada == 6:
            logger('Salir')
            exit()
        else:
            print("Por favor elija una opcion valida \n")

menu()
