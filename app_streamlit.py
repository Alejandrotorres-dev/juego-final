import streamlit as st
import random
import datetime
import pandas as pd
import io
import os

# =================== CONFIGURACIÓN INICIAL ===================
st.set_page_config(
    page_title="Juego de Adivinanza",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== ESTILOS CSS ===================
st.markdown("""
<style>
/* Ocultar elementos de Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
#stDecoration {display:none;}
[data-testid="stToolbar"] {display:none;}
[data-testid="stDecoration"] {display:none;}
[data-testid="stStatusWidget"] {display:none;}
.css-1lsmgbg {display: none;}

/* Ajustes de layout */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-top: 0rem;
}

h1 {
    margin-top: 0rem;
    padding-top: 0rem;
}

/* Botones grandes */
.stButton > button {
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Mensajes */
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

/* Contenedores */
.contenedor-juego {
    background: #f8f9fa;
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    border: 2px solid #dee2e6;
}
</style>
""", unsafe_allow_html=True)

# =================== INICIALIZACIÓN DE SESSION STATE ===================

# Variable CRÍTICA para navegación - controla qué página mostrar
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "inicio"

# Variables para modo SOLITARIO
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
if 'resultado_solo' not in st.session_state:
    st.session_state.resultado_solo = None  # "ganado", "perdido", o None

# Variables para modo 2 JUGADORES
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
    st.session_state.fase_j2 = 1  # 1: Jugador1 elige, 2: Jugador2 adivina
if 'resultado_j2' not in st.session_state:
    st.session_state.resultado_j2 = None  # "ganado", "perdido", o None

# Estadísticas
ARCHIVO_ESTADISTICAS = "estadisticas_partidas.csv"
if 'estadisticas' not in st.session_state:
    try:
        if os.path.exists(ARCHIVO_ESTADISTICAS):
            df = pd.read_csv(ARCHIVO_ESTADISTICAS)
            st.session_state.estadisticas = df.to_dict('records')
        else:
            st.session_state.estadisticas = []
    except Exception as e:
        st.session_state.estadisticas = []

# =================== FUNCIONES DEL JUEGO ===================

def guardar_estadisticas():
    """Guarda las estadísticas en CSV"""
    try:
        if st.session_state.estadisticas:
            df = pd.DataFrame(st.session_state.estadisticas)
            df.to_csv(ARCHIVO_ESTADISTICAS, index=False)
    except Exception as e:
        pass  # Silenciar errores en la nube

def guardar_partida(modo, jugador1, jugador2, dificultad, numero_secreto, intentos, ganado):
    """Guarda una partida en las estadísticas"""
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resultado = "Ganado" if ganado else "Perdido"
    
    max_intentos = st.session_state.max_intentos_solo if modo == "Solitario" else st.session_state.max_intentos_j2
    
    if ganado:
        nota = round((max_intentos - intentos + 1) / max_intentos * 10, 2)
    else:
        nota = 0.0
    
    st.session_state.estadisticas.append({
        "Fecha": fecha,
        "Modo": modo,
        "Jugador1": jugador1,
        "Jugador2": jugador2 or "",
        "Dificultad": dificultad,
        "Número Secreto": "***" if ganado else numero_secreto,
        "Intentos Usados": intentos,
        "Max Intentos": max_intentos,
        "Resultado": resultado,
        "Nota": nota
    })
    guardar_estadisticas()

def sugerir_dificultad(numero):
    """Sugiere dificultad basada en el número"""
    if numero <= 100 or numero >= 900:
        return "Está en un extremo, más difícil de adivinar."
    elif numero <= 300 or numero >= 700:
        return "Algo alejado del centro, dificultad media recomendada."
    else:
        return "Cerca del centro, más fácil de adivinar."

def navegar_a(pagina):
    """Función para cambiar de página - CRÍTICA para funcionamiento en web"""
    st.session_state.pagina_actual = pagina

def reiniciar_solitario():
    """Reinicia el estado del modo solitario"""
    st.session_state.numero_secreto_solo = None
    st.session_state.intentos_solo = 0
    st.session_state.jugador_solo = ""
    st.session_state.dificultad_solo = "Fácil"
    st.session_state.max_intentos_solo = 20
    st.session_state.partida_activa_solo = False
    st.session_state.resultado_solo = None

def reiniciar_dos_jugadores():
    """Reinicia el estado del modo 2 jugadores"""
    st.session_state.numero_secreto_j2 = None
    st.session_state.intentos_j2 = 0
    st.session_state.jugador1_nombre = ""
    st.session_state.jugador2_nombre = ""
    st.session_state.dificultad_j2 = "Fácil"
    st.session_state.max_intentos_j2 = 20
    st.session_state.fase_j2 = 1
    st.session_state.resultado_j2 = None

# =================== PÁGINA DE INICIO ===================

def mostrar_inicio():
    """Muestra la página principal"""
    st.title("🎯 JUEGO DE ADIVINANZA")
    st.markdown("---")
    
    st.header("Bienvenido al Juego de Adivinanza")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## ¿Cómo funciona?
        
        **¡Adivina el número secreto entre 1 y 1000!**
        
        ### Modos de juego:
        
        **🎮 Modo Solitario**  
        • Juega contra la computadora  
        • Elige entre 3 niveles de dificultad  
        • Intenta adivinar el número en pocos intentos
        
        **👥 Modo 2 Jugadores**  
        • Un jugador piensa el número  
        • Otro intenta adivinarlo  
        • ¡Perfecto para jugar con amigos!
        
        ### 📊 Sistema de puntuación:
        • + puntos por adivinar rápido  
        • + puntos por mayor dificultad  
        • Nota final de 0 a 10
        """)
    
    with col2:
        # Mostrar récord
        st.markdown("### 🏆 RÉCORD ACTUAL")
        if st.session_state.estadisticas:
            mejor_partida = max(st.session_state.estadisticas, key=lambda x: x["Nota"])
            st.success(f"**Mejor nota:** {mejor_partida['Nota']}/10")
            st.info(f"**Por:** {mejor_partida['Jugador1']}")
            st.caption(f"Modo: {mejor_partida['Modo']} | Dificultad: {mejor_partida['Dificultad']}")
        else:
            st.info("Aún no hay partidas jugadas")
            st.caption("¡Sé el primero en establecer un récord!")
        
        st.markdown("---")
        
        st.markdown("### 🚀 COMENZAR A JUGAR")
        
        # BOTÓN 1: MODO SOLITARIO
        if st.button(
            "🎮 JUGAR MODO SOLITARIO", 
            key="btn_solitario_inicio",
            use_container_width=True,
            type="primary",
            help="Jugar contra la computadora"
        ):
            reiniciar_solitario()
            navegar_a("solitario")
            st.rerun()
        
        # BOTÓN 2: MODO 2 JUGADORES
        if st.button(
            "👥 JUGAR CON AMIGOS", 
            key="btn_j2_inicio",
            use_container_width=True,
            type="secondary",
            help="Jugar con otra persona"
        ):
            reiniciar_dos_jugadores()
            navegar_a("dos_jugadores")
            st.rerun()
        
        st.markdown("---")
        
        # Otros accesos rápidos
        col_acc1, col_acc2 = st.columns(2)
        with col_acc1:
            if st.button("📊 Ver Estadísticas", key="btn_estad_inicio", use_container_width=True):
                navegar_a("estadisticas")
                st.rerun()
        with col_acc2:
            if st.button("📖 Instrucciones", key="btn_inst_inicio", use_container_width=True):
                navegar_a("instrucciones")
                st.rerun()

# =================== MODO SOLITARIO ===================

def mostrar_solitario():
    """Muestra la página del modo solitario"""
    st.title("🎮 MODO SOLITARIO")
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← Volver al inicio", key="btn_volver_solo"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown("---")
    
    # Mostrar resultado si existe
    if st.session_state.resultado_solo is not None:
        if st.session_state.resultado_solo == "ganado":
            st.markdown(f"""
            <div class="mensaje-correcto">
            <h3>🎉 ¡FELICIDADES {st.session_state.jugador_solo.upper()}!</h3>
            <p><strong>✅ Has ganado en {st.session_state.intentos_solo} intentos</strong></p>
            <p>Número secreto: <strong>{st.session_state.numero_secreto_solo}</strong></p>
            <p>Dificultad: {st.session_state.dificultad_solo}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="mensaje-incorrecto">
            <h3>😞 ¡SE ACABARON LOS INTENTOS!</h3>
            <p><strong>❌ No lograste adivinar el número</strong></p>
            <p>El número era: <strong>{st.session_state.numero_secreto_solo}</strong></p>
            <p>Dificultad: {st.session_state.dificultad_solo}</p>
            <p>Intentos usados: {st.session_state.intentos_solo}/{st.session_state.max_intentos_solo}</p>
            </div>
            """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Jugar otra partida", type="primary", use_container_width=True, key="btn_reiniciar_solo"):
                reiniciar_solitario()
                st.rerun()
        with col_btn2:
            if st.button("📊 Ver estadísticas", use_container_width=True, key="btn_estad_solo"):
                navegar_a("estadisticas")
                st.rerun()
        
        st.markdown("---")
    
    # Configuración de nueva partida
    if not st.session_state.partida_activa_solo:
        st.subheader("📝 Configura tu partida")
        
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            nombre = st.text_input(
                "Tu nombre:", 
                placeholder="Ej: Carlos", 
                key="nombre_solo_input",
                value=st.session_state.jugador_solo if st.session_state.jugador_solo else ""
            )
            
            st.subheader("🎯 Dificultad")
            dificultad_opcion = st.selectbox(
                "Selecciona la dificultad:",
                ["Fácil", "Medio", "Difícil"],
                index=0,
                key="dificultad_select"
            )
            
            if dificultad_opcion == "Fácil":
                max_intentos = 20
                st.info("🟢 **Fácil:** 20 intentos")
            elif dificultad_opcion == "Medio":
                max_intentos = 12
                st.warning("🟡 **Medio:** 12 intentos")
            else:
                max_intentos = 5
                st.error("🔴 **Difícil:** Solo 5 intentos")
        
        with col_config2:
            st.subheader("📋 Reglas del juego")
            st.markdown(f"""
            ### Objetivo:
            Adivinar el número secreto entre **1 y 1000**
            
            ### Tienes:
            **{max_intentos} intentos** máximo
            
            ### Pistas:
            • Te diré si el número es **MAYOR** o **MENOR**
            • ¡Usa la estrategia de búsqueda binaria!
            
            ### ¿Listo para jugar?
            """)
            
            if st.button("▶️ COMENZAR PARTIDA", type="primary", use_container_width=True, key="btn_comenzar_solo"):
                if nombre and nombre.strip():
                    st.session_state.jugador_solo = nombre.strip()
                    st.session_state.dificultad_solo = dificultad_opcion
                    st.session_state.max_intentos_solo = max_intentos
                    st.session_state.numero_secreto_solo = random.randint(1, 1000)
                    st.session_state.intentos_solo = 0
                    st.session_state.partida_activa_solo = True
                    st.session_state.resultado_solo = None
                    st.rerun()
                else:
                    st.error("⚠️ Por favor, ingresa tu nombre")
    
    # Juego activo
    elif st.session_state.partida_activa_solo:
        st.markdown(f"""
        <div class="contenedor-juego">
        <h3>🎯 PARTIDA ACTIVA - {st.session_state.jugador_solo}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_juego1, col_juego2 = st.columns([2, 1])
        
        with col_juego1:
            st.subheader("🔢 Haz tu adivinanza")
            
            adivinanza = st.number_input(
                "Ingresa un número (1-1000):",
                min_value=1,
                max_value=1000,
                step=1,
                key="adivinanza_input_solo",
                help="Presiona Enter o usa los botones para ajustar"
            )
            
            col_btn_intentar, col_btn_cancelar = st.columns(2)
            with col_btn_intentar:
                if st.button("🎯 INTENTAR", type="primary", use_container_width=True, key="btn_intentar_solo"):
                    st.session_state.intentos_solo += 1
                    
                    if adivinanza == st.session_state.numero_secreto_solo:
                        st.session_state.resultado_solo = "ganado"
                        guardar_partida(
                            "Solitario",
                            st.session_state.jugador_solo,
                            "",
                            st.session_state.dificultad_solo,
                            st.session_state.numero_secreto_solo,
                            st.session_state.intentos_solo,
                            True
                        )
                        st.rerun()
                    
                    elif adivinanza < st.session_state.numero_secreto_solo:
                        st.warning(f"📈 **MAYOR** - El número secreto es mayor que {adivinanza}")
                    else:
                        st.warning(f"📉 **MENOR** - El número secreto es menor que {adivinanza}")
                    
                    if st.session_state.intentos_solo >= st.session_state.max_intentos_solo:
                        st.session_state.resultado_solo = "perdido"
                        guardar_partida(
                            "Solitario",
                            st.session_state.jugador_solo,
                            "",
                            st.session_state.dificultad_solo,
                            st.session_state.numero_secreto_solo,
                            st.session_state.intentos_solo,
                            False
                        )
                        st.rerun()
            
            with col_btn_cancelar:
                if st.button("❌ Cancelar partida", use_container_width=True, key="btn_cancelar_solo"):
                    st.session_state.partida_activa_solo = False
                    st.rerun()
        
        with col_juego2:
            st.subheader("📊 Estado de la partida")
            
            st.metric(
                "Intentos usados",
                f"{st.session_state.intentos_solo} / {st.session_state.max_intentos_solo}"
            )
            
            progreso = st.session_state.intentos_solo / st.session_state.max_intentos_solo
            st.progress(min(progreso, 1.0))
            
            st.info(f"🎯 **Dificultad:** {st.session_state.dificultad_solo}")
            st.info(f"👤 **Jugador:** {st.session_state.jugador_solo}")
            
            if st.session_state.intentos_solo > 0:
                with st.expander("💡 Pistas estadísticas", expanded=True):
                    if adivinanza < st.session_state.numero_secreto_solo:
                        st.success(f"Prueba con números entre **{adivinanza + 1}** y **1000**")
                        rango_min = adivinanza + 1
                        rango_max = 1000
                    elif adivinanza > st.session_state.numero_secreto_solo:
                        st.success(f"Prueba con números entre **1** y **{adivinanza - 1}**")
                        rango_min = 1
                        rango_max = adivinanza - 1
                    else:
                        rango_min = 1
                        rango_max = 1000
                    
                    st.caption(f"Rango recomendado: {rango_min} - {rango_max}")
                    
                    intentos_restantes = st.session_state.max_intentos_solo - st.session_state.intentos_solo
                    st.warning(f"⏱️ **Intentos restantes:** {intentos_restantes}")

# =================== MODO 2 JUGADORES ===================

def mostrar_dos_jugadores():
    """Muestra la página del modo 2 jugadores"""
    st.title("👥 MODO 2 JUGADORES")
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← Volver al inicio", key="btn_volver_j2"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown("---")
    
    # Mostrar resultado si existe
    if st.session_state.resultado_j2 is not None:
        if st.session_state.resultado_j2 == "ganado":
            st.markdown(f"""
            <div class="mensaje-correcto">
            <h3>🎉 ¡{st.session_state.jugador2_nombre.upper()} HA GANADO!</h3>
            <p><strong>✅ Adivinó en {st.session_state.intentos_j2} intentos</strong></p>
            <p>Número secreto: <strong>{st.session_state.numero_secreto_j2}</strong></p>
            <p>Dificultad: {st.session_state.dificultad_j2}</p>
            <p>Jugador 1: {st.session_state.jugador1_nombre}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="mensaje-incorrecto">
            <h3>😞 ¡SE ACABARON LOS INTENTOS!</h3>
            <p><strong>❌ No lograste adivinar el número</strong></p>
            <p>El número era: <strong>{st.session_state.numero_secreto_j2}</strong></p>
            <p>Dificultad: {st.session_state.dificultad_j2}</p>
            <p>Jugador 1: {st.session_state.jugador1_nombre}</p>
            <p>Intentos usados: {st.session_state.intentos_j2}/{st.session_state.max_intentos_j2}</p>
            </div>
            """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Jugar otra partida", type="primary", use_container_width=True, key="btn_reiniciar_j2"):
                reiniciar_dos_jugadores()
                st.rerun()
        with col_btn2:
            if st.button("📊 Ver estadísticas", use_container_width=True, key="btn_estad_j2"):
                navegar_a("estadisticas")
                st.rerun()
        
        st.markdown("---")
    
    # FASE 1: Jugador 1 elige el número
    if st.session_state.fase_j2 == 1:
        st.subheader("👤 FASE 1: Jugador 1 (Piensa el número)")
        
        col_j1_1, col_j1_2 = st.columns(2)
        
        with col_j1_1:
            jugador1 = st.text_input(
                "Nombre del Jugador 1:", 
                placeholder="Ej: Ana",
                key="jugador1_input",
                value=st.session_state.jugador1_nombre if st.session_state.jugador1_nombre else ""
            )
            
            numero_secreto = st.number_input(
                "Número secreto (1-1000):",
                min_value=1,
                max_value=1000,
                step=1,
                key="numero_secreto_input",
                help="¡No le digas a nadie el número!",
                value=st.session_state.numero_secreto_j2 if st.session_state.numero_secreto_j2 else 500
            )
            
            if numero_secreto:
                sugerencia = sugerir_dificultad(numero_secreto)
                st.info(f"💡 **Sugerencia:** {sugerencia}")
        
        with col_j1_2:
            st.subheader("🎯 Configurar dificultad")
            dificultad_j2_opcion = st.selectbox(
                "Dificultad para el Jugador 2:",
                ["Fácil", "Medio", "Difícil"],
                index=0,
                key="dificultad_j2_select"
            )
            
            if dificultad_j2_opcion == "Fácil":
                max_j2 = 20
                st.info("🟢 **Fácil:** 20 intentos")
            elif dificultad_j2_opcion == "Medio":
                max_j2 = 12
                st.warning("🟡 **Medio:** 12 intentos")
            else:
                max_j2 = 5
                st.error("🔴 **Difícil:** Solo 5 intentos")
            
            st.markdown("---")
            st.markdown("### 📋 Instrucciones para Jugador 1:")
            st.markdown("""
            1. ✅ Ingresa tu nombre
            2. ✅ Elige un número secreto
            3. ✅ Configura la dificultad
            4. ✅ Presiona REGISTRAR
            5. 🔄 Pasa el dispositivo al Jugador 2
            """)
            
            if st.button("✅ REGISTRAR NÚMERO", type="primary", use_container_width=True, key="btn_registrar_j2"):
                if jugador1 and jugador1.strip() and 1 <= numero_secreto <= 1000:
                    st.session_state.jugador1_nombre = jugador1.strip()
                    st.session_state.numero_secreto_j2 = int(numero_secreto)
                    st.session_state.dificultad_j2 = dificultad_j2_opcion
                    st.session_state.max_intentos_j2 = max_j2
                    st.session_state.fase_j2 = 2
                    st.session_state.intentos_j2 = 0
                    st.session_state.resultado_j2 = None
                    st.rerun()
                else:
                    st.error("⚠️ Completa todos los campos correctamente")
    
    # FASE 2: Jugador 2 adivina
    elif st.session_state.fase_j2 == 2:
        if st.session_state.numero_secreto_j2 is None:
            st.error("Error: No se configuró el número secreto. Vuelve a la fase 1.")
            if st.button("↩️ Volver a fase 1", key="btn_volver_fase1"):
                st.session_state.fase_j2 = 1
                st.rerun()
        else:
            st.subheader("👤 FASE 2: Jugador 2 (Adivina el número)")
            
            col_j2_1, col_j2_2 = st.columns(2)
            
            with col_j2_1:
                jugador2 = st.text_input(
                    "Nombre del Jugador 2:",
                    placeholder="Ej: Luis",
                    key="jugador2_input",
                    value=st.session_state.jugador2_nombre if st.session_state.jugador2_nombre else ""
                )
                
                if jugador2 or st.session_state.jugador2_nombre:
                    jugador_actual = jugador2 or st.session_state.jugador2_nombre
                    st.success(f"🎯 **Reto:** Adivina el número de {st.session_state.jugador1_nombre}")
                    st.info(f"📊 **Dificultad:** {st.session_state.dificultad_j2}")
                    st.warning(f"⏱️ **Intentos disponibles:** {st.session_state.max_intentos_j2 - st.session_state.intentos_j2}")
                    
                    adivinanza_j2 = st.number_input(
                        "Tu adivinanza:",
                        min_value=1,
                        max_value=1000,
                        step=1,
                        key="adivinanza_j2_input"
                    )
                    
                    if st.button("🎯 INTENTAR ADIVINAR", type="primary", use_container_width=True, key="btn_intentar_j2"):
                        if jugador2 and jugador2.strip():
                            st.session_state.jugador2_nombre = jugador2.strip()
                        
                        st.session_state.intentos_j2 += 1
                        
                        if adivinanza_j2 == st.session_state.numero_secreto_j2:
                            st.session_state.resultado_j2 = "ganado"
                            guardar_partida(
                                "2 Jugadores",
                                st.session_state.jugador1_nombre,
                                st.session_state.jugador2_nombre,
                                st.session_state.dificultad_j2,
                                st.session_state.numero_secreto_j2,
                                st.session_state.intentos_j2,
                                True
                            )
                            st.rerun()
                        
                        elif adivinanza_j2 < st.session_state.numero_secreto_j2:
                            st.warning(f"📈 **MAYOR** - Intenta con un número más grande que {adivinanza_j2}")
                        else:
                            st.warning(f"📉 **MENOR** - Intenta con un número más pequeño que {adivinanza_j2}")
                        
                        if st.session_state.intentos_j2 >= st.session_state.max_intentos_j2:
                            st.session_state.resultado_j2 = "perdido"
                            guardar_partida(
                                "2 Jugadores",
                                st.session_state.jugador1_nombre,
                                st.session_state.jugador2_nombre,
                                st.session_state.dificultad_j2,
                                st.session_state.numero_secreto_j2,
                                st.session_state.intentos_j2,
                                False
                            )
                            st.rerun()
            
            with col_j2_2:
                jugador_actual = st.session_state.jugador2_nombre or jugador2 or "Jugador 2"
                st.subheader(f"📊 Estado - {jugador_actual}")
                
                st.metric(
                    "Intentos usados",
                    f"{st.session_state.intentos_j2} / {st.session_state.max_intentos_j2}"
                )
                
                progreso_j2 = st.session_state.intentos_j2 / st.session_state.max_intentos_j2
                st.progress(min(progreso_j2, 1.0))
                
                st.info(f"🎮 **Contra:** {st.session_state.jugador1_nombre}")
                st.info(f"📈 **Dificultad:** {st.session_state.dificultad_j2}")
                
                if st.session_state.intentos_j2 > 0:
                    with st.expander("💡 Estrategia recomendada"):
                        if adivinanza_j2 < st.session_state.numero_secreto_j2:
                            st.success(f"Prueba entre **{adivinanza_j2 + 1}** y **1000**")
                        elif adivinanza_j2 > st.session_state.numero_secreto_j2:
                            st.success(f"Prueba entre **1** y **{adivinanza_j2 - 1}**")
                        else:
                            st.info("¡Empieza por el medio (500)!")
                
                if st.button("❌ Cancelar partida", use_container_width=True, key="btn_cancelar_j2"):
                    st.session_state.fase_j2 = 1
                    st.session_state.resultado_j2 = None
                    st.rerun()

# =================== ESTADÍSTICAS ===================

def mostrar_estadisticas():
    """Muestra la página de estadísticas"""
    st.title("📊 ESTADÍSTICAS")
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← Volver al inicio", key="btn_volver_estad"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown("---")
    
    if not st.session_state.estadisticas:
        st.info("📭 Aún no hay partidas registradas")
        st.caption("Juega algunas partidas para ver estadísticas aquí")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🎮 Jugar modo solitario", type="primary", use_container_width=True, key="btn_ir_solo_estad"):
                navegar_a("solitario")
                st.rerun()
        with col_btn2:
            if st.button("👥 Jugar con amigos", type="secondary", use_container_width=True, key="btn_ir_j2_estad"):
                navegar_a("dos_jugadores")
                st.rerun()
    else:
        df = pd.DataFrame(st.session_state.estadisticas)
        
        st.info(f"📁 **Archivo de datos:** {ARCHIVO_ESTADISTICAS} ({len(df)} partidas guardadas)")
        
        # Filtros - CORREGIDO: usar list() en lugar de tolist()
        st.subheader("🔍 Filtros")
        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        
        with col_filtro1:
            # CORRECCIÓN APLICADA: list(df["Modo"].unique())
            modos = sorted(list(df["Modo"].unique()))
            filtrar_modo = st.multiselect(
                "Modo de juego:",
                options=modos,
                default=modos,
                key="filtro_modo"
            )
        
        with col_filtro2:
            # CORRECCIÓN APLICADA: list(df["Dificultad"].unique())
            dificultades = sorted(list(df["Dificultad"].unique()))
            filtrar_dificultad = st.multiselect(
                "Dificultad:",
                options=dificultades,
                default=dificultades,
                key="filtro_dificultad"
            )
        
        with col_filtro3:
            # CORRECCIÓN APLICADA: list(df["Resultado"].unique())
            resultados = sorted(list(df["Resultado"].unique()))
            filtrar_resultado = st.multiselect(
                "Resultado:",
                options=resultados,
                default=resultados,
                key="filtro_resultado"
            )
        
        # Aplicar filtros
        df_filtrado = df.copy()
        if filtrar_modo:
            df_filtrado = df_filtrado[df_filtrado["Modo"].isin(filtrar_modo)]
        if filtrar_dificultad:
            df_filtrado = df_filtrado[df_filtrado["Dificultad"].isin(filtrar_dificultad)]
        if filtrar_resultado:
            df_filtrado = df_filtrado[df_filtrado["Resultado"].isin(filtrar_resultado)]
        
        # Métricas
        st.subheader("📈 Resumen general")
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
            if not df_filtrado.empty:
                mejor_nota = df_filtrado["Nota"].max()
                st.metric("Mejor nota", f"{mejor_nota:.2f}")
            else:
                st.metric("Mejor nota", "0.00")
        
        # Tabla de datos
        st.subheader("📋 Historial detallado")
        
        # Mostrar mensaje si no hay datos después de filtrar
        if df_filtrado.empty:
            st.warning("⚠️ No hay partidas que coincidan con los filtros seleccionados")
            st.caption("Prueba a cambiar los filtros para ver más resultados")
        else:
            st.dataframe(
                df_filtrado.sort_values("Fecha", ascending=False),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Fecha": st.column_config.DatetimeColumn("Fecha", format="DD/MM/YY HH:mm"),
                    "Nota": st.column_config.NumberColumn("Nota", format="%.2f", help="Puntuación de 0 a 10"),
                    "Número Secreto": st.column_config.TextColumn("Número", help="*** si fue ganado")
                }
            )
        
        # Exportar datos - SOLO si hay datos filtrados
        if not df_filtrado.empty:
            st.subheader("💾 Exportar datos")
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                csv = df_filtrado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar CSV",
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
                    label="📥 Descargar Excel",
                    data=output.getvalue(),
                    file_name="estadisticas_adivinanza.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="btn_descargar_excel"
                )
        
        # Limpiar estadísticas
        st.markdown("---")
        if st.button("🗑️ Limpiar todas las estadísticas", type="secondary", use_container_width=True, key="btn_limpiar_estad"):
            st.session_state.estadisticas = []
            try:
                if os.path.exists(ARCHIVO_ESTADISTICAS):
                    os.remove(ARCHIVO_ESTADISTICAS)
            except:
                pass
            st.success("✅ Estadísticas limpiadas correctamente")
            st.rerun()

