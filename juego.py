import random
import datetime
import os
import getpass
from openpyxl import Workbook, load_workbook


ARCHIVO_EXCEL = "estadisticas_adivinanza.xlsx"

def inicializar_excel():
    if not os.path.exists(ARCHIVO_EXCEL):
        wb = Workbook()
        ws = wb.active
        ws.title = "Estadísticas"
        ws.append(["Fecha", "Modo", "Jugador1", "Jugador2", "Dificultad",
                   "Número Secreto", "Intentos Usados", "Resultado", "Nota"])
        wb.save(ARCHIVO_EXCEL)

def guardar_partida(modo, jugador1, jugador2, dificultad, numero_secreto,
                    intentos_usados, max_intentos, ganado):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resultado = "Ganado" if ganado else "Perdido"
    
    if ganado:
        nota = round((max_intentos - intentos_usados + 1) / max_intentos * 10, 2)
    else:
        nota = 0.0
    
    wb = load_workbook(ARCHIVO_EXCEL)
    ws = wb["Estadísticas"]
    ws.append([fecha, modo, jugador1, jugador2 or "", dificultad,
               numero_secreto, intentos_usados, resultado, nota])
    wb.save(ARCHIVO_EXCEL)

def mostrar_estadisticas(filtro_usuario=None):
    if not os.path.exists(ARCHIVO_EXCEL):
        print("No hay estadísticas guardadas aún.")
        return
    
    wb = load_workbook(ARCHIVO_EXCEL)
    ws = wb["Estadísticas"]
    
    filas = list(ws.iter_rows(min_row=2, values_only=True))
    
    if filtro_usuario:
        filas = [f for f in filas if filtro_usuario.lower() in (f[2] or "").lower() or
                 filtro_usuario.lower() in (f[3] or "").lower()]
        print(f"\n=== ESTADÍSTICAS FILTRADAS POR USUARIO: {filtro_usuario.upper()} ===")
    else:
        print("\n=== ESTADÍSTICAS GENERALES ===")
    
    if not filas:
        print("No se encontraron partidas con ese filtro.")
        return
    
    print(f"{'Fecha':20} {'Modo':10} {'Jugador1':12} {'Jugador2':12} "
          f"{'Dif.':6} {'Nº Secreto':12} {'Intentos':8} {'Resultado':10} {'Nota':5}")
    print("-" * 100)
    
    for row in filas:
        fecha, modo, j1, j2, dif, num, intentos, res, nota = row
        j2 = j2 or "-"
        num_mostrar = "***" if res == "Ganado" else num
        print(f"{fecha:20} {modo:10} {j1:12} {j2:12} {dif:6} "
              f"{num_mostrar:12} {intentos:8} {res:10} {nota:5}")

def elegir_dificultad():
    """Submenú común de dificultad usado en ambos modos."""
    while True:
        print("\nElige la dificultad:")
        print("1. Fácil (20 intentos)")
        print("2. Medio (12 intentos)")
        print("3. Difícil (5 intentos)")
        opc = input("Opción (1-3): ").strip()
        if opc == "1":
            return "Fácil", 20
        elif opc == "2":
            return "Medio", 12
        elif opc == "3":
            return "Difícil", 5
        else:
            print("Opción inválida.")

def jugar_solitario():
    dificultad_texto, max_intentos = elegir_dificultad()
    
    nombre = input("\nIngrese su nombre: ").strip()
    if not nombre:
        print("Nombre inválido.")
        return
    
    numero_secreto = random.randint(1, 1000)
    intentos = 0
    print(f"\n¡Bienvenido {nombre}! Adivina el número entre 1 y 1000.")
    print(f"Dificultad {dificultad_texto} - Tienes {max_intentos} intentos.\n")
    
    while intentos < max_intentos:
        try:
            adivinanza = int(input("Ingresa tu número: "))
        except ValueError:
            print("Por favor, ingresa un número válido.")
            continue
        
        intentos += 1
        if adivinanza == numero_secreto:
            print(f"¡Felicidades {nombre}! ¡Has ganado en {intentos} intentos!")
            guardar_partida("Solitario", nombre, None, dificultad_texto,
                            numero_secreto, intentos, max_intentos, True)
            return
        elif adivinanza < numero_secreto:
            print("El número buscado es mayor.")
        else:
            print("El número buscado es menor.")
        
        print(f"Te quedan {max_intentos - intentos} intentos.\n")
    
    print(f"¡Has perdido! El número era {numero_secreto}.")
    guardar_partida("Solitario", nombre, None, dificultad_texto,
                    numero_secreto, intentos, max_intentos, False)

