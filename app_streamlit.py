import streamlit as st
import random
import datetime
import pandas as pd
import io
import os

# =================== CONFIGURACIÓN DE LA PÁGINA ===================
st.set_page_config(
    page_title="Juego de Adivinanza",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== FUNCIONES DE GUARDADO EN CSV ===================
ARCHIVO_ESTADISTICAS = "estadisticas_partidas.csv"

def cargar_estadisticas_desde_csv():
    """Carga las estadísticas desde un archivo CSV si existe."""
    try:
        if os.path.exists(ARCHIVO_ESTADISTICAS):
            df = pd.read_csv(ARCHIVO_ESTADISTICAS)
            return df.to_dict('records')
        else:
            return []
    except Exception as e:
        st.warning(f"No se pudieron cargar las estadísticas: {e}")
        return []

def guardar_estadisticas_a_csv():
    """Guarda las estadísticas actuales en un archivo CSV."""
    try:
        if st.session_state.estadisticas:
            df = pd.DataFrame(st.session_state.estadisticas)
            df.to_csv(ARCHIVO_ESTADISTICAS, index=False)
            return True
    except Exception as e:
        st.error(f"Error al guardar estadísticas: {e}")
    return False

# =================== ESTILOS CSS ===================
st.markdown("""
<style>
/* Eliminar barra blanca superior y otros elementos */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Ocultar la barra de menú de Streamlit */
.stDeployButton {display:none;}

/* Ocultar el menú hamburguesa */
#stDecoration {display:none;}

/* Ajustar márgenes superiores */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-top: 0rem;
}

/* Ocultar elementos adicionales */
[data-testid="stToolbar"] {display:none;}
[data-testid="stDecoration"] {display:none;}
[data-testid="stStatusWidget"] {display:none;}
.css-1lsmgbg {display: none;}

/* Ajustar el título principal */
h1 {
    margin-top: 0rem;
    padding-top: 0rem;
}

/* Estilo para contenedores */
.contenedor-botones-inicio {
    background: #f8f9fa;
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    border: 2px solid #dee2e6;
}

.titulo-boton {
    font-size: 20px !important;
    font-weight: bold !important;
    color: #333 !important;
    margin-bottom: 15px !important;
}

/* Estilos para mensajes de resultado */
.mensaje-correcto {
    background-color: #d4edda;
    border: 2px solid #c3e6cb;
    border-radius: 10px;
    padding: 20px;
    margin: 15px 0;
}

.mensaje-incorrecto {
    background-color: #f8d7da;
    border: 2px solid #f5c6cb;
    border-radius: 10px;
    padding: 20px;
    margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

# =================== INICIALIZAR DATOS EN SESSION_STATE ===================
if 'opcion_menu' not in st.session_state:
    st.session_state.opcion_menu = "Inicio"

if 'estadisticas' not in st.session_state:
    st.session_state.estadisticas = cargar_estadisticas_desde_csv()

# Inicializar variables para modo solitario
if 'numero_secreto_solo' not in st.session_state:
    st.session_state.numero_secreto_solo = None
if 'intentos_solo' not in st.session_state:
    st.session_state.intentos_solo = 0
if 'jugador_solo' not in st.session_state:
    st.session_state.jugador_solo = ""
if 'dificultad_solo' not in st.session_state:
    st.session_state.dificultad_solo = "Fácil"
if 'max_intentos_solo' not in st.session_state:
    st.session_state.max_intentos_solo = 20
if 'partida_activa_solo' not in st.session_state:
    st.session_state.partida_activa_solo = False
if 'resultado_mostrado_solo' not in st.session_state:
    st.session_state.resultado_mostrado_solo = False
if 'mensaje_resultado_solo' not in st.session_state:
    st.session_state.mensaje_resultado_solo = ""
if 'tipo_resultado_solo' not in st.session_state:
    st.session_state.tipo_resultado_solo = ""

# Inicializar variables para modo 2 jugadores
if 'numero_secreto_j2' not in st.session_state:
    st.session_state.numero_secreto_j2 = None
if 'intentos_j2' not in st.session_state:
    st.session_state.intentos_j2 = 0
if 'jugador1_nombre' not in st.session_state:
    st.session_state.jugador1_nombre = ""
if 'jugador2_nombre' not in st.session_state:
    st.session_state.jugador2_nombre = ""
if 'dificultad_j2' not in st.session_state:
    st.session_state.dificultad_j2 = "Fácil"
if 'max_intentos_j2' not in st.session_state:
    st.session_state.max_intentos_j2 = 20
if 'fase_j2' not in st.session_state:
    st.session_state.fase_j2 = 1
if 'resultado_mostrado_j2' not in st.session_state:
    st.session_state.resultado_mostrado_j2 = False
if 'mensaje_resultado_j2' not in st.session_state:
    st.session_state.mensaje_resultado_j2 = ""
if 'tipo_resultado_j2' not in st.session_state:
    st.session_state.tipo_resultado_j2 = ""

# =================== FUNCIONES DEL JUEGO ===================
def guardar_partida(modo, jugador1, jugador2, dificultad, numero_secreto, intentos_usados, ganado):
    """Guarda una partida en las estadísticas y en CSV"""
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resultado = "Ganado" if ganado else "Perdido"
    
    max_intentos = 0
    if modo == "Solitario":
        max_intentos = st.session_state.max_intentos_solo
    else:
        max_intentos = st.session_state.max_intentos_j2
    
    if ganado:
        nota = round((max_intentos - intentos_usados + 1) / max_intentos * 10, 2)
    else:
        nota = 0.0
    
    num_mostrar = "***" if ganado else numero_secreto
    
    st.session_state.estadisticas.append({
        "Fecha": fecha,
        "Modo": modo,
        "Jugador1": jugador1,
        "Jugador2": jugador2 or "",
        "Dificultad": dificultad,
        "Número Secreto": num_mostrar,
        "Intentos Usados": intentos_usados,
        "Max Intentos": max_intentos,
        "Resultado": resultado,
        "Nota": nota
    })
    
    guardar_estadisticas_a_csv()

def sugerir_dificultad(numero):
    """Sugiere dificultad basada en el número"""
    if numero <= 100 or numero >= 900:
        return "Está en un extremo, más difícil de adivinar."
    elif numero <= 300 or numero >= 700:
        return "Algo alejado del centro, dificultad media recomendada."
    else:
        return "Cerca del centro, más fácil de adivinar."

# =================== INTERFAZ PRINCIPAL ===================
st.title("JUEGO DE ADIVINANZA")
st.markdown("---")

with st.sidebar:
    st.header("MENÚ PRINCIPAL")
    
    opcion = st.radio(
        "Selecciona una opción:",
        ["Inicio", "Modo Solitario", "Modo 2 Jugadores", 
         "Estadísticas", "Instrucciones", "Acerca de"],
        key="menu_principal",
        index=["Inicio", "Modo Solitario", "Modo 2 Jugadores", 
               "Estadísticas", "Instrucciones", "Acerca de"].index(st.session_state.opcion_menu)
    )
    
    st.session_state.opcion_menu = opcion
    
    st.markdown("---")
    st.caption(f"Partidas jugadas: {len(st.session_state.estadisticas)}")

# =================== PÁGINA DE INICIO ===================
if opcion == "Inicio":
    st.header("Bienvenido al Juego de Adivinanza")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ## ¿Cómo funciona?
        
        **¡Adivina el número secreto entre 1 y 1000!**
        
        ### Modos de juego:
        1. **Modo Solitario**  
           - Juega contra la computadora
           - Elige tu dificultad
           - Intenta adivinar el número
        
        2. **Modo 2 Jugadores**  
           - Un jugador piensa el número
           - Otro intenta adivinarlo
           - Perfecto para jugar con amigos!
        
        ### Estadísticas:
        - Registro de todas tus partidas
        - Calificación por partida
        - Filtros por jugador y dificultad
        
        ### Sistema de puntuación:
        - + puntos por adivinar rápido
        - + puntos por elegir mayor dificultad
        - Nota final de 0 a 10
        """)
    
    with col2:
        record_container = st.container()
        with record_container:
            if st.session_state.estadisticas:
                mejor_partida = max(st.session_state.estadisticas, key=lambda x: x["Nota"])
                st.success("NUEVO RÉCORD")
                st.metric("Mejor nota", f"{mejor_partida['Nota']}/10", delta=f"por {mejor_partida['Jugador1']}")
                st.caption(f"Modo: {mejor_partida['Modo']}")
                st.caption(f"Dificultad: {mejor_partida['Dificultad']}")
            else:
                st.info("NUEVO RÉCORD")
                st.info("Aún no hay partidas jugadas")
        
        st.markdown("---")
        
        st.markdown("### Comenzar ahora:")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("Jugar modo solitario", key="btn_solitario_inicio"):
                # En Streamlit Cloud necesitamos usar st.switch_page()
                st.session_state.opcion_menu = "Modo Solitario"
                st.session_state.partida_activa_solo = False
                st.session_state.resultado_mostrado_solo = False
                st.session_state.mensaje_resultado_solo = ""
                st.session_state.numero_secreto_solo = None
                st.session_state.intentos_solo = 0
                st.rerun()
        
        with col_btn2:
            if st.button("Jugar con amigos", key="btn_j2_inicio"):
                # En Streamlit Cloud necesitamos usar st.switch_page()
                st.session_state.opcion_menu = "Modo 2 Jugadores"
                st.session_state.fase_j2 = 1
                st.session_state.resultado_mostrado_j2 = False
                st.session_state.mensaje_resultado_j2 = ""
                st.session_state.numero_secreto_j2 = None
                st.session_state.intentos_j2 = 0
                st.rerun()
# =================== MODO SOLITARIO ===================
elif opcion == "Modo Solitario":
    st.header("MODO SOLITARIO")
    
    if st.session_state.resultado_mostrado_solo and st.session_state.mensaje_resultado_solo:
        if st.session_state.tipo_resultado_solo == "correcto":
            st.markdown(f'<div class="mensaje-correcto">{st.session_state.mensaje_resultado_solo}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="mensaje-incorrecto">{st.session_state.mensaje_resultado_solo}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Jugar otra partida", type="primary", use_container_width=True):
                st.session_state.resultado_mostrado_solo = False
                st.session_state.mensaje_resultado_solo = ""
                st.session_state.partida_activa_solo = False
                st.session_state.numero_secreto_solo = None
                st.rerun()
        with col2:
            if st.button("Ver estadísticas", use_container_width=True):
                st.session_state.opcion_menu = "Estadísticas"
                st.rerun()
        
        st.markdown("---")
    
    if not st.session_state.partida_activa_solo and not st.session_state.resultado_mostrado_solo:
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            st.subheader("Configuración del jugador")
            nombre = st.text_input("Tu nombre:", placeholder="Ej: Carlos", key="nombre_solo_input")
            
            st.subheader("Dificultad")
            dificultad_opcion = st.selectbox(
                "Selecciona la dificultad:",
                ["Fácil", "Medio", "Difícil"],
                index=0,
                key="dificultad_select"
            )
            
            if dificultad_opcion == "Fácil":
                max_intentos = 20
                st.info("Fácil: 20 intentos")
            elif dificultad_opcion == "Medio":
                max_intentos = 12
                st.warning("Medio: 12 intentos")
            else:
                max_intentos = 5
                st.error("Difícil: Solo 5 intentos")
        
        with col_config2:
            st.subheader("¿Listo para jugar?")
            st.markdown(f"""
            ### Reglas:
            - Número entre 1 y 1000
            - {max_intentos} intentos máximo
            - El sistema te dirá si el número es mayor o menor
            - ¡Buena suerte!
            """)
            
            if st.button("COMENZAR PARTIDA", type="primary", use_container_width=True, key="btn_comenzar_solo"):
                if nombre:
                    st.session_state.jugador_solo = nombre
                    st.session_state.dificultad_solo = dificultad_opcion
                    st.session_state.max_intentos_solo = max_intentos
                    st.session_state.numero_secreto_solo = random.randint(1, 1000)
                    st.session_state.intentos_solo = 0
                    st.session_state.partida_activa_solo = True
                    st.session_state.resultado_mostrado_solo = False
                    st.session_state.mensaje_resultado_solo = ""
                    st.rerun()
                else:
                    st.error("Por favor, ingresa tu nombre")
    
    elif st.session_state.partida_activa_solo:
        if st.session_state.numero_secreto_solo is None:
            st.session_state.numero_secreto_solo = random.randint(1, 1000)
            st.warning("Se reinició la partida. ¡Buena suerte!")
        
        st.success(f"PARTIDA ACTIVA - Jugador: {st.session_state.jugador_solo}")
        
        col_juego1, col_juego2 = st.columns([2, 1])
        
        with col_juego1:
            st.subheader("Haz tu adivinanza")
            
            adivinanza = st.number_input(
                "Ingresa un número (1-1000):",
                min_value=1,
                max_value=1000,
                step=1,
                key="adivinanza_input"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("INTENTAR", type="primary", use_container_width=True, key="btn_intentar_solo"):
                    st.session_state.intentos_solo += 1
                    
                    if st.session_state.numero_secreto_solo is None:
                        st.error("Error: No hay número secreto. Reinicia la partida.")
                    elif adivinanza == st.session_state.numero_secreto_solo:
                        st.session_state.resultado_mostrado_solo = True
                        st.session_state.tipo_resultado_solo = "correcto"
                        st.session_state.mensaje_resultado_solo = f"""
                        <h3>¡FELICIDADES {st.session_state.jugador_solo.upper()}!</h3>
                        <p><strong>CORRECTO</strong> - ¡Has ganado en {st.session_state.intentos_solo} intentos!</p>
                        <p>Número secreto: <strong>{st.session_state.numero_secreto_solo}</strong></p>
                        <p>Dificultad: {st.session_state.dificultad_solo}</p>
                        """
                        
                        guardar_partida(
                            "Solitario",
                            st.session_state.jugador_solo,
                            None,
                            st.session_state.dificultad_solo,
                            st.session_state.numero_secreto_solo,
                            st.session_state.intentos_solo,
                            True
                        )
                        
                        st.rerun()
                    
                    elif adivinanza < st.session_state.numero_secreto_solo:
                        st.warning("MAYOR - El número secreto es mayor")
                    else:
                        st.warning("MENOR - El número secreto es menor")
                    
                    if st.session_state.intentos_solo >= st.session_state.max_intentos_solo:
                        st.session_state.resultado_mostrado_solo = True
                        st.session_state.tipo_resultado_solo = "incorrecto"
                        st.session_state.mensaje_resultado_solo = f"""
                        <h3>¡SE ACABARON LOS INTENTOS!</h3>
                        <p><strong>INCORRECTO</strong> - No lograste adivinar el número.</p>
                        <p>El número era: <strong>{st.session_state.numero_secreto_solo}</strong></p>
                        <p>Dificultad: {st.session_state.dificultad_solo}</p>
                        <p>¡Inténtalo de nuevo!</p>
                        """
                        
                        if st.session_state.numero_secreto_solo is not None:
                            guardar_partida(
                                "Solitario",
                                st.session_state.jugador_solo,
                                None,
                                st.session_state.dificultad_solo,
                                st.session_state.numero_secreto_solo,
                                st.session_state.intentos_solo,
                                False
                            )
                        
                        st.rerun()
            
            with col_btn2:
                if st.button("Cancelar partida", use_container_width=True, key="btn_cancelar_solo"):
                    st.session_state.partida_activa_solo = False
                    st.session_state.numero_secreto_solo = None
                    st.session_state.resultado_mostrado_solo = False
                    st.rerun()
        
        with col_juego2:
            st.subheader("Estado de la partida")
            
            st.metric(
                "Intentos usados",
                f"{st.session_state.intentos_solo} / {st.session_state.max_intentos_solo}"
            )
            
            progreso = st.session_state.intentos_solo / st.session_state.max_intentos_solo
            st.progress(progreso)
            
            st.info(f"Dificultad: {st.session_state.dificultad_solo}")
            st.info(f"Jugador: {st.session_state.jugador_solo}")
            
            if st.session_state.intentos_solo > 0 and st.session_state.numero_secreto_solo is not None:
                with st.expander("Pistas estadísticas"):
                    st.caption(f"Último intento: {adivinanza}")
                    if adivinanza < st.session_state.numero_secreto_solo:
                        st.caption(f"Prueba con números entre {adivinanza + 1} y 1000")
                    elif adivinanza > st.session_state.numero_secreto_solo:
                        st.caption(f"Prueba con números entre 1 y {adivinanza - 1}")

# =================== MODO 2 JUGADORES ===================
elif opcion == "Modo 2 Jugadores":
    st.header("MODO 2 JUGADORES")
    
    if st.session_state.resultado_mostrado_j2 and st.session_state.mensaje_resultado_j2:
        if st.session_state.tipo_resultado_j2 == "correcto":
            st.markdown(f'<div class="mensaje-correcto">{st.session_state.mensaje_resultado_j2}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="mensaje-incorrecto">{st.session_state.mensaje_resultado_j2}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Jugar otra partida", type="primary", use_container_width=True, key="btn_otra_j2"):
                st.session_state.resultado_mostrado_j2 = False
                st.session_state.mensaje_resultado_j2 = ""
                st.session_state.fase_j2 = 1
                st.session_state.numero_secreto_j2 = None
                st.rerun()
        with col2:
            if st.button("Ver estadísticas", use_container_width=True, key="btn_estadisticas_j2"):
                st.session_state.opcion_menu = "Estadísticas"
                st.rerun()
        
        st.markdown("---")
    
    if st.session_state.fase_j2 == 1 and not st.session_state.resultado_mostrado_j2:
        st.subheader("FASE 1: Jugador 1 (Piensa el número)")
        
        col_j1_1, col_j1_2 = st.columns(2)
        
        with col_j1_1:
            jugador1 = st.text_input("Nombre del Jugador 1:", 
                                   placeholder="Ej: Ana",
                                   key="jugador1_input")
            
            numero_secreto = st.number_input(
                "Número secreto (1-1000):",
                min_value=1,
                max_value=1000,
                step=1,
                key="numero_secreto_input",
                help="¡No le digas a nadie el número!"
            )
            
            if numero_secreto:
                sugerencia = sugerir_dificultad(numero_secreto)
                st.info(f"Sugerencia: {sugerencia}")
        
        with col_j1_2:
            st.subheader("Configurar dificultad")
            dificultad_j2_opcion = st.selectbox(
                "Dificultad para el Jugador 2:",
                ["Fácil", "Medio", "Difícil"],
                index=0,
                key="dificultad_j2_select"
            )
            
            if dificultad_j2_opcion == "Fácil":
                max_j2 = 20
                st.info("Fácil: 20 intentos")
            elif dificultad_j2_opcion == "Medio":
                max_j2 = 12
                st.warning("Medio: 12 intentos")
            else:
                max_j2 = 5
                st.error("Difícil: Solo 5 intentos")
            
            st.markdown("---")
            
            if st.button("REGISTRAR NÚMERO", type="primary", use_container_width=True, key="btn_registrar_j2"):
                if jugador1 and 1 <= numero_secreto <= 1000:
                    st.session_state.jugador1_nombre = jugador1
                    st.session_state.numero_secreto_j2 = numero_secreto
                    st.session_state.dificultad_j2 = dificultad_j2_opcion
                    st.session_state.max_intentos_j2 = max_j2
                    st.session_state.fase_j2 = 2
                    st.session_state.intentos_j2 = 0
                    st.session_state.resultado_mostrado_j2 = False
                    st.session_state.mensaje_resultado_j2 = ""
                    st.rerun()
                else:
                    st.error("Completa todos los campos correctamente")
    
    elif st.session_state.fase_j2 == 2 and not st.session_state.resultado_mostrado_j2:
        if st.session_state.numero_secreto_j2 is None:
            st.error("Error: No se configuró el número secreto. Vuelve a la fase 1.")
            if st.button("Volver a fase 1", key="btn_volver_fase1"):
                st.session_state.fase_j2 = 1
                st.rerun()
        else:
            st.subheader("FASE 2: Jugador 2 (Adivina el número)")
            
            col_j2_1, col_j2_2 = st.columns(2)
            
            with col_j2_1:
                jugador2 = st.text_input("Nombre del Jugador 2:",
                                       placeholder="Ej: Luis",
                                       key="jugador2_input")
                
                if jugador2:
                    st.success(f"Reto: Adivina el número de {st.session_state.jugador1_nombre}")
                    st.info(f"Dificultad: {st.session_state.dificultad_j2}")
                    st.warning(f"Intentos disponibles: {st.session_state.max_intentos_j2}")
                    
                    adivinanza_j2 = st.number_input(
                        "Tu adivinanza:",
                        min_value=1,
                        max_value=1000,
                        step=1,
                        key="adivinanza_j2_input"
                    )
                    
                    if st.button("INTENTAR ADIVINAR", type="primary", use_container_width=True, key="btn_intentar_j2"):
                        if jugador2:
                            st.session_state.jugador2_nombre = jugador2
                            st.session_state.intentos_j2 += 1
                            
                            if adivinanza_j2 == st.session_state.numero_secreto_j2:
                                st.session_state.resultado_mostrado_j2 = True
                                st.session_state.tipo_resultado_j2 = "correcto"
                                st.session_state.mensaje_resultado_j2 = f"""
                                <h3>¡{jugador2.upper()} HA GANADO!</h3>
                                <p><strong>CORRECTO</strong> - ¡Adivinó en {st.session_state.intentos_j2} intentos!</p>
                                <p>Número secreto: <strong>{st.session_state.numero_secreto_j2}</strong></p>
                                <p>Dificultad: {st.session_state.dificultad_j2}</p>
                                <p>Jugador 1: {st.session_state.jugador1_nombre}</p>
                                """
                                
                                guardar_partida(
                                    "2 Jugadores",
                                    st.session_state.jugador1_nombre,
                                    jugador2,
                                    st.session_state.dificultad_j2,
                                    st.session_state.numero_secreto_j2,
                                    st.session_state.intentos_j2,
                                    True
                                )
                                
                                st.rerun()
                            
                            elif adivinanza_j2 < st.session_state.numero_secreto_j2:
                                st.warning("MAYOR - Intenta con un número más grande")
                            else:
                                st.warning("MENOR - Intenta con un número más pequeño")
                            
                            if st.session_state.intentos_j2 >= st.session_state.max_intentos_j2:
                                st.session_state.resultado_mostrado_j2 = True
                                st.session_state.tipo_resultado_j2 = "incorrecto"
                                st.session_state.mensaje_resultado_j2 = f"""
                                <h3>¡SE ACABARON LOS INTENTOS!</h3>
                                <p><strong>INCORRECTO</strong> - No lograste adivinar el número.</p>
                                <p>El número era: <strong>{st.session_state.numero_secreto_j2}</strong></p>
                                <p>Dificultad: {st.session_state.dificultad_j2}</p>
                                <p>Jugador 1: {st.session_state.jugador1_nombre}</p>
                                <p>¡Inténtalo de nuevo!</p>
                                """
                                
                                guardar_partida(
                                    "2 Jugadores",
                                    st.session_state.jugador1_nombre,
                                    jugador2,
                                    st.session_state.dificultad_j2,
                                    st.session_state.numero_secreto_j2,
                                    st.session_state.intentos_j2,
                                    False
                                )
                                
                                st.rerun()
            
            with col_j2_2:
                if st.session_state.jugador2_nombre or jugador2:
                    nombre_actual = st.session_state.jugador2_nombre or jugador2
                    st.subheader(f"Estado - {nombre_actual}")
                    
                    st.metric(
                        "Intentos usados",
                        f"{st.session_state.intentos_j2} / {st.session_state.max_intentos_j2}"
                    )
                    
                    progreso_j2 = st.session_state.intentos_j2 / st.session_state.max_intentos_j2
                    st.progress(progreso_j2)
                    
                    st.info(f"Contra: {st.session_state.jugador1_nombre}")
                    st.info(f"Dificultad: {st.session_state.dificultad_j2}")
                    
                    if st.button("Cancelar partida", use_container_width=True, key="btn_cancelar_j2"):
                        st.session_state.fase_j2 = 1
                        st.session_state.numero_secreto_j2 = None
                        st.session_state.resultado_mostrado_j2 = False
                        st.rerun()

# =================== ESTADÍSTICAS ===================
elif opcion == "Estadísticas":
    st.header("ESTADÍSTICAS")
    
    if not st.session_state.estadisticas:
        st.info("Aún no hay partidas registradas")
        st.caption("Juega algunas partidas para ver estadísticas aquí")
        
        col_volver1, col_volver2 = st.columns(2)
        with col_volver1:
            if st.button("Jugar modo solitario", type="primary", use_container_width=True, key="btn_solitario_estadisticas"):
                st.session_state.opcion_menu = "Modo Solitario"
                st.session_state.partida_activa_solo = False
                st.session_state.resultado_mostrado_solo = False
                st.rerun()
        with col_volver2:
            if st.button("Jugar con amigos", type="primary", use_container_width=True, key="btn_j2_estadisticas"):
                st.session_state.opcion_menu = "Modo 2 Jugadores"
                st.session_state.fase_j2 = 1
                st.session_state.resultado_mostrado_j2 = False
                st.rerun()
    else:
        df = pd.DataFrame(st.session_state.estadisticas)
        
        st.info(f"Archivo de datos: {ARCHIVO_ESTADISTICAS} ({len(df)} partidas guardadas)")
        
        st.subheader("Filtros")
        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        
        with col_filtro1:
            filtrar_modo = st.multiselect(
                "Modo de juego:",
                options=sorted(df["Modo"].unique()),
                default=sorted(df["Modo"].unique()),
                key="filtro_modo"
            )
        
        with col_filtro2:
            filtrar_dificultad = st.multiselect(
                "Dificultad:",
                options=sorted(df["Dificultad"].unique()),
                default=sorted(df["Dificultad"].unique()),
                key="filtro_dificultad"
            )
        
        with col_filtro3:
            filtrar_resultado = st.multiselect(
                "Resultado:",
                options=sorted(df["Resultado"].unique()),
                default=sorted(df["Resultado"].unique()),
                key="filtro_resultado"
            )
        
        df_filtrado = df.copy()
        
        if filtrar_modo:
            df_filtrado = df_filtrado[df_filtrado["Modo"].isin(filtrar_modo)]
        if filtrar_dificultad:
            df_filtrado = df_filtrado[df_filtrado["Dificultad"].isin(filtrar_dificultad)]
        if filtrar_resultado:
            df_filtrado = df_filtrado[df_filtrado["Resultado"].isin(filtrar_resultado)]
        
        st.subheader("Resumen general")
        
        col_met1, col_met2, col_met3, col_met4, col_met5 = st.columns(5)
        
        with col_met1:
            total = len(df_filtrado)
            st.metric("Total partidas", total)
        
        with col_met2:
            ganadas = len(df_filtrado[df_filtrado["Resultado"] == "Ganado"])
            st.metric("Partidas ganadas", ganadas)
        
        with col_met3:
            perdidas = len(df_filtrado[df_filtrado["Resultado"] == "Perdido"])
            st.metric("Partidas perdidas", perdidas)
        
        with col_met4:
            if total > 0:
                tasa_exito = (ganadas / total) * 100
                st.metric("Tasa de éxito", f"{tasa_exito:.1f}%")
            else:
                st.metric("Tasa de éxito", "0%")
        
        with col_met5:
            if ganadas > 0:
                mejor_nota = df_filtrado["Nota"].max()
                st.metric("Mejor nota", f"{mejor_nota:.2f}")
            else:
                st.metric("Mejor nota", "0.00")
        
        st.subheader("Historial detallado")
        
        st.dataframe(
            df_filtrado.sort_values("Fecha", ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Fecha": st.column_config.DatetimeColumn(
                    "Fecha",
                    format="DD/MM/YY HH:mm"
                ),
                "Nota": st.column_config.NumberColumn(
                    "Nota",
                    format="%.2f",
                    help="Puntuación de 0 a 10"
                )
            }
        )
        
        st.subheader("Gráficos y análisis")
        
        tab_graf1, tab_graf2, tab_graf3 = st.tabs(["Por dificultad", "Por jugador", "Evolución"])
        
        with tab_graf1:
            if not df_filtrado.empty:
                stats_dif = df_filtrado.groupby("Dificultad").agg({
                    "Nota": "mean",
                    "Resultado": lambda x: (x == "Ganado").mean() * 100
                }).round(2)
                
                col_graf1_1, col_graf1_2 = st.columns(2)
                with col_graf1_1:
                    st.bar_chart(stats_dif["Nota"])
                    st.caption("Nota promedio por dificultad")
                
                with col_graf1_2:
                    st.bar_chart(stats_dif["Resultado"])
                    st.caption("% de victorias por dificultad")
        
        with tab_graf2:
            if not df_filtrado.empty:
                jugadores = pd.concat([
                    df_filtrado[["Jugador1", "Nota", "Resultado"]].rename(columns={"Jugador1": "Jugador"}),
                    df_filtrado[df_filtrado["Jugador2"] != ""][["Jugador2", "Nota", "Resultado"]].rename(columns={"Jugador2": "Jugador"})
                ])
                
                if not jugadores.empty:
                    stats_jug = jugadores.groupby("Jugador").agg({
                        "Nota": ["count", "mean", "max"],
                        "Resultado": lambda x: (x == "Ganado").mean() * 100
                    }).round(2)
                    
                    stats_jug.columns = ["Partidas", "Nota Promedio", "Mejor Nota", "% Victorias"]
                    st.dataframe(stats_jug.sort_values("Nota Promedio", ascending=False))
        
        with tab_graf3:
            if len(df_filtrado) > 1:
                df_filtrado["Fecha_dt"] = pd.to_datetime(df_filtrado["Fecha"])
                df_filtrado = df_filtrado.sort_values("Fecha_dt")
                
                st.line_chart(df_filtrado.set_index("Fecha_dt")["Nota"])
                st.caption("Evolución de tu puntuación")
        
        st.subheader("Exportar datos")
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            csv = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name="estadisticas_adivinanza.csv",
                mime="text/csv",
                use_container_width=True,
                key="btn_descargar_csv"
            )
        
        with col_exp2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtrado.to_excel(writer, index=False, sheet_name='Estadísticas')
            
            st.download_button(
                label="Descargar Excel",
                data=output.getvalue(),
                file_name="estadisticas_adivinanza.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="btn_descargar_excel"
            )
        
        st.markdown("---")
        col_limpiar1, col_limpiar2, col_limpiar3 = st.columns(3)
        with col_limpiar2:
            if st.button("Limpiar todas las estadísticas", type="secondary", use_container_width=True, key="btn_limpiar_estadisticas"):
                st.session_state.estadisticas = []
                try:
                    if os.path.exists(ARCHIVO_ESTADISTICAS):
                        os.remove(ARCHIVO_ESTADISTICAS)
                except:
                    pass
                st.success("Estadísticas limpiadas")
                st.rerun()

# =================== INSTRUCCIONES ===================
elif opcion == "Instrucciones":
    st.header("INSTRUCCIONES DETALLADAS")
    
    tab_inst1, tab_inst2, tab_inst3 = st.tabs(["Cómo jugar", "Sistema de puntuación", "Consejos"])
    
    with tab_inst1:
        st.markdown("""
        ## OBJETIVO DEL JUEGO
        Adivinar un número secreto entre 1 y 1000 en la menor cantidad de intentos posible.
        
        ---
        
        ## MODO SOLITARIO
        
        ### Paso a paso:
        1. Ingresa tu nombre
        2. Selecciona la dificultad:
           - Fácil: 20 intentos
           - Medio: 12 intentos  
           - Difícil: 5 intentos
        
        3. Comienza a jugar:
           - Ingresa tu adivinanza
           - El sistema te dirá si el número secreto es MAYOR o MENOR
           - ¡Sigue intentando hasta adivinarlo!
        
        4. Resultado:
           - Si adivinas: ¡CORRECTO! (puedes volver a jugar)
           - Si se acaban los intentos: ¡INCORRECTO! (puedes volver a intentar)
        
        ---
        
        ## MODO 2 JUGADORES
        
        ### Para el Jugador 1 (piensa el número):
        1. Ingresa tu nombre
        2. Elige un número secreto (1-1000)
        3. ¡No le digas a nadie el número!
        4. Configura la dificultad para el Jugador 2
        
        ### Para el Jugador 2 (adivina):
        1. Ingresa tu nombre
        2. Comienza a adivinar
        3. Recibirás pistas: MAYOR o MENOR
        4. Intenta adivinar antes de que se acaban los intentos
        5. Resultado: CORRECTO (ganas) o INCORRECTO (pierdes)
        
        ---
        
        ## ESTADÍSTICAS
        - Todas tus partidas se guardan automáticamente en un archivo CSV
        - Puedes filtrar por jugador, dificultad o resultado
        - Exporta tus datos a CSV o Excel
        - Los datos se conservan mientras el servidor esté activo
        """)
    
    with tab_inst2:
        st.markdown("""
        ## SISTEMA DE PUNTUACIÓN
        
        ### Fórmula de cálculo:
        ```
        NOTA = 10 × (Intentos restantes + 1) / Intentos totales
        ```
        
        ### Ejemplos:
        
        #### Dificultad Fácil (20 intentos):
        - Adivinas en 5 intentos:  
          `Nota = 10 × (20-5+1)/20 = 10 × 16/20 = 8.0`
        
        - Adivinas en 15 intentos:  
          `Nota = 10 × (20-15+1)/20 = 10 × 6/20 = 3.0`
        
        #### Dificultad Difícil (5 intentos):
        - Adivinas en 3 intentos:  
          `Nota = 10 × (5-3+1)/5 = 10 × 3/5 = 6.0`
        
        ### Cómo obtener mejor puntuación:
        1. Adivina más rápido (menos intentos = más puntos)
        2. Juega en dificultad alta (más riesgo = más recompensa)
        3. Enfócate en mejorar tu estrategia
        
        ### Escala de notas:
        - 9.0 - 10.0: Excelente  
        - 7.0 - 8.9: Muy bueno  
        - 5.0 - 6.9: Bueno  
        - 3.0 - 4.9: Aceptable  
        - 0.0 - 2.9: Sigue practicando
        """)
    
    with tab_inst3:
        st.markdown("""
        ## ESTRATEGIAS PARA GANAR
        
        ### Método de búsqueda binaria:
        1. Empieza con 500 (el punto medio)
        2. Si es mayor, prueba 750
        3. Si es menor, prueba 250
        4. Sigue dividiendo el rango por la mitad
        
        ### Estadísticas útiles:
        - 67% de los números están entre 300-700
        - Solo 10% están en los extremos (1-100, 900-1000)
        - El número 500 es el más común de adivinar
        
        ### Consejos rápidos:
        
        #### Para modo solitario:
        - Fácil: Tómate tu tiempo, explora diferentes rangos
        - Medio: Usa búsqueda binaria desde el inicio
        - Difícil: Arriesga más, confía en tu intuición
        
        #### Para modo 2 jugadores:
        - Jugador 1: Elige números inusuales (ej: 137, 842)
        - Jugador 2: Pregunta por rangos en lugar de números específicos
        
        ### Patrones comunes:
        1. Muchos jugadores eligen números que terminan en 0, 5 o 7
        2. Los números del 1 al 100 son más difíciles de adivinar
        3. Los números con dígitos repetidos (333, 777) son populares
        
        ### Récords a batir:
        - Nota perfecta 10.0: Adivinar en el primer intento
        - Racha ganadora: 5 partidas consecutivas ganadas
        - Reto extremo: Ganar en dificultad Difícil con nota >8.0
        """)
        
    st.markdown("---")
    st.subheader("¿Listo para jugar?")
    
    col_inst_btn1, col_inst_btn2 = st.columns(2)
    with col_inst_btn1:
        if st.button("Comenzar modo solitario", type="primary", use_container_width=True, key="btn_solitario_inst"):
            st.session_state.opcion_menu = "Modo Solitario"
            st.session_state.partida_activa_solo = False
            st.session_state.resultado_mostrado_solo = False
            st.rerun()
    with col_inst_btn2:
        if st.button("Comenzar con amigos", type="primary", use_container_width=True, key="btn_j2_inst"):
            st.session_state.opcion_menu = "Modo 2 Jugadores"
            st.session_state.fase_j2 = 1
            st.session_state.resultado_mostrado_j2 = False
            st.rerun()

# =================== ACERCA DE ===================
else:
    st.header("ACERCA DE ESTE PROYECTO")
    
    col_about1, col_about2 = st.columns([2, 1])
    
    with col_about1:
        st.markdown("""
        ## Juego de Adivinanza - Proyecto Educativo
        
        ### Características principales:
        - Dos modos de juego: Solitario y 2 jugadores
        - Tres niveles de dificultad: Fácil, Medio, Difícil
        - Sistema de puntuación inteligente: Notas del 0 al 10
        - Estadísticas guardadas en CSV: Datos persistentes
        - Interfaz moderna y responsive: Funciona en cualquier dispositivo
        
        ### Tecnologías utilizadas:
        - Python 3 + Streamlit para la interfaz web
        - Pandas para análisis de datos y guardado en CSV
        - OpenPyXL para manejo de archivos Excel
        - Random para generación de números aleatorios
        
        ### Propósito educativo:
        Este proyecto fue desarrollado como demostración de:
        - Programación en Python aplicada a juegos
        - Interfaz de usuario web con Streamlit
        - Manejo de datos y estadísticas con persistencia
        - Lógica de programación y algoritmos
        
        ### Licencia:
        Proyecto educativo - Libre para uso académico y personal.
        
        ### Código fuente:
        Disponible para fines educativos y de aprendizaje.
        """)
    
    with col_about2:
        st.info("Proyecto Educativo")
        st.success("100% Funcional")
        st.warning("Responsive Design")
        st.error("Alto Rendimiento")
        
        st.markdown("---")
        st.subheader("Datos del proyecto")
        
        st.metric("Partidas guardadas", len(st.session_state.estadisticas))
        st.metric("Funcionalidades", "15+")
        st.metric("Archivo de datos", ARCHIVO_ESTADISTICAS)
        
        st.markdown("---")
        
        st.subheader("Probar el juego")
        if st.button("Probar modo solitario", type="primary", use_container_width=True, key="btn_probar_solo"):
            st.session_state.opcion_menu = "Modo Solitario"
            st.session_state.partida_activa_solo = False
            st.session_state.resultado_mostrado_solo = False
            st.rerun()
        
        if st.button("Probar con amigos", type="secondary", use_container_width=True, key="btn_probar_j2"):
            st.session_state.opcion_menu = "Modo 2 Jugadores"
            st.session_state.fase_j2 = 1
            st.session_state.resultado_mostrado_j2 = False
            st.rerun()
        
        st.markdown("---")
        st.caption("Última actualización:")
        st.caption(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))

# =================== FOOTER ===================
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("Juego de Adivinanza v2.0")
with footer_col2:
    st.caption("Datos guardados en CSV")
with footer_col3:
    st.caption(f"{datetime.datetime.now().strftime('%H:%M')}")