import streamlit as st
import random
import datetime
import pandas as pd
import io
import os
from io import BytesIO

# =================== CONFIGURACIÓN INICIAL ===================
st.set_page_config(
    page_title="Juego de Adivinanza",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== CSS APPLE STYLE ===================
apple_css = """
<style>
    /* Variables de diseño Apple */
    :root {
        --apple-white: #f5f5f7;
        --apple-light-gray: #f2f2f7;
        --apple-gray: #8e8e93;
        --apple-dark-gray: #1d1d1f;
        --apple-black: #000000;
        --apple-blue: #0071e3;
        --apple-blue-hover: #0077ed;
        --apple-blue-active: #0062b9;
        --apple-green: #34c759;
        --apple-red: #ff3b30;
        --apple-orange: #ff9500;
        --apple-border: #d2d2d7;
        --apple-shadow: rgba(0, 0, 0, 0.06);
        --apple-shadow-hover: rgba(0, 0, 0, 0.08);
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
    
    /* Estructura principal */
    .main {
        background-color: var(--apple-white);
        color: var(--apple-dark-gray);
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', sans-serif;
    }
    
    /* Títulos y encabezados Apple */
    h1, h2, h3, h4 {
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif;
        font-weight: 600;
        letter-spacing: -0.5px;
        color: var(--apple-dark-gray);
        margin-top: 0;
    }
    
    h1 {
        font-size: 48px;
        font-weight: 700;
        background: linear-gradient(90deg, var(--apple-dark-gray), var(--apple-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 32px;
        text-align: center;
    }
    
    h2 {
        font-size: 32px;
        margin-bottom: 24px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--apple-border);
    }
    
    h3 {
        font-size: 24px;
        color: var(--apple-gray);
    }
    
    /* Sidebar estilo Apple */
    .css-1d391kg, .css-12oz5g7 {
        background-color: var(--apple-light-gray) !important;
        border-right: 1px solid var(--apple-border);
    }
    
    /* Contenedores y tarjetas Apple */
    .apple-card {
        background: white;
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px var(--apple-shadow);
        border: 1px solid var(--apple-border);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .apple-card:hover {
        box-shadow: 0 8px 30px var(--apple-shadow-hover);
        transform: translateY(-4px);
    }
    
    /* Botones estilo Apple */
    .stButton > button {
        background-color: var(--apple-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 980px !important;
        padding: 12px 28px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2) !important;
        letter-spacing: -0.2px;
    }
    
    .stButton > button:hover {
        background-color: var(--apple-blue-hover) !important;
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(0, 113, 227, 0.3) !important;
    }
    
    .stButton > button:active {
        background-color: var(--apple-blue-active) !important;
        transform: scale(0.98);
    }
    
    /* Botones secundarios */
    .secondary-button {
        background-color: transparent !important;
        color: var(--apple-blue) !important;
        border: 2px solid var(--apple-blue) !important;
        box-shadow: none !important;
    }
    
    .secondary-button:hover {
        background-color: rgba(0, 113, 227, 0.08) !important;
    }
    
    /* Mensajes Apple */
    .mensaje-correcto {
        background: linear-gradient(135deg, rgba(52, 199, 89, 0.1), rgba(52, 199, 89, 0.05));
        border: 2px solid rgba(52, 199, 89, 0.3);
        border-radius: 16px;
        padding: 28px;
        margin: 20px 0;
        color: var(--apple-dark-gray);
        animation: fadeIn 0.5s ease;
    }
    
    .mensaje-incorrecto {
        background: linear-gradient(135deg, rgba(255, 59, 48, 0.1), rgba(255, 59, 48, 0.05));
        border: 2px solid rgba(255, 59, 48, 0.3);
        border-radius: 16px;
        padding: 28px;
        margin: 20px 0;
        color: var(--apple-dark-gray);
        animation: fadeIn 0.5s ease;
    }
    
    /* Métricas Apple */
    .metric-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 24px;
        background: linear-gradient(135deg, #f8f9ff 0%, #f2f4ff 100%);
        border-radius: 20px;
        border: 2px solid rgba(0, 113, 227, 0.1);
        min-height: 140px;
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0, 113, 227, 0.1);
    }
    
    .metric-value {
        font-size: 56px;
        font-weight: 700;
        background: linear-gradient(90deg, var(--apple-blue), #5856d6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        margin-bottom: 8px;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    }
    
    .metric-label {
        font-size: 14px;
        color: var(--apple-gray);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    /* Tablas estilo Apple */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
    }
    
    .dataframe th {
        background-color: var(--apple-light-gray);
        color: var(--apple-dark-gray);
        font-weight: 600;
        padding: 18px 24px;
        text-align: left;
        border-bottom: 2px solid var(--apple-border);
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .dataframe td {
        padding: 18px 24px;
        border-bottom: 1px solid var(--apple-border);
        color: var(--apple-dark-gray);
        font-size: 15px;
        font-weight: 400;
    }
    
    .dataframe tr:hover {
        background-color: rgba(0, 113, 227, 0.04);
    }
    
    /* Inputs y selectores Apple */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border-radius: 12px !important;
        border: 2px solid var(--apple-border) !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: var(--apple-blue) !important;
        box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.1) !important;
    }
    
    /* Badges Apple */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 0 4px;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
    }
    
    .badge-success {
        background-color: rgba(52, 199, 89, 0.1);
        color: var(--apple-green);
        border: 2px solid rgba(52, 199, 89, 0.3);
    }
    
    .badge-error {
        background-color: rgba(255, 59, 48, 0.1);
        color: var(--apple-red);
        border: 2px solid rgba(255, 59, 48, 0.3);
    }
    
    .badge-warning {
        background-color: rgba(255, 149, 0, 0.1);
        color: var(--apple-orange);
        border: 2px solid rgba(255, 149, 0, 0.3);
    }
    
    .badge-info {
        background-color: rgba(0, 113, 227, 0.1);
        color: var(--apple-blue);
        border: 2px solid rgba(0, 113, 227, 0.3);
    }
    
    /* Alertas Apple */
    .stAlert {
        border-radius: 16px;
        border-left: none;
        padding: 20px 24px;
        background-color: white;
        border: 2px solid var(--apple-border);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
    }
    
    /* Progress bar Apple */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--apple-blue), #5856d6);
        border-radius: 10px;
    }
    
    /* Separadores */
    .separator {
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--apple-border), transparent);
        margin: 40px 0;
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
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }
    
    /* Contenedor de juego */
    .contenedor-juego {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        border-radius: 20px;
        padding: 32px;
        margin: 24px 0;
        border: 2px solid var(--apple-border);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
        animation: fadeInUp 0.5s ease;
    }
    
    /* Efectos especiales */
    .numero-secreto {
        font-size: 64px;
        font-weight: 800;
        background: linear-gradient(90deg, #FF375F, #FF9500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 20px 0;
        animation: pulse 2s infinite;
    }
    
    .emoji-grande {
        font-size: 48px;
        text-align: center;
        margin: 20px 0;
    }
    
    /* Grid responsive */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 24px;
        margin: 24px 0;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        h1 {
            font-size: 36px;
        }
        
        h2 {
            font-size: 28px;
        }
        
        .metric-value {
            font-size: 42px;
        }
        
        .apple-card {
            padding: 24px;
        }
        
        .numero-secreto {
            font-size: 48px;
        }
    }
</style>
"""

# Aplicar el CSS
st.markdown(apple_css, unsafe_allow_html=True)

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
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.markdown('<div class="emoji-grande">🔢</div>', unsafe_allow_html=True)
    st.title("Juego de Adivinanza")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🎯 ¿Cómo funciona?
        
        **¡Adivina el número secreto entre 1 y 1000!**
        
        ### 🎮 Modos de juego:
        
        **🔹 Modo Solitario**  
        • Juega contra la computadora  
        • Elige entre 3 niveles de dificultad  
        • Intenta adivinar en pocos intentos
        
        **🔹 Modo 2 Jugadores**  
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
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{mejor_partida["Nota"]:.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Mejor Nota</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption(f"**Por:** {mejor_partida['Jugador1']} | **Modo:** {mejor_partida['Modo']}")
        else:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">0.00</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Mejor Nota</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption("¡Sé el primero en establecer un récord!")
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
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
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        # Otros accesos rápidos
        st.markdown("### 📍 Accesos rápidos")
        col_acc1, col_acc2 = st.columns(2)
        with col_acc1:
            if st.button("📊 Estadísticas", key="btn_estad_inicio", use_container_width=True):
                navegar_a("estadisticas")
                st.rerun()
        with col_acc2:
            if st.button("📖 Instrucciones", key="btn_inst_inicio", use_container_width=True):
                navegar_a("instrucciones")
                st.rerun()

# =================== MODO SOLITARIO ===================

def mostrar_solitario():
    """Muestra la página del modo solitario"""
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.title("🎮 MODO SOLITARIO")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← Volver al inicio", key="btn_volver_solo", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # Mostrar resultado si existe
    if st.session_state.resultado_solo is not None:
        if st.session_state.resultado_solo == "ganado":
            st.markdown(f"""
            <div class="mensaje-correcto">
            <h3>🎉 ¡FELICIDADES {st.session_state.jugador_solo.upper()}!</h3>
            <p><strong>✅ Has ganado en {st.session_state.intentos_solo} intentos</strong></p>
            <div class="numero-secreto">{st.session_state.numero_secreto_solo}</div>
            <p><span class="badge badge-success">Victoria</span> • Dificultad: {st.session_state.dificultad_solo}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="mensaje-incorrecto">
            <h3>😞 ¡SE ACABARON LOS INTENTOS!</h3>
            <p><strong>❌ No lograste adivinar el número</strong></p>
            <div class="numero-secreto">{st.session_state.numero_secreto_solo}</div>
            <p><span class="badge badge-error">Derrota</span> • Dificultad: {st.session_state.dificultad_solo}</p>
            <p>Intentos usados: {st.session_state.intentos_solo}/{st.session_state.max_intentos_solo}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="grid-container">', unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Jugar otra partida", type="primary", use_container_width=True, key="btn_reiniciar_solo"):
                reiniciar_solitario()
                st.rerun()
        with col_btn2:
            if st.button("📊 Ver estadísticas", use_container_width=True, type="secondary", key="btn_estad_solo"):
                navegar_a("estadisticas")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # Configuración de nueva partida
    if not st.session_state.partida_activa_solo:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
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
            st.markdown('<div class="apple-card">', unsafe_allow_html=True)
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
                if st.button("❌ Cancelar partida", use_container_width=True, type="secondary", key="btn_cancelar_solo"):
                    st.session_state.partida_activa_solo = False
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_juego2:
            st.markdown('<div class="apple-card">', unsafe_allow_html=True)
            st.subheader("📊 Estado de la partida")
            
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{st.session_state.intentos_solo}/{st.session_state.max_intentos_solo}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Intentos Usados</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
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
            st.markdown('</div>', unsafe_allow_html=True)

# =================== MODO 2 JUGADORES ===================

def mostrar_dos_jugadores():
    """Muestra la página del modo 2 jugadores"""
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.title("👥 MODO 2 JUGADORES")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← Volver al inicio", key="btn_volver_j2", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # Mostrar resultado si existe
    if st.session_state.resultado_j2 is not None:
        if st.session_state.resultado_j2 == "ganado":
            st.markdown(f"""
            <div class="mensaje-correcto">
            <h3>🎉 ¡{st.session_state.jugador2_nombre.upper()} HA GANADO!</h3>
            <p><strong>✅ Adivinó en {st.session_state.intentos_j2} intentos</strong></p>
            <div class="numero-secreto">{st.session_state.numero_secreto_j2}</div>
            <p><span class="badge badge-success">Victoria</span> • Dificultad: {st.session_state.dificultad_j2}</p>
            <p>Jugador 1: {st.session_state.jugador1_nombre}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="mensaje-incorrecto">
            <h3>😞 ¡SE ACABARON LOS INTENTOS!</h3>
            <p><strong>❌ No lograste adivinar el número</strong></p>
            <div class="numero-secreto">{st.session_state.numero_secreto_j2}</div>
            <p><span class="badge badge-error">Derrota</span> • Dificultad: {st.session_state.dificultad_j2}</p>
            <p>Jugador 1: {st.session_state.jugador1_nombre}</p>
            <p>Intentos usados: {st.session_state.intentos_j2}/{st.session_state.max_intentos_j2}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="grid-container">', unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Jugar otra partida", type="primary", use_container_width=True, key="btn_reiniciar_j2"):
                reiniciar_dos_jugadores()
                st.rerun()
        with col_btn2:
            if st.button("📊 Ver estadísticas", use_container_width=True, type="secondary", key="btn_estad_j2"):
                navegar_a("estadisticas")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # FASE 1: Jugador 1 elige el número
    if st.session_state.fase_j2 == 1:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
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
            
            st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)
    
    # FASE 2: Jugador 2 adivina
    elif st.session_state.fase_j2 == 2:
        if st.session_state.numero_secreto_j2 is None:
            st.error("Error: No se configuró el número secreto. Vuelve a la fase 1.")
            if st.button("↩️ Volver a fase 1", key="btn_volver_fase1", type="secondary"):
                st.session_state.fase_j2 = 1
                st.rerun()
        else:
            st.markdown('<div class="contenedor-juego">', unsafe_allow_html=True)
            st.subheader("👤 FASE 2: Jugador 2 (Adivina el número)")
            st.markdown('</div>', unsafe_allow_html=True)
            
            col_j2_1, col_j2_2 = st.columns(2)
            
            with col_j2_1:
                st.markdown('<div class="apple-card">', unsafe_allow_html=True)
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
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_j2_2:
                st.markdown('<div class="apple-card">', unsafe_allow_html=True)
                jugador_actual = st.session_state.jugador2_nombre or jugador2 or "Jugador 2"
                st.subheader(f"📊 Estado - {jugador_actual}")
                
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{st.session_state.intentos_j2}/{st.session_state.max_intentos_j2}</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Intentos Usados</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                progreso_j2 = st.session_state.intentos_j2 / st.session_state.max_intentos_j2
                st.progress(min(progreso_j2, 1.0))
                
                st.info(f"🎮 **Contra:** {st.session_state.jugador1_nombre}")
                st.info(f"📈 **Dificultad:** {st.session_state.dificultad_j2}")
                
                if st.session_state.intentos_j2 > 0:
                    with st.expander("💡 Estrategia recomendada", expanded=True):
                        if adivinanza_j2 < st.session_state.numero_secreto_j2:
                            st.success(f"Prueba entre **{adivinanza_j2 + 1}** y **1000**")
                        elif adivinanza_j2 > st.session_state.numero_secreto_j2:
                            st.success(f"Prueba entre **1** y **{adivinanza_j2 - 1}**")
                        else:
                            st.info("¡Empieza por el medio (500)!")
                
                if st.button("❌ Cancelar partida", use_container_width=True, type="secondary", key="btn_cancelar_j2"):
                    st.session_state.fase_j2 = 1
                    st.session_state.resultado_j2 = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# =================== ESTADÍSTICAS ===================

def mostrar_estadisticas():
    """Muestra la página de estadísticas"""
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.title("📊 ESTADÍSTICAS")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← Volver al inicio", key="btn_volver_estad", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    if not st.session_state.estadisticas:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        df = pd.DataFrame(st.session_state.estadisticas)
        
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.info(f"📁 **Archivo de datos:** {ARCHIVO_ESTADISTICAS} ({len(df)} partidas guardadas)")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filtros
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.subheader("🔍 Filtros")
        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        
        with col_filtro1:
            modos = sorted(list(df["Modo"].unique()))
            filtrar_modo = st.multiselect(
                "Modo de juego:",
                options=modos,
                default=modos,
                key="filtro_modo"
            )
        
        with col_filtro2:
            dificultades = sorted(list(df["Dificultad"].unique()))
            filtrar_dificultad = st.multiselect(
                "Dificultad:",
                options=dificultades,
                default=dificultades,
                key="filtro_dificultad"
            )
        
        with col_filtro3:
            resultados = sorted(list(df["Resultado"].unique()))
            filtrar_resultado = st.multiselect(
                "Resultado:",
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
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.subheader("📈 Resumen general")
        
        col_met1, col_met2, col_met3, col_met4, col_met5 = st.columns(5)
        
        with col_met1:
            total = len(df_filtrado)
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{total}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Total partidas</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_met2:
            ganadas = len(df_filtrado[df_filtrado["Resultado"] == "Ganado"])
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{ganadas}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Partidas ganadas</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_met3:
            perdidas = len(df_filtrado[df_filtrado["Resultado"] == "Perdido"])
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{perdidas}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Partidas perdidas</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_met4:
            if total > 0:
                tasa_exito = (ganadas / total) * 100
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{tasa_exito:.1f}%</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Tasa de éxito</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">0%</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Tasa de éxito</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col_met5:
            if not df_filtrado.empty:
                mejor_nota = df_filtrado["Nota"].max()
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{mejor_nota:.2f}</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Mejor nota</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">0.00</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Mejor nota</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tabla de datos
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Exportar datos - SOLO si hay datos filtrados
        if not df_filtrado.empty:
            st.markdown('<div class="apple-card">', unsafe_allow_html=True)
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
                    key="btn_descargar_csv",
                    type="primary"
                )
            
            with col_exp2:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_filtrado.to_excel(writer, index=False, sheet_name='Estadísticas')
                    writer.save()
                
                st.download_button(
                    label="📥 Descargar Excel",
                    data=output.getvalue(),
                    file_name="estadisticas_adivinanza.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="btn_descargar_excel",
                    type="secondary"
                )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Limpiar estadísticas
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        if st.button("🗑️ Limpiar todas las estadísticas", type="secondary", use_container_width=True, key="btn_limpiar_estad"):
            st.session_state.estadisticas = []
            try:
                if os.path.exists(ARCHIVO_ESTADISTICAS):
                    os.remove(ARCHIVO_ESTADISTICAS)
            except:
                pass
            st.success("✅ Estadísticas limpiadas correctamente")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# =================== INSTRUCCIONES ===================

def mostrar_instrucciones():
    """Muestra la página de instrucciones"""
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.title("📖 INSTRUCCIONES DETALLADAS")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← Volver al inicio", key="btn_volver_inst", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    # Pestañas
    tab1, tab2, tab3 = st.tabs(["🎮 Cómo jugar", "🏆 Sistema de puntuación", "💡 Consejos"])
    
    with tab1:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.markdown("""
        ## 🎯 OBJETIVO DEL JUEGO
        Adivinar un número secreto entre **1 y 1000** en la menor cantidad de intentos posible.
        
        <div class="separator"></div>
        
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
        
        <div class="separator"></div>
        
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
        
        <div class="separator"></div>
        
        ## 📊 ESTADÍSTICAS
        - Todas tus partidas se guardan automáticamente en un archivo CSV
        - Puedes filtrar por jugador, dificultad o resultado
        - Exporta tus datos a CSV o Excel
        - Los datos se conservan mientras uses la misma sesión
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

# =================== ACERCA DE ===================

def mostrar_acerca_de():
    """Muestra la página acerca de"""
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.title("ℹ️ ACERCA DE ESTE PROYECTO")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón para volver al inicio
    col_volver, _ = st.columns([1, 3])
    with col_volver:
        if st.button("← Volver al inicio", key="btn_volver_acerca", type="secondary"):
            navegar_a("inicio")
            st.rerun()
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    
    col_about1, col_about2 = st.columns([2, 1])
    
    with col_about1:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.markdown("""
        ## 🎮 Juego de Adivinanza - Proyecto Educativo
        
        ### ✨ Características principales:
        - **Dos modos de juego:** Solitario y 2 jugadores
        - **Tres niveles de dificultad:** Fácil, Medio, Difícil
        - **Sistema de puntuación inteligente:** Notas del 0 al 10
        - **Estadísticas persistentes:** Guardado automático en CSV
        - **Interfaz moderna:** Diseño inspirado en Apple
        
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
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_about2:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.info("🎓 **Proyecto Educativo**")
        st.success("✅ **100% Funcional**")
        st.warning("📱 **Responsive Design**")
        st.error("⚡ **Alto Rendimiento**")
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.subheader("📊 Datos del proyecto")
        
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{len(st.session_state.estadisticas)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Partidas guardadas</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        
        st.subheader("🎮 Probar el juego")
        if st.button("🎮 Probar modo solitario", type="primary", use_container_width=True, key="btn_probar_solo"):
            navegar_a("solitario")
            st.rerun()
        
        if st.button("👥 Probar con amigos", type="secondary", use_container_width=True, key="btn_probar_j2"):
            navegar_a("dos_jugadores")
            st.rerun()
        
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
        st.caption(f"🕐 **Última actualización:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
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
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.caption("🎮 Juego de Adivinanza v4.0")
    with footer_col2:
        st.caption("📊 Diseño inspirado en Apple")
    with footer_col3:
        st.caption(f"🕐 {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.markdown('</div>', unsafe_allow_html=True)

# =================== EJECUCIÓN ===================

if __name__ == "__main__":
    main()