# =================== INSTRUCCIONES ===================

def mostrar_instrucciones():
    """Muestra la página de instrucciones"""
    st.title("📖 INSTRUCCIONES DETALLADAS")
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← Volver al inicio", key="btn_volver_inst"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown("---")
    
    # Pestañas
    tab1, tab2, tab3 = st.tabs(["🎮 Cómo jugar", "🏆 Sistema de puntuación", "💡 Consejos"])
    
    with tab1:
        st.markdown("""
        ## 🎯 OBJETIVO DEL JUEGO
        Adivinar un número secreto entre **1 y 1000** en la menor cantidad de intentos posible.
        
        ---
        
        ## 🎮 MODO SOLITARIO
        
        ### Paso a paso:
        1. **Ingresa tu nombre**
        2. **Selecciona la dificultad:**
           - 🟢 **Fácil:** 20 intentos
           - 🟡 **Medio:** 12 intentos  
           - 🔴 **Difícil:** 5 intentos
        
        3. **Comienza a jugar:**
           - Ingresa tu adivinanza
           - El sistema te dirá si el número secreto es **MAYOR** o **MENOR**
           - ¡Sigue intentando hasta adivinarlo!
        
        4. **Resultado:**
           - ✅ **Si adivinas:** ¡FELICIDADES! (puedes volver a jugar)
           - ❌ **Si se acaban los intentos:** ¡INTÉNTALO DE NUEVO!
        
        ---
        
        ## 👥 MODO 2 JUGADORES
        
        ### Para el **Jugador 1** (piensa el número):
        1. Ingresa tu nombre
        2. Elige un número secreto (1-1000)
        3. **¡No le digas a nadie el número!**
        4. Configura la dificultad para el Jugador 2
        
        ### Para el **Jugador 2** (adivina):
        1. Ingresa tu nombre
        2. Comienza a adivinar
        3. Recibirás pistas: **MAYOR** o **MENOR**
        4. Intenta adivinar antes de que se acaben los intentos
        5. **Resultado:** ✅ CORRECTO (ganas) o ❌ INCORRECTO (pierdes)
        
        ---
        
        ## 📊 ESTADÍSTICAS
        - Todas tus partidas se guardan automáticamente en un archivo CSV
        - Puedes filtrar por jugador, dificultad o resultado
        - Exporta tus datos a CSV o Excel
        - Los datos se conservan mientras uses la misma sesión
        """)
    
    with tab2:
        st.markdown("""
        ## 🏆 SISTEMA DE PUNTUACIÓN
        
        ### 📐 Fórmula de cálculo:
        ```
        NOTA = 10 × (Intentos restantes + 1) / Intentos totales
        ```
        
        ### 📊 Ejemplos:
        
        #### Dificultad **Fácil** (20 intentos):
        - ✅ Adivinas en **5 intentos**:  
          `Nota = 10 × (20-5+1)/20 = 10 × 16/20 = 8.0`
        
        - ✅ Adivinas en **15 intentos**:  
          `Nota = 10 × (20-15+1)/20 = 10 × 6/20 = 3.0`
        
        #### Dificultad **Difícil** (5 intentos):
        - ✅ Adivinas en **3 intentos**:  
          `Nota = 10 × (5-3+1)/5 = 10 × 3/5 = 6.0`
        
        ### 🎯 Cómo obtener mejor puntuación:
        1. **Adivina más rápido** (menos intentos = más puntos)
        2. **Juega en dificultad alta** (más riesgo = más recompensa)
        3. **Mejora tu estrategia** de adivinanza
        
        ### 📈 Escala de notas:
        - **9.0 - 10.0:** 🏅 Excelente  
        - **7.0 - 8.9:** 🥈 Muy bueno  
        - **5.0 - 6.9:** 🥉 Bueno  
        - **3.0 - 4.9:** ✅ Aceptable  
        - **0.0 - 2.9:** 📚 Sigue practicando
        """)
    
    with tab3:
        st.markdown("""
        ## 💡 ESTRATEGIAS PARA GANAR
        
        ### 🔍 Método de búsqueda binaria (RECOMENDADO):
        1. Empieza con **500** (el punto medio)
        2. Si es mayor, prueba **750**
        3. Si es menor, prueba **250**
        4. Sigue dividiendo el rango por la mitad
        
        ### 📊 Estadísticas útiles:
        - **67%** de los números están entre **300-700**
        - Solo **10%** están en los extremos (1-100, 900-1000)
        - El número **500** es el más común de adivinar
        
        ### 🎮 Consejos por modo:
        
        #### Para **modo solitario:**
        - **Fácil:** Tómate tu tiempo, explora diferentes rangos
        - **Medio:** Usa búsqueda binaria desde el inicio
        - **Difícil:** Arriesga más, confía en tu intuición
        
        #### Para **modo 2 jugadores:**
        - **Jugador 1:** Elige números inusuales (ej: 137, 842, 369)
        - **Jugador 2:** Pregunta por rangos amplios primero
        
        ### 🎲 Patrones comunes:
        1. Muchos jugadores eligen números que terminan en **0, 5 o 7**
        2. Los números del **1 al 100** son más difíciles de adivinar
        3. Los números con **dígitos repetidos** (333, 777) son populares
        
        ### 🏅 Récords a batir:
        - **Nota perfecta 10.0:** Adivinar en el primer intento
        - **Racha ganadora:** 5 partidas consecutivas ganadas
        - **Reto extremo:** Ganar en dificultad **Difícil** con nota >8.0
        """)
    
    st.markdown("---")
    st.subheader("🎮 ¿Listo para jugar?")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🎮 Comenzar modo solitario", type="primary", use_container_width=True, key="btn_inst_solo"):
            navegar_a("solitario")
            st.rerun()
    with col_btn2:
        if st.button("👥 Comenzar con amigos", type="secondary", use_container_width=True, key="btn_inst_j2"):
            navegar_a("dos_jugadores")
            st.rerun()