def jugar_dos_jugadores():
    print("=== MODO 2 JUGADORES ===")
    jugador1 = input("Nombre del Jugador 1 (quien piensa el número): ").strip()
    if not jugador1:
        print("Nombre inválido.")
        return

    # Limpiar pantalla y pasar al Jugador 1
    print("\n" * 50)
    print(f"{jugador1}, ahora es tu turno de introducir el número secreto.")
    input("Presiona Enter cuando estés listo y el Jugador 2 no esté mirando...")

    # Entrada oculta del número secreto
    try:
        numero_secreto_str = getpass.getpass(prompt=f"{jugador1}, ingresa el número secreto (1-1000): ")
        numero_secreto = int(numero_secreto_str)
        if not 1 <= numero_secreto <= 1000:
            raise ValueError
    except:
        print("\nNúmero inválido. Partida cancelada.")
        return

    # Sugerencias según el número elegido
    print(f"\nNúmero secreto registrado.")
    print("\nSugerencias según el número:")
    if numero_secreto <= 100 or numero_secreto >= 900:
        print("- Está en un extremo → más difícil de adivinar.")
    elif numero_secreto <= 300 or numero_secreto >= 700:
        print("- Algo alejado del centro → dificultad media recomendada.")
    else:
        print("- Cerca del centro → más fácil de adivinar.")

    
    dificultad_texto, max_intentos = elegir_dificultad()

    # Limpiar pantalla para el Jugador 2
    print("\n" * 50)
    jugador2 = input("Nombre del Jugador 2 (quien adivina): ").strip()
    if not jugador2:
        print("Nombre inválido.")
        return

    print("\n" * 3)
    print(f"¡Turno de {jugador2}!")
    print(f"Adivina el número que pensó {jugador1} (entre 1 y 1000).")
    print(f"Dificultad: {dificultad_texto} - Tienes {max_intentos} intentos.\n")

    intentos = 0
    while intentos < max_intentos:
        try:
            adivinanza = int(input("Ingresa tu adivinanza: "))
        except ValueError:
            print("Por favor, ingresa un número válido.")
            continue
        
        intentos += 1
        if adivinanza == numero_secreto:
            print(f"¡ENHORABUENA {jugador2}! ¡Has acertado en {intentos} intentos!")
            guardar_partida("2 Jugadores", jugador1, jugador2, dificultad_texto,
                            numero_secreto, intentos, max_intentos, True)
            return
        elif adivinanza < numero_secreto:
            print("El número es mayor.")
        else:
            print("El número es menor.")
        
        print(f"Te quedan {max_intentos - intentos} intentos.\n")
    
    print(f"¡Se acabaron los intentos! El número era {numero_secreto}.")
    guardar_partida("2 Jugadores", jugador1, jugador2, dificultad_texto,
                    numero_secreto, intentos, max_intentos, False)

def menu_estadisticas():
    while True:
        print("\n--- Menú Estadísticas ---")
        print("1. Ver todas las estadísticas")
        print("2. Filtrar por nombre de jugador")
        print("3. Volver al menú principal")
        opc = input("Elige opción (1-3): ").strip()
        
        if opc == "1":
            mostrar_estadisticas()
        elif opc == "2":
            nombre = input("Ingresa el nombre del jugador a filtrar: ").strip()
            if nombre:
                mostrar_estadisticas(nombre)
            else:
                print("Nombre no válido.")
        elif opc == "3":
            break
        else:
            print("Opción inválida.")

def menu_principal():
    inicializar_excel()
    
    while True:
        print("\n" + "="*50)
        print("         JUEGO DE ADIVINANZA")
        print("="*50)
        print("1. Partida modo solitario")
        print("2. Partida 2 Jugadores")
        print("3. Estadísticas")
        print("4. Salir")
        opcion = input("\nElige una opción (1-4): ").strip()
        
        if opcion == "1":
            jugar_solitario()
        elif opcion == "2":
            jugar_dos_jugadores()
        elif opcion == "3":
            menu_estadisticas()
        elif opcion == "4":
            print("\n¡Gracias por jugar! Hasta pronto.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()