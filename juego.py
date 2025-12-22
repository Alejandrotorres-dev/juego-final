import random
import datetime
import os
import getpass
from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, Reference

# --- COLORES---
try:
    from termcolor import colored
    COLORES_HABILITADOS = True
except ImportError:
    COLORES_HABILITADOS = False
    def colored(text, color=None, on_color=None, attrs=None):
        return text  # Fallback: sin color

# --- LIMPIEZA DE PANTALLA-
def limpiar_pantalla():
    """Limpia la pantalla de forma multiplataforma."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- ARCHIVO Y CONFIG ---
ARCHIVO_EXCEL = "estadisticas_adivinanza.xlsx"

def inicializar_excel():
    """Crea el archivo Excel si no existe y añade encabezados."""
    if not os.path.exists(ARCHIVO_EXCEL):
        wb = Workbook()
        ws = wb.active
        ws.title = "Estadísticas"
        ws.append(["Fecha", "Modo", "Jugador1", "Jugador2", "Dificultad",
                   "Número Secreto", "Intentos Usados", "Resultado", "Nota"])
        wb.save(ARCHIVO_EXCEL)

def guardar_partida(modo, jugador1, jugador2, dificultad, numero_secreto,
                    intentos_usados, max_intentos, ganado):
    """
    Guarda la partida en Excel y actualiza el gráfico de notas.
    
    Extra: Crea/actualiza un gráfico de barras con las notas de todas las partidas.
    """
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
    
    # - Gráfico de barras con las notas ---
    if ws.max_row > 1:  # Solo si hay datos
        chart = BarChart()
        chart.type = "col"
        chart.style = 10
        chart.title = "Notas de las partidas"
        chart.y_axis.title = "Nota (0-10)"
        chart.x_axis.title = "Partida"
        
        data = Reference(ws, min_col=9, min_row=1, max_row=ws.max_row)  # Columna Nota
        cats = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)  # Fechas como categorías
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        chart.height = 10
        chart.width = 20
        
        # Elimina gráfico anterior si existe
        for existing_chart in ws._charts[:]:
            ws._charts.remove(existing_chart)
        
        ws.add_chart(chart, "K2")
    
    wb.save(ARCHIVO_EXCEL)

def mostrar_estadisticas(filtro_usuario=None):
    """
    Muestra estadísticas en consola.
    
    Extra: Calcula promedio de nota y mejor partida.
    """
    if not os.path.exists(ARCHIVO_EXCEL):
        print(colored("No hay estadísticas guardadas aún.", 'yellow'))
        return
    
    wb = load_workbook(ARCHIVO_EXCEL)
    ws = wb["Estadísticas"]
    filas = list(ws.iter_rows(min_row=2, values_only=True))
    
    if filtro_usuario:
        filas = [f for f in filas if filtro_usuario.lower() in (f[2] or "").lower() or
                 filtro_usuario.lower() in (f[3] or "").lower()]
        print(colored(f"\n=== ESTADÍSTICAS FILTRADAS POR: {filtro_usuario.upper()} ===", 'cyan'))
    else:
        print(colored("\n=== ESTADÍSTICAS GENERALES ===", 'cyan'))
    
    if not filas:
        print(colored("No se encontraron partidas.", 'yellow'))
        return
    
    print(f"{'Fecha':20} {'Modo':10} {'Jugador1':12} {'Jugador2':12} "
          f"{'Dif.':6} {'Nº Secreto':12} {'Intentos':8} {'Resultado':10} {'Nota':5}")
    print("-" * 100)
    
    for row in filas:
        fecha, modo, j1, j2, dif, num, intentos, res, nota = row
        j2 = j2 or "-"
        num_mostrar = "***" if res == "Ganado" else num
        res_color = 'green' if res == "Ganado" else 'red'
        print(f"{fecha:20} {modo:10} {j1:12} {j2:12} {dif:6} "
              f"{num_mostrar:12} {intentos:8} {colored(res, res_color):10} {nota:5.2f}")
    
    # --- EXTRA: Estadísticas avanzadas ---
    notas_ganadas = [row[8] for row in filas if row[7] == "Ganado" and row[8] > 0]
    if notas_ganadas:
        promedio = sum(notas_ganadas) / len(notas_ganadas)
        print(colored(f"\nPromedio de nota en partidas ganadas: {promedio:.2f}", 'magenta'))
    
    mejor = max(filas, key=lambda x: x[8] if x[8] else 0)
    print(colored(f"Mejor nota: {mejor[8]:.2f} → {mejor[2]} ({mejor[0]})", 'magenta'))

def elegir_dificultad():
    """Submenú común de dificultad usado en ambos modos."""
    while True:
        print(colored("\nElige la dificultad:", 'blue'))
        print("1. Fácil (20 intentos)")
        print("2. Medio (12 intentos)")
        print("3. Difícil (5 intentos)")
        opc = input(colored("Opción (1-3): ", 'blue')).strip()
        if opc == "1":
            return "Fácil", 20
        elif opc == "2":
            return "Medio", 12
        elif opc == "3":
            return "Difícil", 5
        else:
            print(colored("Opción inválida. Intenta de nuevo.", 'red'))

def jugar_solitario():
    """Modo solitario: el ordenador genera el número."""
    dificultad_texto, max_intentos = elegir_dificultad()
    
    while True:
        nombre = input(colored("\nIngrese su nombre: ", 'blue')).strip()
        if len(nombre) < 2:
            print(colored("El nombre debe tener al menos 2 caracteres.", 'red'))
        else:
            break
    
    numero_secreto = random.randint(1, 1000)
    intentos = 0
    print(colored(f"\n¡Bienvenido {nombre}! Adivina el número entre 1 y 1000.", 'green'))
    print(colored(f"Dificultad {dificultad_texto} - Tienes {max_intentos} intentos.\n", 'green'))
    
    while intentos < max_intentos:
        try:
            adivinanza = int(input(colored("Ingresa tu número: ", 'blue')))
            if not 1 <= adivinanza <= 1000:
                print(colored("El número debe estar entre 1 y 1000.", 'red'))
                continue
        except ValueError:
            print(colored("Por favor, ingresa un número válido.", 'red'))
            continue
        
        intentos += 1
        if adivinanza == numero_secreto:
            print(colored(f"¡FELICIDADES {nombre.upper()}! ¡Has ganado en {intentos} intentos!", 'green', attrs=['bold']))
            guardar_partida("Solitario", nombre, None, dificultad_texto,
                            numero_secreto, intentos, max_intentos, True)
            return
        elif adivinanza < numero_secreto:
            print(colored("El número buscado es mayor ↑", 'yellow'))
        else:
            print(colored("El número buscado es menor ↓", 'yellow'))
        
        print(colored(f"Te quedan {max_intentos - intentos} intentos.\n", 'cyan'))
    
    print(colored(f"¡Has perdido! El número era {numero_secreto}.", 'red', attrs=['bold']))
    guardar_partida("Solitario", nombre, None, dificultad_texto,
                    numero_secreto, intentos, max_intentos, False)

def jugar_dos_jugadores():
    """Modo 2 jugadores: uno piensa, otro adivina."""
    print(colored("=== MODO 2 JUGADORES ===", 'magenta', attrs=['bold']))
    
    while True:
        jugador1 = input(colored("Nombre del Jugador 1 (quien piensa el número): ", 'blue')).strip()
        if len(jugador1) < 2:
            print(colored("Nombre demasiado corto.", 'red'))
        else:
            break

    limpiar_pantalla()
    print(colored(f"{jugador1}, ahora es tu turno de introducir el número secreto.", 'yellow'))
    input(colored("Presiona Enter cuando el Jugador 2 no esté mirando...", 'yellow'))

    try:
        numero_secreto_str = getpass.getpass(prompt=colored(f"{jugador1}, ingresa el número secreto (1-1000): ", 'blue'))
        numero_secreto = int(numero_secreto_str)
        if not 1 <= numero_secreto <= 1000:
            raise ValueError
    except:
        print(colored("\nNúmero inválido. Partida cancelada.", 'red'))
        return

    print(colored(f"\nNúmero secreto registrado.", 'green'))
    print(colored("\nSugerencias según el número:", 'cyan'))
    if numero_secreto <= 100 or numero_secreto >= 900:
        print(colored("- Está en un extremo → más difícil de adivinar.", 'red'))
    elif numero_secreto <= 300 or numero_secreto >= 700:
        print(colored("- Algo alejado del centro → dificultad media recomendada.", 'yellow'))
    else:
        print(colored("- Cerca del centro → más fácil de adivinar.", 'green'))

    dificultad_texto, max_intentos = elegir_dificultad()

    limpiar_pantalla()
    while True:
        jugador2 = input(colored("Nombre del Jugador 2 (quien adivina): ", 'blue')).strip()
        if len(jugador2) < 2:
            print(colored("Nombre demasiado corto.", 'red'))
        else:
            break

    limpiar_pantalla()
    print(colored(f"¡Turno de {jugador2}!", 'green', attrs=['bold']))
    print(colored(f"Adivina el número que pensó {jugador1} (entre 1 y 1000).", 'green'))
    print(colored(f"Dificultad: {dificultad_texto} - Tienes {max_intentos} intentos.\n", 'green'))

    intentos = 0
    while intentos < max_intentos:
        try:
            adivinanza = int(input(colored("Ingresa tu adivinanza: ", 'blue')))
            if not 1 <= adivinanza <= 1000:
                print(colored("El número debe estar entre 1 y 1000.", 'red'))
                continue
        except ValueError:
            print(colored("Por favor, ingresa un número válido.", 'red'))
            continue
        
        intentos += 1
        if adivinanza == numero_secreto:
            print(colored(f"¡ENHORABUENA {jugador2.upper()}! ¡Has acertado en {intentos} intentos!", 'green', attrs=['bold']))
            guardar_partida("2 Jugadores", jugador1, jugador2, dificultad_texto,
                            numero_secreto, intentos, max_intentos, True)
            return
        elif adivinanza < numero_secreto:
            print(colored("El número es mayor ↑", 'yellow'))
        else:
            print(colored("El número es menor ↓", 'yellow'))
        
        print(colored(f"Te quedan {max_intentos - intentos} intentos.\n", 'cyan'))
    
    print(colored(f"¡Se acabaron los intentos! El número era {numero_secreto}.", 'red', attrs=['bold']))
    guardar_partida("2 Jugadores", jugador1, jugador2, dificultad_texto,
                    numero_secreto, intentos, max_intentos, False)

def menu_estadisticas():
    """Menú para ver estadísticas."""
    while True:
        print(colored("\n--- Menú Estadísticas ---", 'cyan'))
        print("1. Ver todas las estadísticas")
        print("2. Filtrar por nombre de jugador")
        print("3. Volver al menú principal")
        opc = input(colored("Elige opción (1-3): ", 'blue')).strip()
        
        if opc == "1":
            mostrar_estadisticas()
        elif opc == "2":
            nombre = input(colored("Ingresa el nombre del jugador a filtrar: ", 'blue')).strip()
            if len(nombre) >= 2:
                mostrar_estadisticas(nombre)
            else:
                print(colored("Nombre no válido.", 'red'))
        elif opc == "3":
            break
        else:
            print(colored("Opción inválida.", 'red'))

def menu_principal():
    """Menú principal del juego."""
    inicializar_excel()
    
    print(colored("\n" + "="*60, 'magenta'))
    print(colored("         JUEGO DE ADIVINANZA - ¡VERSIÓN MEJORADA!", 'magenta', attrs=['bold']))
    print(colored("="*60, 'magenta'))
    
    while True:
        print(colored("\n1. Partida modo solitario", 'white'))
        print(colored("2. Partida 2 Jugadores", 'white'))
        print(colored("3. Estadísticas", 'white'))
        print(colored("4. Salir", 'white'))
        opcion = input(colored("\nElige una opción (1-4): ", 'blue')).strip()
        
        if opcion == "1":
            jugar_solitario()
        elif opcion == "2":
            jugar_dos_jugadores()
        elif opcion == "3":
            menu_estadisticas()
        elif opcion == "4":
            print(colored("\n¡Gracias por jugar! Hasta pronto.", 'green', attrs=['bold']))
            break
        else:
            print(colored("Opción no válida. Intenta de nuevo.", 'red'))

if __name__ == "__main__":
    menu_principal()