# =================== ACERCA DE ===================

def mostrar_acerca_de():
    """Muestra la página acerca de"""
    st.title("ℹ️ ACERCA DE ESTE PROYECTO")
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← Volver al inicio", key="btn_volver_acerca"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown("---")
    
    col_about1, col_about2 = st.columns([2, 1])
    
    with col_about1:
        st.markdown("""
        ## 🎮 Juego de Adivinanza - Proyecto Educativo
        
        ### ✨ Características principales:
        - **Dos modos de juego:** Solitario y 2 jugadores
        - **Tres niveles de dificultad:** Fácil, Medio, Difícil
        - **Sistema de puntuación inteligente:** Notas del 0 al 10
        - **Estadísticas persistentes:** Guardado automático en CSV
        - **Interfaz moderna:** Responsive y amigable
        
        ### 🛠️ Tecnologías utilizadas:
        - **Python 3** + **Streamlit** para la interfaz web
        - **Pandas** para análisis de datos y CSV
        - **OpenPyXL** para exportación a Excel
        - **Random** para generación de números aleatorios
        
        ### 🎯 Propósito educativo:
        Este proyecto fue desarrollado como demostración de:
        - Programación en Python aplicada a juegos
        - Interfaz de usuario web con Streamlit
        - Manejo de datos y estadísticas
        - Lógica de programación y algoritmos
        
        ### 📄 Licencia:
        **Proyecto educativo** - Libre para uso académico y personal.
        
        ### 💻 Código fuente:
        Disponible para fines educativos y de aprendizaje.
        """)
    
    with col_about2:
        st.info("🎓 **Proyecto Educativo**")
        st.success("✅ **100% Funcional**")
        st.warning("📱 **Responsive Design**")
        st.error("⚡ **Alto Rendimiento**")
        
        st.markdown("---")
        st.subheader("📊 Datos del proyecto")
        
        st.metric("Partidas guardadas", len(st.session_state.estadisticas))
        st.metric("Funcionalidades", "15+")
        st.metric("Archivo de datos", ARCHIVO_ESTADISTICAS)
        
        st.markdown("---")
        
        st.subheader("🎮 Probar el juego")
        if st.button("🎮 Probar modo solitario", type="primary", use_container_width=True, key="btn_probar_solo"):
            navegar_a("solitario")
            st.rerun()
        
        if st.button("👥 Probar con amigos", type="secondary", use_container_width=True, key="btn_probar_j2"):
            navegar_a("dos_jugadores")
            st.rerun()
        
        st.markdown("---")
        st.caption(f"🕐 **Última actualización:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")

# =================== ROUTER PRINCIPAL ===================

def main():
    """Función principal que decide qué página mostrar"""
    
    # Determinar qué página mostrar basado en session_state
    pagina = st.session_state.get('pagina_actual', 'inicio')
    
    if pagina == "inicio":
        mostrar_inicio()
    elif pagina == "solitario":
        mostrar_solitario()
    elif pagina == "dos_jugadores":
        mostrar_dos_jugadores()
    elif pagina == "estadisticas":
        mostrar_estadisticas()
    elif pagina == "instrucciones":
        mostrar_instrucciones()
    elif pagina == "acerca_de":
        mostrar_acerca_de()
    else:
        mostrar_inicio()  # Por defecto
    
    # Footer común
    st.markdown("---")
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.caption("🎮 Juego de Adivinanza v3.0")
    with footer_col2:
        st.caption("📊 Datos guardados en CSV")
    with footer_col3:
        st.caption(f"🕐 {datetime.datetime.now().strftime('%H:%M:%S')}")

# =================== EJECUCIÓN ===================

if __name__ == "__main__":
    main()