import streamlit as st
import random
import datetime 
import pandas as pd
import io
import os
from io import BytesIO
import json

try:
    # Streamlit >= 1.30
    query_params = dict(st.query_params)
except AttributeError:
    # Streamlit < 1.30 (fallback)
    query_params = st.experimental_get_query_params()

# Función auxiliar para obtener parámetros de forma segura
def get_param(key, default=''):
    """Obtiene un parámetro de la URL de forma segura"""
    try:
        value = query_params.get(key, default)
        # Si es lista, tomar el primer elemento
        if isinstance(value, list):
            return value[0] if value else default
        return value if value else default
    except:
        return default

# ===== ENDPOINT 1: PING (?ping=true) - OPTIMIZADO =====
if get_param('ping').lower() == 'true':
    # Respuesta ultra-simple y rápida
    st.write("✅ STREAMLIT APP ACTIVE")
    st.write(f"🕐 {dt.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write("🟢 Status: RUNNING")
    st.stop()

# ===== ENDPOINT 2: HEALTH CHECK (?health=check) - OPTIMIZADO =====
if get_param('health').lower() == 'check':
    # JSON simple y rápido
    health = {
        "status": "healthy",
        "timestamp": dt.now().isoformat(),
        "service": "juego-final-alejandro-torres"
    }
    st.json(health)
    st.stop()

# ===== ENDPOINT 3: STATUS (?status=1) - ULTRA-LIGERO =====
if get_param('status') == '1':
    st.success("OK")
    st.stop()

# =================== CONFIGURACIÓN INICIAL ===================
st.set_page_config(
    page_title="Juego de Adivinanza",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== CSS STYLE ===================
app_css = """
<style>
    /* Variables de diseño */
    :root {
        --primary-color: #0066B3;
        --primary-light: #0099FF;
        --primary-dark: #004C8F;
        --success-color: #00A86B;
        --error-color: #E4002B;
        --warning-color: #FFC107;
        --dark-bg: #0D0D0D;
        --medium-bg: #1A1A1A;
        --light-bg: #2D2D2D;
        --text-light: #FFFFFF;
        --text-muted: #CCCCCC;
        --border-color: #333333;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    #stDecoration {display:none;}
    [data-testid="stToolbar"] {display:none;}
    [data-testid="stDecoration"] {display:none;}
    [data-testid="stStatusWidget"] {display:none;}
    
    /* Fondo principal */
    .main {
        background: linear-gradient(135deg, var(--dark-bg) 0%, var(--medium-bg) 100%) !important;
        color: var(--text-light);
        min-height: 100vh;
    }
    
    /* Contenido principal */
    .block-container {
        background: transparent !important;
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    /* Títulos */
    h1, h2, h3, h4 {
        font-weight: 700;
        color: var(--text-light);
        margin-top: 0;
    }
    
    h1 {
        font-size: 48px;
        background: linear-gradient(90deg, var(--text-light), var(--primary-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 24px;
        text-align: center;
        position: relative;
        padding-bottom: 15px;
    }
    
    h1:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
        border-radius: 2px;
    }
    
    /* Tarjetas */
    .app-card {
        background: linear-gradient(145deg, var(--medium-bg) 0%, var(--light-bg) 100%);
        border-radius: 8px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .app-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--primary-color), var(--primary-light));
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%) !important;
        color: var(--text-light) !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 12px 28px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 102, 179, 0.3) !important;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary-color) 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 153, 255, 0.4) !important;
    }
    
    /* Métricas */
    .metric-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        background: linear-gradient(135deg, var(--dark-bg) 0%, var(--light-bg) 100%);
        border-radius: 8px;
        border: 1px solid var(--border-color);
        min-height: 120px;
        position: relative;
        overflow: hidden;
    }
    
    .metric-value {
        font-size: 42px;
        font-weight: 700;
        background: linear-gradient(90deg, var(--primary-light), var(--text-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        margin-bottom: 5px;
    }
    
    .metric-label {
        font-size: 12px;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    /* Mensajes */
    .mensaje-correcto {
        background: linear-gradient(135deg, rgba(0, 168, 107, 0.1) 0%, rgba(0, 133, 82, 0.05) 100%);
        border: 2px solid rgba(0, 168, 107, 0.3);
        border-radius: 8px;
        padding: 25px;
        margin: 20px 0;
        color: var(--text-light);
    }
    
    .mensaje-incorrecto {
        background: linear-gradient(135deg, rgba(228, 0, 43, 0.1) 0%, rgba(179, 0, 30, 0.05) 100%);
        border: 2px solid rgba(228, 0, 43, 0.3);
        border-radius: 8px;
        padding: 25px;
        margin: 20px 0;
        color: var(--text-light);
    }
    
    /* Número secreto */
    .numero-secreto {
        font-size: 56px;
        font-weight: 800;
        background: linear-gradient(90deg, var(--primary-light), #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 20px 0;
        text-shadow: 0 0 20px rgba(0, 153, 255, 0.3);
    }
    
    /* Separadores */
    .separator {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: 30px 0;
    }
    
    /* Tablas */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .dataframe th {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
        color: var(--text-light);
        font-weight: 600;
        padding: 16px;
        text-align: left;
    }
    
    .dataframe td {
        padding: 14px 16px;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-muted);
        background: var(--light-bg);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0 4px;
    }
    
    .badge-success {
        background: rgba(0, 168, 107, 0.2);
        color: #00A86B;
        border: 1px solid rgba(0, 168, 107, 0.4);
    }
    
    .badge-error {
        background: rgba(228, 0, 43, 0.2);
        color: var(--error-color);
        border: 1px solid rgba(228, 0, 43, 0.4);
    }
    
    /* Contenedor de juego */
    .contenedor-juego {
        background: linear-gradient(145deg, var(--dark-bg) 0%, var(--medium-bg) 100%);
        border-radius: 8px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Footer */
    .footer-app {
        background: var(--dark-bg);
        border-top: 1px solid var(--border-color);
        padding: 20px;
        margin-top: 40px;
        text-align: center;
        color: var(--text-muted);
        font-size: 12px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        h1 {
            font-size: 36px;
        }
        
        .metric-value {
            font-size: 32px;
        }
        
        .app-card {
            padding: 20px;
        }
        
        .numero-secreto {
            font-size: 42px;
        }
    }
</style>
"""

# Aplicar el CSS
st.markdown(app_css, unsafe_allow_html=True)

# INICIALIZACIÓN DE SESSION STATE 

# Variable para navegación
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
    st.session_state.resultado_solo = None

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
    st.session_state.fase_j2 = 1
if 'resultado_j2' not in st.session_state:
    st.session_state.resultado_j2 = None

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

#  FUNCIONES DEL JUEGO 

def guardar_estadisticas():
    """Guarda las estadísticas en CSV"""
    try:
        if st.session_state.estadisticas:
            df = pd.DataFrame(st.session_state.estadisticas)
            df.to_csv(ARCHIVO_ESTADISTICAS, index=False)
    except Exception as e:
        pass

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
    """Función para cambiar de página"""
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

# PÁGINA DE INICIO

def mostrar_inicio():
    """Muestra la página principal"""
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.title("JUEGO DE ADIVINANZA")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ##  ¿CÓMO FUNCIONA?
        
        **¡Adivina el número secreto entre 1 y 1000!**
        
        ### MODOS DE JUEGO:
        
        **🔹 MODO SOLITARIO**  
        • Juega contra la computadora  
        • Elige entre 3 niveles de dificultad  
        
        **🔹 MODO 2 JUGADORES**  
        • Un jugador piensa el número  
        • Otro intenta adivinarlo  
        • ¡Perfecto para jugar con amigos!
        """)
    
    with col2:
        st.markdown("### 🏆 RÉCORD ACTUAL")
        if st.session_state.estadisticas:
            mejor_partida = max(st.session_state.estadisticas, key=lambda x: x["Nota"])
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{mejor_partida["Nota"]:.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">MEJOR NOTA</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption(f"**POR:** {mejor_partida['Jugador1']} | **MODO:** {mejor_partida['Modo']}")
        else:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">0.00</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">MEJOR NOTA</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        st.markdown("###  COMENZAR A JUGAR")
        
        if st.button(
            "JUGAR MODO SOLITARIO", 
            key="btn_solitario_inicio",
            use_container_width=True
        ):
            reiniciar_solitario()
            navegar_a("solitario")
            st.rerun()
        
        if st.button(
            "👥 JUGAR CON AMIGOS", 
            key="btn_j2_inicio",
            use_container_width=True,
            type="secondary"
        ):
            reiniciar_dos_jugadores()
            navegar_a("dos_jugadores")
            st.rerun()
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        st.markdown("### ACCESOS RÁPIDOS")
        col_acc1, col_acc2 = st.columns(2)
        with col_acc1:
            if st.button("📊 ESTADÍSTICAS", key="btn_estad_inicio", use_container_width=True):
                navegar_a("estadisticas")
                st.rerun()
        with col_acc2:
            if st.button("📖 INSTRUCCIONES", key="btn_inst_inicio", use_container_width=True):
                navegar_a("instrucciones")
                st.rerun()

#MODO SOLITARIO 

def mostrar_solitario():
    """Muestra la página del modo solitario"""
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.title("🎮 MODO SOLITARIO")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← VOLVER AL INICIO", key="btn_volver_solo", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    if st.session_state.resultado_solo is not None:
        if st.session_state.resultado_solo == "ganado":
            st.markdown(f"""
            <div class="mensaje-correcto">
            <h3>🎉 ¡FELICIDADES {st.session_state.jugador_solo.upper()}!</h3>
            <p><strong>✅ HAS GANADO EN {st.session_state.intentos_solo} INTENTOS</strong></p>
            <div class="numero-secreto">{st.session_state.numero_secreto_solo}</div>
            <p><span class="badge badge-success">VICTORIA</span> • DIFICULTAD: {st.session_state.dificultad_solo}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="mensaje-incorrecto">
            <h3>😞 ¡SE ACABARON LOS INTENTOS!</h3>
            <p><strong>❌ NO LOGRAMOS ADIVINAR EL NÚMERO</strong></p>
            <div class="numero-secreto">{st.session_state.numero_secreto_solo}</div>
            <p><span class="badge badge-error">DERROTA</span> • DIFICULTAD: {st.session_state.dificultad_solo}</p>
            <p>INTENTOS USADOS: {st.session_state.intentos_solo}/{st.session_state.max_intentos_solo}</p>
            </div>
            """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 JUGAR OTRA PARTIDA", use_container_width=True, key="btn_reiniciar_solo"):
                reiniciar_solitario()
                st.rerun()
        with col_btn2:
            if st.button("📊 VER ESTADÍSTICAS", use_container_width=True, type="secondary", key="btn_estad_solo"):
                navegar_a("estadisticas")
                st.rerun()
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    if not st.session_state.partida_activa_solo:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("⚙️ CONFIGURA TU PARTIDA")
        
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            nombre = st.text_input(
                "TU NOMBRE:", 
                placeholder="EJ: CARLOS", 
                key="nombre_solo_input",
                value=st.session_state.jugador_solo if st.session_state.jugador_solo else ""
            )
            
            st.subheader("🎯 DIFICULTAD")
            dificultad_opcion = st.selectbox(
                "SELECCIONA LA DIFICULTAD:",
                ["Fácil", "Medio", "Difícil"],
                index=0,
                key="dificultad_select"
            )
            
            if dificultad_opcion == "Fácil":
                max_intentos = 20
                st.info("🟢 **FÁCIL:** 20 INTENTOS")
            elif dificultad_opcion == "Medio":
                max_intentos = 12
                st.warning("🟡 **MEDIO:** 12 INTENTOS")
            else:
                max_intentos = 5
                st.error("🔴 **DIFÍCIL:** SOLO 5 INTENTOS")
        
        with col_config2:
            st.subheader("📋 REGLAS DEL JUEGO")
            st.markdown(f"""
            ### OBJETIVO:
            ADIVINAR EL NÚMERO SECRETO ENTRE **1 Y 1000**
            
            ### TIENES:
            **{max_intentos} INTENTOS** MÁXIMO
            
            ### PISTAS:
            • TE DIRÉ SI EL NÚMERO ES **MAYOR** O **MENOR**
            """)
            
            if st.button("▶️ COMENZAR PARTIDA", use_container_width=True, key="btn_comenzar_solo"):
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
                    st.error("⚠️ POR FAVOR, INGRESA TU NOMBRE")
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.partida_activa_solo:
        st.markdown(f"""
        <div class="contenedor-juego">
        <h3>🎯 PARTIDA ACTIVA - {st.session_state.jugador_solo}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_juego1, col_juego2 = st.columns([2, 1])
        
        with col_juego1:
            st.markdown('<div class="app-card">', unsafe_allow_html=True)
            st.subheader("🔢 HAZ TU ADIVINANZA")
            
            adivinanza = st.number_input(
                "INGRESA UN NÚMERO (1-1000):",
                min_value=1,
                max_value=1000,
                step=1,
                key="adivinanza_input_solo"
            )
            
            col_btn_intentar, col_btn_cancelar = st.columns(2)
            with col_btn_intentar:
                if st.button("🎯 INTENTAR", use_container_width=True, key="btn_intentar_solo"):
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
                        st.warning(f"📈 **MAYOR** - EL NÚMERO SECRETO ES MAYOR QUE {adivinanza}")
                    else:
                        st.warning(f"📉 **MENOR** - EL NÚMERO SECRETO ES MENOR QUE {adivinanza}")
                    
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
                if st.button("❌ CANCELAR PARTIDA", use_container_width=True, type="secondary", key="btn_cancelar_solo"):
                    st.session_state.partida_activa_solo = False
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_juego2:
            st.markdown('<div class="app-card">', unsafe_allow_html=True)
            st.subheader("📊 ESTADO DE LA PARTIDA")
            
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{st.session_state.intentos_solo}/{st.session_state.max_intentos_solo}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">INTENTOS USADOS</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            progreso = st.session_state.intentos_solo / st.session_state.max_intentos_solo
            st.progress(min(progreso, 1.0))
            
            st.info(f"🎯 **DIFICULTAD:** {st.session_state.dificultad_solo}")
            st.info(f"👤 **JUGADOR:** {st.session_state.jugador_solo}")
            st.markdown('</div>', unsafe_allow_html=True)

#  MODO 2 JUGADORES 

def mostrar_dos_jugadores():
    """Muestra la página del modo 2 jugadores"""
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.title("👥 MODO 2 JUGADORES")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← VOLVER AL INICIO", key="btn_volver_j2", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    if st.session_state.resultado_j2 is not None:
        if st.session_state.resultado_j2 == "ganado":
            st.markdown(f"""
            <div class="mensaje-correcto">
            <h3>🎉 ¡{st.session_state.jugador2_nombre.upper()} HA GANADO!</h3>
            <p><strong>✅ ADIVINÓ EN {st.session_state.intentos_j2} INTENTOS</strong></p>
            <div class="numero-secreto">{st.session_state.numero_secreto_j2}</div>
            <p><span class="badge badge-success">VICTORIA</span> • DIFICULTAD: {st.session_state.dificultad_j2}</p>
            <p>JUGADOR 1: {st.session_state.jugador1_nombre}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="mensaje-incorrecto">
            <h3>😞 ¡SE ACABARON LOS INTENTOS!</h3>
            <p><strong>❌ NO LOGRAMOS ADIVINAR EL NÚMERO</strong></p>
            <div class="numero-secreto">{st.session_state.numero_secreto_j2}</div>
            <p><span class="badge badge-error">DERROTA</span> • DIFICULTAD: {st.session_state.dificultad_j2}</p>
            <p>JUGADOR 1: {st.session_state.jugador1_nombre}</p>
            <p>INTENTOS USADOS: {st.session_state.intentos_j2}/{st.session_state.max_intentos_j2}</p>
            </div>
            """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 JUGAR OTRA PARTIDA", use_container_width=True, key="btn_reiniciar_j2"):
                reiniciar_dos_jugadores()
                st.rerun()
        with col_btn2:
            if st.button("📊 VER ESTADÍSTICAS", use_container_width=True, type="secondary", key="btn_estad_j2"):
                navegar_a("estadisticas")
                st.rerun()
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    if st.session_state.fase_j2 == 1:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("👤 FASE 1: JUGADOR 1 (PIENSA EL NÚMERO)")
        
        col_j1_1, col_j1_2 = st.columns(2)
        
        with col_j1_1:
            jugador1 = st.text_input(
                "NOMBRE DEL JUGADOR 1:", 
                placeholder="EJ: ANA",
                key="jugador1_input",
                value=st.session_state.jugador1_nombre if st.session_state.jugador1_nombre else ""
            )
            
            numero_secreto = st.number_input(
                "NÚMERO SECRETO (1-1000):",
                min_value=1,
                max_value=1000,
                step=1,
                key="numero_secreto_input",
                value=st.session_state.numero_secreto_j2 if st.session_state.numero_secreto_j2 else 500
            )
        
        with col_j1_2:
            st.subheader("🎯 CONFIGURAR DIFICULTAD")
            dificultad_j2_opcion = st.selectbox(
                "DIFICULTAD PARA EL JUGADOR 2:",
                ["Fácil", "Medio", "Difícil"],
                index=0,
                key="dificultad_j2_select"
            )
            
            if dificultad_j2_opcion == "Fácil":
                max_j2 = 20
                st.info("🟢 **FÁCIL:** 20 INTENTOS")
            elif dificultad_j2_opcion == "Medio":
                max_j2 = 12
                st.warning("🟡 **MEDIO:** 12 INTENTOS")
            else:
                max_j2 = 5
                st.error("🔴 **DIFÍCIL:** SOLO 5 INTENTOS")
            
            if st.button("✅ REGISTRAR NÚMERO", use_container_width=True, key="btn_registrar_j2"):
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
                    st.error("⚠️ COMPLETA TODOS LOS CAMPOS CORRECTAMENTE")
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.fase_j2 == 2:
        if st.session_state.numero_secreto_j2 is None:
            st.error("ERROR: NO SE CONFIGURÓ EL NÚMERO SECRETO. VUELVE A LA FASE 1.")
            if st.button("↩️ VOLVER A FASE 1", key="btn_volver_fase1", type="secondary"):
                st.session_state.fase_j2 = 1
                st.rerun()
        else:
            st.markdown('<div class="contenedor-juego">', unsafe_allow_html=True)
            st.subheader("👤 FASE 2: JUGADOR 2 (ADIVINA EL NÚMERO)")
            st.markdown('</div>', unsafe_allow_html=True)
            
            col_j2_1, col_j2_2 = st.columns(2)
            
            with col_j2_1:
                st.markdown('<div class="app-card">', unsafe_allow_html=True)
                jugador2 = st.text_input(
                    "NOMBRE DEL JUGADOR 2:",
                    placeholder="EJ: LUIS",
                    key="jugador2_input",
                    value=st.session_state.jugador2_nombre if st.session_state.jugador2_nombre else ""
                )
                
                if jugador2 or st.session_state.jugador2_nombre:
                    jugador_actual = jugador2 or st.session_state.jugador2_nombre
                    st.success(f"🎯 **RETO:** ADIVINA EL NÚMERO DE {st.session_state.jugador1_nombre}")
                    st.info(f"📊 **DIFICULTAD:** {st.session_state.dificultad_j2}")
                    st.warning(f"⏱️ **INTENTOS DISPONIBLES:** {st.session_state.max_intentos_j2 - st.session_state.intentos_j2}")
                    
                    adivinanza_j2 = st.number_input(
                        "TU ADIVINANZA:",
                        min_value=1,
                        max_value=1000,
                        step=1,
                        key="adivinanza_j2_input"
                    )
                    
                    if st.button("🎯 INTENTAR ADIVINAR", use_container_width=True, key="btn_intentar_j2"):
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
                            st.warning(f"📈 **MAYOR** - INTENTA CON UN NÚMERO MÁS GRANDE QUE {adivinanza_j2}")
                        else:
                            st.warning(f"📉 **MENOR** - INTENTA CON UN NÚMERO MÁS PEQUEÑO QUE {adivinanza_j2}")
                        
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
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_j2_2:
                st.markdown('<div class="app-card">', unsafe_allow_html=True)
                jugador_actual = st.session_state.jugador2_nombre or jugador2 or "JUGADOR 2"
                st.subheader(f"📊 ESTADO - {jugador_actual}")
                
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{st.session_state.intentos_j2}/{st.session_state.max_intentos_j2}</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">INTENTOS USADOS</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                progreso_j2 = st.session_state.intentos_j2 / st.session_state.max_intentos_j2
                st.progress(min(progreso_j2, 1.0))
                
                st.info(f"🎮 **CONTRA:** {st.session_state.jugador1_nombre}")
                st.info(f"📈 **DIFICULTAD:** {st.session_state.dificultad_j2}")
                
                if st.button("❌ CANCELAR PARTIDA", use_container_width=True, type="secondary", key="btn_cancelar_j2"):
                    st.session_state.fase_j2 = 1
                    st.session_state.resultado_j2 = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

#  ESTADÍSTICAS  SIN EXCEL

def mostrar_estadisticas():
    """Muestra la página de estadísticas - SIN openpyxl"""
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.title("📊 ESTADÍSTICAS")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← VOLVER AL INICIO", key="btn_volver_estad", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    if not st.session_state.estadisticas:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.info("📭 AÚN NO HAY PARTIDAS REGISTRADAS")
        st.caption("JUEGA ALGUNAS PARTIDAS PARA VER ESTADÍSTICAS AQUÍ")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🎮 JUGAR MODO SOLITARIO", use_container_width=True, key="btn_ir_solo_estad"):
                navegar_a("solitario")
                st.rerun()
        with col_btn2:
            if st.button("👥 JUGAR CON AMIGOS", use_container_width=True, type="secondary", key="btn_ir_j2_estad"):
                navegar_a("dos_jugadores")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        df = pd.DataFrame(st.session_state.estadisticas)
        
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.info(f"📁 **DATOS REGISTRADOS:** {len(df)} PARTIDAS")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filtros
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("🔍 FILTROS")
        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        
        with col_filtro1:
            modos = sorted(list(df["Modo"].unique()))
            filtrar_modo = st.multiselect(
                "MODO DE JUEGO:",
                options=modos,
                default=modos,
                key="filtro_modo"
            )
        
        with col_filtro2:
            dificultades = sorted(list(df["Dificultad"].unique()))
            filtrar_dificultad = st.multiselect(
                "DIFICULTAD:",
                options=dificultades,
                default=dificultades,
                key="filtro_dificultad"
            )
        
        with col_filtro3:
            resultados = sorted(list(df["Resultado"].unique()))
            filtrar_resultado = st.multiselect(
                "RESULTADO:",
                options=resultados,
                default=resultados,
                key="filtro_resultado"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Aplicar filtros
        df_filtrado = df.copy()
        if filtrar_modo:
            df_filtrado = df_filtrado[df_filtrado["Modo"].isin(filtrar_modo)]
        if filtrar_dificultad:
            df_filtrado = df_filtrado[df_filtrado["Dificultad"].isin(filtrar_dificultad)]
        if filtrar_resultado:
            df_filtrado = df_filtrado[df_filtrado["Resultado"].isin(filtrar_resultado)]
        
        # Métricas
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("📈 RESUMEN GENERAL")
        
        col_met1, col_met2, col_met3, col_met4, col_met5 = st.columns(5)
        
        with col_met1:
            total = len(df_filtrado)
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{total}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">TOTAL PARTIDAS</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_met2:
            ganadas = len(df_filtrado[df_filtrado["Resultado"] == "Ganado"])
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{ganadas}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">PARTIDAS GANADAS</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_met3:
            perdidas = len(df_filtrado[df_filtrado["Resultado"] == "Perdido"])
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{perdidas}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">PARTIDAS PERDIDAS</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_met4:
            if total > 0:
                tasa_exito = (ganadas / total) * 100
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{tasa_exito:.1f}%</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">TASA DE ÉXITO</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">0%</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">TASA DE ÉXITO</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col_met5:
            if not df_filtrado.empty:
                mejor_nota = df_filtrado["Nota"].max()
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{mejor_nota:.2f}</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">MEJOR NOTA</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">0.00</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">MEJOR NOTA</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tabla de datos - OPCIÓN 3: MOSTRAR EN PANTALLA
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.subheader("📋 HISTORIAL DETALLADO")
        
        if df_filtrado.empty:
            st.warning("⚠️ NO HAY PARTIDAS QUE COINCIDAN CON LOS FILTROS SELECCIONADOS")
        else:
            # Ordenar por fecha descendente
            df_filtrado = df_filtrado.sort_values("Fecha", ascending=False)
            
            # Mostrar como tabla interactiva
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Fecha": st.column_config.TextColumn("Fecha"),
                    "Nota": st.column_config.NumberColumn("Nota", format="%.2f"),
                    "Número Secreto": st.column_config.TextColumn("Número Secreto")
                }
            )
            
            # Mostrar también como tabla estática
            with st.expander("📄 VER COMO TABLA SIMPLE"):
                st.table(df_filtrado.head(20))
                
            # Mostrar datos en formato de texto
            with st.expander("📝 VER DATOS EN TEXTO"):
                st.code(df_filtrado.to_string(index=False), language='text')
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Exportar datos - SOLO CSV (SIN EXCEL)
        if not df_filtrado.empty:
            st.markdown('<div class="app-card">', unsafe_allow_html=True)
            st.subheader("💾 EXPORTAR DATOS")
            
            # Opción 1: Descargar CSV
            csv = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 DESCARGAR COMO CSV",
                data=csv,
                file_name="estadisticas_juego_adivinanza.csv",
                mime="text/csv",
                use_container_width=True,
                key="btn_descargar_csv"
            )
            
            # Opción 2: Copiar datos al portapapeles
            with st.expander("📋 COPIAR DATOS AL PORTAPAPELES"):
                datos_texto = df_filtrado.to_string(index=False)
                st.code(datos_texto, language='text')
                if st.button("📋 COPIAR TEXTO", key="btn_copiar_texto"):
                    st.success("Texto copiado (simulado - usa Ctrl+C)")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Limpiar estadísticas
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        if st.button("🗑️ LIMPIAR TODAS LAS ESTADÍSTICAS", type="secondary", use_container_width=True, key="btn_limpiar_estad"):
            st.session_state.estadisticas = []
            try:
                if os.path.exists(ARCHIVO_ESTADISTICAS):
                    os.remove(ARCHIVO_ESTADISTICAS)
            except:
                pass
            st.success("✅ ESTADÍSTICAS LIMPIADAS CORRECTAMENTE")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# =================== INSTRUCCIONES ===================

def mostrar_instrucciones():
    """Muestra la página de instrucciones"""
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.title("📖 INSTRUCCIONES")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← VOLVER AL INICIO", key="btn_volver_inst", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🎮 CÓMO JUGAR", "💡 CONSEJOS"])
    
    with tab1:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("""
        ## 🎯 OBJETIVO DEL JUEGO
        ADIVINAR UN NÚMERO SECRETO ENTRE **1 Y 1000**.
        
        ## 🎮 MODO SOLITARIO
        1. INGRESA TU NOMBRE
        2. SELECCIONA LA DIFICULTAD
        3. ADIVINA EL NÚMERO SECRETO
        4. RECIBIRÁS PISTAS: **MAYOR** O **MENOR**
        
        ## 👥 MODO 2 JUGADORES
        - **JUGADOR 1:** ELIGE UN NÚMERO SECRETO
        - **JUGADOR 2:** INTENTA ADIVINARLO
        - INTERCAMBIEN EL DISPOSITIVO ENTRE FASES
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("""
        ## 💡 ESTRATEGIAS
        - **EMPIEZA POR EL MEDIO** (500)
        - **USA BÚSQUEDA BINARIA:** DIVIDE EL RANGO POR LA MITAD
        - **APRENDE DE TUS ERRORES:** LAS PISTAS SON TU MEJOR ALIADO
        
        ## 🎯 DIFICULTADES
        - **FÁCIL:** 20 INTENTOS - PERFECTO PARA PRINCIPIANTES
        - **MEDIO:** 12 INTENTOS - UN BUEN DESAFÍO
        - **DIFÍCIL:** 5 INTENTOS - SOLO PARA EXPERTOS
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.subheader("🎮 ¿LISTO PARA JUGAR?")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🎮 COMENZAR MODO SOLITARIO", use_container_width=True, key="btn_inst_solo"):
            navegar_a("solitario")
            st.rerun()
    with col_btn2:
        if st.button("👥 COMENZAR CON AMIGOS", use_container_width=True, type="secondary", key="btn_inst_j2"):
            navegar_a("dos_jugadores")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

#ROUTER PRINCIPAL 

def main():
    """Función principal que decide qué página mostrar"""
    
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
    else:
        mostrar_inicio()
    
    # Footer
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown('<div class="app-card footer-app">', unsafe_allow_html=True)
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.caption("Juego de adivinanza v4.0")
    with footer_col2:
        st.caption("Alejandro Torres Morán")
    with footer_col3:
        st.caption(f"🕐 {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.markdown('</div>', unsafe_allow_html=True)

# =================== EJECUCIÓN ===================

if __name__ == "__main__":
    main()