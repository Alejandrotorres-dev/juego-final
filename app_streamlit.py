import streamlit as st
import random
import datetime
import pandas as pd
import io
import os
from io import BytesIO

# =================== CONFIGURACIÓN INICIAL ===================
st.set_page_config(
    page_title="Juego de Adivinanza BMW Edition",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== CSS BMW STYLE ===================
bmw_css = """
<style>
    /* Variables de diseño BMW */
    :root {
        --bmw-black: #000000;
        --bmw-dark: #0D0D0D;
        --bmw-gray: #1A1A1A;
        --bmw-light-gray: #2D2D2D;
        --bmw-blue: #0066B3;
        --bmw-blue-light: #0099FF;
        --bmw-blue-dark: #004C8F;
        --bmw-red: #E4002B;
        --bmw-white: #FFFFFF;
        --bmw-silver: #CCCCCC;
        --bmw-border: #333333;
        --bmw-shadow: rgba(0, 0, 0, 0.3);
        --bmw-glow: rgba(0, 153, 255, 0.3);
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
    .css-1lsmgbg {display: none;}
    
    /* Fondo principal estilo BMW */
    .main {
        background: linear-gradient(135deg, var(--bmw-black) 0%, var(--bmw-dark) 50%, var(--bmw-gray) 100%) !important;
        color: var(--bmw-white);
        font-family: 'BMW Type Next', 'Arial', sans-serif;
        min-height: 100vh;
    }
    
    /* Contenido principal */
    .block-container {
        background: transparent !important;
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    /* Títulos BMW */
    h1, h2, h3, h4 {
        font-family: 'BMW Type Next Bold', 'Arial Black', sans-serif;
        font-weight: 700;
        color: var(--bmw-white);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0;
    }
    
    h1 {
        font-size: 48px;
        background: linear-gradient(90deg, var(--bmw-white), var(--bmw-blue-light));
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
        background: linear-gradient(90deg, var(--bmw-blue), var(--bmw-blue-light));
        border-radius: 2px;
    }
    
    h2 {
        font-size: 32px;
        margin-bottom: 20px;
        color: var(--bmw-blue-light);
        border-left: 4px solid var(--bmw-blue);
        padding-left: 15px;
    }
    
    h3 {
        font-size: 24px;
        color: var(--bmw-silver);
        border-bottom: 2px solid var(--bmw-border);
        padding-bottom: 10px;
    }
    
    /* Sidebar estilo BMW */
    .css-1d391kg, .css-12oz5g7 {
        background: linear-gradient(180deg, var(--bmw-dark) 0%, var(--bmw-gray) 100%) !important;
        border-right: 1px solid var(--bmw-border) !important;
    }
    
    /* Tarjetas BMW */
    .bmw-card {
        background: linear-gradient(145deg, var(--bmw-gray) 0%, var(--bmw-light-gray) 100%);
        border-radius: 8px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid var(--bmw-border);
        box-shadow: 0 4px 15px var(--bmw-shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .bmw-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--bmw-blue), var(--bmw-blue-light));
    }
    
    .bmw-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px var(--bmw-shadow), 0 0 15px var(--bmw-glow);
        border-color: var(--bmw-blue);
    }
    
    /* Botones BMW */
    .stButton > button {
        background: linear-gradient(135deg, var(--bmw-blue) 0%, var(--bmw-blue-dark) 100%) !important;
        color: var(--bmw-white) !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 12px 28px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        font-family: 'BMW Type Next', 'Arial', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 102, 179, 0.3) !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--bmw-blue-light) 0%, var(--bmw-blue) 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 153, 255, 0.4) !important;
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 10px rgba(0, 102, 179, 0.4) !important;
    }
    
    /* Botones secundarios */
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: var(--bmw-blue-light) !important;
        border: 2px solid var(--bmw-blue) !important;
        box-shadow: none !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: rgba(0, 102, 179, 0.1) !important;
        border-color: var(--bmw-blue-light) !important;
        color: var(--bmw-white) !important;
    }
    
    /* Botones de éxito/error */
    .stButton > button.success-btn {
        background: linear-gradient(135deg, #00A86B 0%, #008552 100%) !important;
    }
    
    .stButton > button.error-btn {
        background: linear-gradient(135deg, var(--bmw-red) 0%, #B3001E 100%) !important;
    }
    
    /* Mensajes BMW */
    .mensaje-correcto {
        background: linear-gradient(135deg, rgba(0, 168, 107, 0.1) 0%, rgba(0, 133, 82, 0.05) 100%);
        border: 2px solid rgba(0, 168, 107, 0.3);
        border-radius: 8px;
        padding: 25px;
        margin: 20px 0;
        color: var(--bmw-white);
        position: relative;
        overflow: hidden;
    }
    
    .mensaje-correcto:before {
        content: '🏆';
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 40px;
        opacity: 0.2;
    }
    
    .mensaje-incorrecto {
        background: linear-gradient(135deg, rgba(228, 0, 43, 0.1) 0%, rgba(179, 0, 30, 0.05) 100%);
        border: 2px solid rgba(228, 0, 43, 0.3);
        border-radius: 8px;
        padding: 25px;
        margin: 20px 0;
        color: var(--bmw-white);
        position: relative;
        overflow: hidden;
    }
    
    .mensaje-incorrecto:before {
        content: '⚡';
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 40px;
        opacity: 0.2;
    }
    
    /* Métricas BMW */
    .metric-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        background: linear-gradient(135deg, var(--bmw-dark) 0%, var(--bmw-light-gray) 100%);
        border-radius: 8px;
        border: 1px solid var(--bmw-border);
        min-height: 120px;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--bmw-blue), var(--bmw-blue-light));
    }
    
    .metric-value {
        font-size: 42px;
        font-weight: 700;
        background: linear-gradient(90deg, var(--bmw-blue-light), var(--bmw-white));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        margin-bottom: 5px;
        font-family: 'BMW Type Next Bold', sans-serif;
    }
    
    .metric-label {
        font-size: 12px;
        color: var(--bmw-silver);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    /* Tablas BMW */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 15px var(--bmw-shadow);
        font-family: 'BMW Type Next', sans-serif;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, var(--bmw-blue-dark) 0%, var(--bmw-blue) 100%);
        color: var(--bmw-white);
        font-weight: 600;
        padding: 16px;
        text-align: left;
        border: none;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .dataframe td {
        padding: 14px 16px;
        border-bottom: 1px solid var(--bmw-border);
        color: var(--bmw-silver);
        font-size: 14px;
        background: var(--bmw-light-gray);
    }
    
    .dataframe tr:hover {
        background: rgba(0, 102, 179, 0.1);
    }
    
    /* Inputs BMW */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: var(--bmw-dark) !important;
        color: var(--bmw-white) !important;
        border-radius: 4px !important;
        border: 1px solid var(--bmw-border) !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        font-family: 'BMW Type Next', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: var(--bmw-blue) !important;
        box-shadow: 0 0 0 3px var(--bmw-glow) !important;
        outline: none !important;
    }
    
    /* Badges BMW */
    .badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0 4px;
        font-family: 'BMW Type Next', sans-serif;
    }
    
    .badge-success {
        background: rgba(0, 168, 107, 0.2);
        color: #00A86B;
        border: 1px solid rgba(0, 168, 107, 0.4);
    }
    
    .badge-error {
        background: rgba(228, 0, 43, 0.2);
        color: var(--bmw-red);
        border: 1px solid rgba(228, 0, 43, 0.4);
    }
    
    .badge-warning {
        background: rgba(255, 193, 7, 0.2);
        color: #FFC107;
        border: 1px solid rgba(255, 193, 7, 0.4);
    }
    
    .badge-info {
        background: rgba(0, 102, 179, 0.2);
        color: var(--bmw-blue-light);
        border: 1px solid rgba(0, 102, 179, 0.4);
    }
    
    /* Alertas BMW */
    .stAlert {
        border-radius: 8px;
        border-left: none;
        padding: 16px 20px;
        background: var(--bmw-light-gray);
        border: 1px solid var(--bmw-border);
        box-shadow: 0 4px 12px var(--bmw-shadow);
        font-family: 'BMW Type Next', sans-serif;
    }
    
    /* Progress bar BMW */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--bmw-blue), var(--bmw-blue-light));
        border-radius: 4px;
    }
    
    /* Separadores */
    .separator {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--bmw-border), transparent);
        margin: 30px 0;
    }
    
    /* Animaciones */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(0, 153, 255, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(0, 153, 255, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(0, 153, 255, 0);
        }
    }
    
    .bmw-card {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Contenedor de juego */
    .contenedor-juego {
        background: linear-gradient(145deg, var(--bmw-dark) 0%, var(--bmw-gray) 100%);
        border-radius: 8px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid var(--bmw-border);
        box-shadow: 0 4px 20px var(--bmw-shadow);
        animation: fadeInUp 0.5s ease;
        position: relative;
    }
    
    .contenedor-juego:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--bmw-blue), var(--bmw-blue-light));
    }
    
    /* Efectos especiales */
    .numero-secreto {
        font-size: 56px;
        font-weight: 800;
        background: linear-gradient(90deg, var(--bmw-blue-light), #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 20px 0;
        font-family: 'BMW Type Next Bold', sans-serif;
        text-shadow: 0 0 20px rgba(0, 153, 255, 0.3);
        animation: pulse 2s infinite;
    }
    
    .emoji-grande {
        font-size: 48px;
        text-align: center;
        margin: 20px 0;
        text-shadow: 0 0 10px rgba(0, 153, 255, 0.5);
    }
    
    /* Grid responsive */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    /* Chip BMW */
    .chip {
        display: inline-block;
        padding: 6px 15px;
        background: var(--bmw-dark);
        border: 1px solid var(--bmw-border);
        border-radius: 20px;
        font-size: 12px;
        color: var(--bmw-silver);
        margin: 5px;
        transition: all 0.3s ease;
    }
    
    .chip:hover {
        border-color: var(--bmw-blue);
        color: var(--bmw-blue-light);
    }
    
    /* Footer BMW */
    .footer-bmw {
        background: var(--bmw-black);
        border-top: 1px solid var(--bmw-border);
        padding: 20px;
        margin-top: 40px;
        text-align: center;
        color: var(--bmw-silver);
        font-size: 12px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        h1 {
            font-size: 36px;
        }
        
        h2 {
            font-size: 24px;
        }
        
        .metric-value {
            font-size: 32px;
        }
        
        .bmw-card {
            padding: 20px;
        }
        
        .numero-secreto {
            font-size: 42px;
        }
        
        .stButton > button {
            padding: 10px 20px !important;
            font-size: 13px !important;
        }
    }
    
    /* Estilo para selectores y multiselect */
    .stSelectbox > div > div {
        background: var(--bmw-dark) !important;
        color: var(--bmw-white) !important;
    }
    
    .stMultiSelect > div > div {
        background: var(--bmw-dark) !important;
        color: var(--bmw-white) !important;
    }
    
    /* Placeholder styling */
    ::placeholder {
        color: var(--bmw-silver) !important;
        opacity: 0.7 !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bmw-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--bmw-blue);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--bmw-blue-light);
    }
</style>
"""

# Aplicar el CSS
st.markdown(bmw_css, unsafe_allow_html=True)

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
    st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
    st.markdown('<div class="emoji-grande"></div>', unsafe_allow_html=True)
    st.title("JUEGO DE ADIVINANZA")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🎯 ¿CÓMO FUNCIONA?
        
        **¡Adivina el número secreto entre 1 y 1000!**
        
        ### MODOS DE JUEGO:
        
        **🔹 MODO SOLITARIO**  
        • Juega contra la computadora  
        • Elige entre 3 niveles de dificultad  
        • Intenta adivinar en pocos intentos
        
        **🔹 MODO 2 JUGADORES**  
        • Un jugador piensa el número  
        • Otro intenta adivinarlo  
        • ¡Perfecto para jugar con amigos!
        
        ### 📊 SISTEMA DE PUNTUACIÓN:
        • + puntos por adivinar rápido  
        • + puntos por mayor dificultad  
        • Nota final de 0 a 10
        """)
    
    with col2:
        # Mostrar récord
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
            st.caption("¡SÉ EL PRIMERO EN ESTABLECER UN RÉCORD!")
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        st.markdown("### 🚀 COMENZAR A JUGAR")
        
        # BOTÓN 1: MODO SOLITARIO
        if st.button(
            "🏎️ JUGAR MODO SOLITARIO", 
            key="btn_solitario_inicio",
            use_container_width=True,
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
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        # Otros accesos rápidos
        st.markdown("### 📍 ACCESOS RÁPIDOS")
        col_acc1, col_acc2 = st.columns(2)
        with col_acc1:
            if st.button("📊 ESTADÍSTICAS", key="btn_estad_inicio", use_container_width=True):
                navegar_a("estadisticas")
                st.rerun()
        with col_acc2:
            if st.button("📖 INSTRUCCIONES", key="btn_inst_inicio", use_container_width=True):
                navegar_a("instrucciones")
                st.rerun()

# =================== MODO SOLITARIO ===================

def mostrar_solitario():
    """Muestra la página del modo solitario"""
    st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
    st.title("🏎️ MODO SOLITARIO")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← VOLVER AL INICIO", key="btn_volver_solo", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # Mostrar resultado si existe
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
        
        st.markdown('<div class="grid-container">', unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 JUGAR OTRA PARTIDA", use_container_width=True, key="btn_reiniciar_solo"):
                reiniciar_solitario()
                st.rerun()
        with col_btn2:
            if st.button("📊 VER ESTADÍSTICAS", use_container_width=True, type="secondary", key="btn_estad_solo"):
                navegar_a("estadisticas")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # Configuración de nueva partida
    if not st.session_state.partida_activa_solo:
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
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
            • ¡USA LA ESTRATEGIA DE BÚSQUEDA BINARIA!
            
            ### ¿LISTO PARA JUGAR?
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
    
    # Juego activo
    elif st.session_state.partida_activa_solo:
        st.markdown(f"""
        <div class="contenedor-juego">
        <h3>🎯 PARTIDA ACTIVA - {st.session_state.jugador_solo}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_juego1, col_juego2 = st.columns([2, 1])
        
        with col_juego1:
            st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
            st.subheader("🔢 HAZ TU ADIVINANZA")
            
            adivinanza = st.number_input(
                "INGRESA UN NÚMERO (1-1000):",
                min_value=1,
                max_value=1000,
                step=1,
                key="adivinanza_input_solo",
                help="PRESIONA ENTER O USA LOS BOTONES PARA AJUSTAR"
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
            st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
            st.subheader("📊 ESTADO DE LA PARTIDA")
            
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{st.session_state.intentos_solo}/{st.session_state.max_intentos_solo}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">INTENTOS USADOS</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            progreso = st.session_state.intentos_solo / st.session_state.max_intentos_solo
            st.progress(min(progreso, 1.0))
            
            st.info(f"🎯 **DIFICULTAD:** {st.session_state.dificultad_solo}")
            st.info(f"👤 **JUGADOR:** {st.session_state.jugador_solo}")
            
            if st.session_state.intentos_solo > 0:
                with st.expander("💡 PISTAS ESTADÍSTICAS", expanded=True):
                    if adivinanza < st.session_state.numero_secreto_solo:
                        st.success(f"PRUEBA CON NÚMEROS ENTRE **{adivinanza + 1}** Y **1000**")
                        rango_min = adivinanza + 1
                        rango_max = 1000
                    elif adivinanza > st.session_state.numero_secreto_solo:
                        st.success(f"PRUEBA CON NÚMEROS ENTRE **1** Y **{adivinanza - 1}**")
                        rango_min = 1
                        rango_max = adivinanza - 1
                    else:
                        rango_min = 1
                        rango_max = 1000
                    
                    st.caption(f"RANGO RECOMENDADO: {rango_min} - {rango_max}")
                    
                    intentos_restantes = st.session_state.max_intentos_solo - st.session_state.intentos_solo
                    st.warning(f"⏱️ **INTENTOS RESTANTES:** {intentos_restantes}")
            st.markdown('</div>', unsafe_allow_html=True)

# =================== MODO 2 JUGADORES ===================

def mostrar_dos_jugadores():
    """Muestra la página del modo 2 jugadores"""
    st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
    st.title("👥 MODO 2 JUGADORES")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← VOLVER AL INICIO", key="btn_volver_j2", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # Mostrar resultado si existe
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
        
        st.markdown('<div class="grid-container">', unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 JUGAR OTRA PARTIDA", use_container_width=True, key="btn_reiniciar_j2"):
                reiniciar_dos_jugadores()
                st.rerun()
        with col_btn2:
            if st.button("📊 VER ESTADÍSTICAS", use_container_width=True, type="secondary", key="btn_estad_j2"):
                navegar_a("estadisticas")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # FASE 1: Jugador 1 elige el número
    if st.session_state.fase_j2 == 1:
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
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
                help="¡NO LE DIGAS A NADIE EL NÚMERO!",
                value=st.session_state.numero_secreto_j2 if st.session_state.numero_secreto_j2 else 500
            )
            
            if numero_secreto:
                sugerencia = sugerir_dificultad(numero_secreto)
                st.info(f"💡 **SUGERENCIA:** {sugerencia}")
        
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
            
            st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
            st.markdown("### 📋 INSTRUCCIONES PARA JUGADOR 1:")
            st.markdown("""
            1. ✅ INGRESA TU NOMBRE
            2. ✅ ELIGE UN NÚMERO SECRETO
            3. ✅ CONFIGURA LA DIFICULTAD
            4. ✅ PRESIONA REGISTRAR
            5. 🔄 PASA EL DISPOSITIVO AL JUGADOR 2
            """)
            
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
    
    # FASE 2: Jugador 2 adivina
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
                st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
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
                st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
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
                
                if st.session_state.intentos_j2 > 0:
                    with st.expander("💡 ESTRATEGIA RECOMENDADA", expanded=True):
                        if adivinanza_j2 < st.session_state.numero_secreto_j2:
                            st.success(f"PRUEBA ENTRE **{adivinanza_j2 + 1}** Y **1000**")
                        elif adivinanza_j2 > st.session_state.numero_secreto_j2:
                            st.success(f"PRUEBA ENTRE **1** Y **{adivinanza_j2 - 1}**")
                        else:
                            st.info("¡EMPIEZA POR EL MEDIO (500)!")
                
                if st.button("❌ CANCELAR PARTIDA", use_container_width=True, type="secondary", key="btn_cancelar_j2"):
                    st.session_state.fase_j2 = 1
                    st.session_state.resultado_j2 = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# =================== ESTADÍSTICAS ===================

def mostrar_estadisticas():
    """Muestra la página de estadísticas"""
    st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
    st.title("📊 ESTADÍSTICAS")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← VOLVER AL INICIO", key="btn_volver_estad", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    if not st.session_state.estadisticas:
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
        st.info("📭 AÚN NO HAY PARTIDAS REGISTRADAS")
        st.caption("JUEGA ALGUNAS PARTIDAS PARA VER ESTADÍSTICAS AQUÍ")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🏎️ JUGAR MODO SOLITARIO", use_container_width=True, key="btn_ir_solo_estad"):
                navegar_a("solitario")
                st.rerun()
        with col_btn2:
            if st.button("👥 JUGAR CON AMIGOS", use_container_width=True, type="secondary", key="btn_ir_j2_estad"):
                navegar_a("dos_jugadores")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        df = pd.DataFrame(st.session_state.estadisticas)
        
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
        st.info(f"📁 **ARCHIVO DE DATOS:** {ARCHIVO_ESTADISTICAS} ({len(df)} PARTIDAS GUARDADAS)")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filtros
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
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
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
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
        
        # Tabla de datos
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
        st.subheader("📋 HISTORIAL DETALLADO")
        
        # Mostrar mensaje si no hay datos después de filtrar
        if df_filtrado.empty:
            st.warning("⚠️ NO HAY PARTIDAS QUE COINCIDAN CON LOS FILTROS SELECCIONADOS")
            st.caption("PRUEBA A CAMBIAR LOS FILTROS PARA VER MÁS RESULTADOS")
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
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Exportar datos - SOLO si hay datos filtrados
        if not df_filtrado.empty:
            st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
            st.subheader("💾 EXPORTAR DATOS")
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                csv = df_filtrado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 DESCARGAR CSV",
                    data=csv,
                    file_name="estadisticas_adivinanza_bmw.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="btn_descargar_csv"
                )
            
            with col_exp2:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_filtrado.to_excel(writer, index=False, sheet_name='Estadísticas')
                    writer.save()
                
                st.download_button(
                    label="📥 DESCARGAR EXCEL",
                    data=output.getvalue(),
                    file_name="estadisticas_adivinanza_bmw.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="btn_descargar_excel",
                    type="secondary"
                )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Limpiar estadísticas
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
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
    st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
    st.title("📖 INSTRUCCIONES DETALLADAS")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← VOLVER AL INICIO", key="btn_volver_inst", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # Pestañas
    tab1, tab2, tab3 = st.tabs(["🎮 CÓMO JUGAR", "🏆 SISTEMA DE PUNTUACIÓN", "💡 CONSEJOS"])
    
    with tab1:
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
        st.markdown("""
        ## 🎯 OBJETIVO DEL JUEGO
        ADIVINAR UN NÚMERO SECRETO ENTRE **1 Y 1000** EN LA MENOR CANTIDAD DE INTENTOS POSIBLE.
        
        <div class="separator"></div>
        
        ## 🎮 MODO SOLITARIO
        
        ### PASO A PASO:
        1. **INGRESA TU NOMBRE**
        2. **SELECCIONA LA DIFICULTAD:**
           - 🟢 **FÁCIL:** 20 INTENTOS
           - 🟡 **MEDIO:** 12 INTENTOS  
           - 🔴 **DIFÍCIL:** 5 INTENTOS
        
        3. **COMIENZA A JUGAR:**
           - INGRESA TU ADIVINANZA
           - EL SISTEMA TE DIRÁ SI EL NÚMERO SECRETO ES **MAYOR** O **MENOR**
           - ¡SIGUE INTENTANDO HASTA ADIVINARLO!
        
        4. **RESULTADO:**
           - ✅ **SI ADIVINAS:** ¡FELICIDADES! (PUEDES VOLVER A JUGAR)
           - ❌ **SI SE ACABAN LOS INTENTOS:** ¡INTÉNTALO DE NUEVO!
        
        <div class="separator"></div>
        
        ## 👥 MODO 2 JUGADORES
        
        ### PARA EL **JUGADOR 1** (PIENSA EL NÚMERO):
        1. INGRESA TU NOMBRE
        2. ELIGE UN NÚMERO SECRETO (1-1000)
        3. **¡NO LE DIGAS A NADIE EL NÚMERO!**
        4. CONFIGURA LA DIFICULTAD PARA EL JUGADOR 2
        
        ### PARA EL **JUGADOR 2** (ADIVINA):
        1. INGRESA TU NOMBRE
        2. COMIENZA A ADIVINAR
        3. RECIBIRÁS PISTAS: **MAYOR** O **MENOR**
        4. INTENTA ADIVINAR ANTES DE QUE SE ACABEN LOS INTENTOS
        5. **RESULTADO:** ✅ CORRECTO (GANAS) O ❌ INCORRECTO (PIERDES)
        
        <div class="separator"></div>
        
        ## 📊 ESTADÍSTICAS
        - TODAS TUS PARTIDAS SE GUARDAN AUTOMÁTICAMENTE EN UN ARCHIVO CSV
        - PUEDES FILTRAR POR JUGADOR, DIFICULTAD O RESULTADO
        - EXPORTA TUS DATOS A CSV O EXCEL
        - LOS DATOS SE CONSERVAN MIENTRAS USES LA MISMA SESIÓN
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
        st.markdown("""
        ## 🏆 SISTEMA DE PUNTUACIÓN
        
        ### 📐 FÓRMULA DE CÁLCULO:
        ```
        NOTA = 10 × (INTENTOS RESTANTES + 1) / INTENTOS TOTALES
        ```
        
        ### 📊 EJEMPLOS:
        
        #### DIFICULTAD **FÁCIL** (20 INTENTOS):
        - ✅ ADIVINAS EN **5 INTENTOS**:  
          `NOTA = 10 × (20-5+1)/20 = 10 × 16/20 = 8.0`
        
        - ✅ ADIVINAS EN **15 INTENTOS**:  
          `NOTA = 10 × (20-15+1)/20 = 10 × 6/20 = 3.0`
        
        #### DIFICULTAD **DIFÍCIL** (5 INTENTOS):
        - ✅ ADIVINAS EN **3 INTENTOS**:  
          `NOTA = 10 × (5-3+1)/5 = 10 × 3/5 = 6.0`
        
        ### 🎯 CÓMO OBTENER MEJOR PUNTUACIÓN:
        1. **ADIVINA MÁS RÁPIDO** (MENOS INTENTOS = MÁS PUNTOS)
        2. **JUEGA EN DIFICULTAD ALTA** (MÁS RIESGO = MÁS RECOMPENSA)
        3. **MEJORA TU ESTRATEGIA** DE ADIVINANZA
        
        ### 📈 ESCALA DE NOTAS:
        - **9.0 - 10.0:** 🏅 EXCELENTE  
        - **7.0 - 8.9:** 🥈 MUY BUENO  
        - **5.0 - 6.9:** 🥉 BUENO  
        - **3.0 - 4.9:** ✅ ACEPTABLE  
        - **0.0 - 2.9:** 📚 SIGUE PRACTICANDO
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
        st.markdown("""
        ## 💡 ESTRATEGIAS PARA GANAR
        
        ### 🔍 MÉTODO DE BÚSQUEDA BINARIA (RECOMENDADO):
        1. EMPIEZA CON **500** (EL PUNTO MEDIO)
        2. SI ES MAYOR, PRUEBA **750**
        3. SI ES MENOR, PRUEBA **250**
        4. SIGUE DIVIDIENDO EL RANGO POR LA MITAD
        
        ### 📊 ESTADÍSTICAS ÚTILES:
        - **67%** DE LOS NÚMEROS ESTÁN ENTRE **300-700**
        - SOLO **10%** ESTÁN EN LOS EXTREMOS (1-100, 900-1000)
        - EL NÚMERO **500** ES EL MÁS COMÚN DE ADIVINAR
        
        ### 🎮 CONSEJOS POR MODO:
        
        #### PARA **MODO SOLITARIO:**
        - **FÁCIL:** TÓMATE TU TIEMPO, EXPLORA DIFERENTES RANGOS
        - **MEDIO:** USA BÚSQUEDA BINARIA DESDE EL INICIO
        - **DIFÍCIL:** ARRIESGA MÁS, CONFÍA EN TU INTUICIÓN
        
        #### PARA **MODO 2 JUGADORES:**
        - **JUGADOR 1:** ELIGE NÚMEROS INUSUALES (EJ: 137, 842, 369)
        - **JUGADOR 2:** PREGUNTA POR RANGOS AMPLIOS PRIMERO
        
        ### 🎲 PATRONES COMUNES:
        1. MUCHOS JUGADORES ELIGEN NÚMEROS QUE TERMINAN EN **0, 5 O 7**
        2. LOS NÚMEROS DEL **1 AL 100** SON MÁS DIFÍCILES DE ADIVINAR
        3. LOS NÚMEROS CON **DÍGITOS REPETIDOS** (333, 777) SON POPULARES
        
        ### 🏅 RÉCORDS A BATIR:
        - **NOTA PERFECTA 10.0:** ADIVINAR EN EL PRIMER INTENTO
        - **RACHA GANADORA:** 5 PARTIDAS CONSECUTIVAS GANADAS
        - **RETO EXTREMO:** GANAR EN DIFICULTAD **DIFÍCIL** CON NOTA >8.0
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
    st.subheader("🎮 ¿LISTO PARA JUGAR?")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🏎️ COMENZAR MODO SOLITARIO", use_container_width=True, key="btn_inst_solo"):
            navegar_a("solitario")
            st.rerun()
    with col_btn2:
        if st.button("👥 COMENZAR CON AMIGOS", use_container_width=True, type="secondary", key="btn_inst_j2"):
            navegar_a("dos_jugadores")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =================== ACERCA DE ===================

def mostrar_acerca_de():
    """Muestra la página acerca de"""
    st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
    st.title("ℹ️ ACERCA DE ESTE PROYECTO")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← VOLVER AL INICIO", key="btn_volver_acerca", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    col_about1, col_about2 = st.columns([2, 1])
    
    with col_about1:
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
        st.markdown("""
        ## 🎮 JUEGO DE ADIVINANZA - BMW EDITION
        
        ### ✨ CARACTERÍSTICAS PRINCIPALES:
        - **DOS MODOS DE JUEGO:** SOLITARIO Y 2 JUGADORES
        - **TRES NIVELES DE DIFICULTAD:** FÁCIL, MEDIO, DIFÍCIL
        - **SISTEMA DE PUNTUACIÓN INTELIGENTE:** NOTAS DEL 0 AL 10
        - **ESTADÍSTICAS PERSISTENTES:** GUARDADO AUTOMÁTICO EN CSV
        - **INTERFAZ PREMIUM:** DISEÑO INSPIRADO EN BMW
        
        ### 🛠️ TECNOLOGÍAS UTILIZADAS:
        - **PYTHON 3** + **STREAMLIT** PARA LA INTERFAZ WEB
        - **PANDAS** PARA ANÁLISIS DE DATOS Y CSV
        - **OPENPYXL** PARA EXPORTACIÓN A EXCEL
        - **RANDOM** PARA GENERACIÓN DE NÚMEROS ALEATORIOS
        
        ### 🎯 PROPÓSITO EDUCATIVO:
        ESTE PROYECTO FUE DESARROLLADO COMO DEMOSTRACIÓN DE:
        - PROGRAMACIÓN EN PYTHON APLICADA A JUEGOS
        - INTERFAZ DE USUARIO WEB CON STREAMLIT
        - MANEJO DE DATOS Y ESTADÍSTICAS
        - LÓGICA DE PROGRAMACIÓN Y ALGORITMOS
        
        ### 📄 LICENCIA:
        **PROYECTO EDUCATIVO** - LIBRE PARA USO ACADÉMICO Y PERSONAL.
        
        ### 💻 CÓDIGO FUENTE:
        DISPONIBLE PARA FINES EDUCATIVOS Y DE APRENDIZAJE.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_about2:
        st.markdown('<div class="bmw-card">', unsafe_allow_html=True)
        st.info("🎓 **PROYECTO EDUCATIVO**")
        st.success("✅ **100% FUNCIONAL**")
        st.warning("📱 **DISEÑO RESPONSIVE**")
        st.error("⚡ **ALTO RENDIMIENTO**")
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.subheader("📊 DATOS DEL PROYECTO")
        
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{len(st.session_state.estadisticas)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">PARTIDAS GUARDADAS</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        st.subheader("🎮 PROBAR EL JUEGO")
        if st.button("🏎️ PROBAR MODO SOLITARIO", use_container_width=True, key="btn_probar_solo"):
            navegar_a("solitario")
            st.rerun()
        
        if st.button("👥 PROBAR CON AMIGOS", use_container_width=True, type="secondary", key="btn_probar_j2"):
            navegar_a("dos_jugadores")
            st.rerun()
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.caption(f"🕐 **ÚLTIMA ACTUALIZACIÓN:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown('<div class="bmw-card footer-bmw">', unsafe_allow_html=True)
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.caption("🎮 JUEGO DE ADIVINANZA BMW EDITION v4.0")
    with footer_col2:
        st.caption("📊 DISEÑO INSPIRADO EN BMW")
    with footer_col3:
        st.caption(f"🕐 {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.markdown('</div>', unsafe_allow_html=True)

# =================== EJECUCIÓN ===================

if __name__ == "__main__":
    main()