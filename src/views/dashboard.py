import streamlit as st
import pandas as pd

from src.controllers.GestorIncidencias import GestorIncidencias
from src.clases.Phishing import Phishing
from src.clases.malware import Malware
from src.clases.ataque_fuerza_bruta import AtaqueFuerzaBruta
from src.clases.fuga_datos import FugaDatos
from src.clases.acceso_no_autorizado import AccesoNoAutorizado
from src.clases.excepciones import ErrorIncidencia

<<<<<<< Updated upstream
=======

ARCHIVO_JSON = "incidencias.json"

COLORES_RIESGO = {
    "Bajo":    "#6ee7b7",
    "Medio":   "#fde68a",
    "Alto":    "#fdba74",
    "Critico": "#fca5a5",
}

ICONOS_TIPO = {
    "Phishing":               "🎣",
    "Malware":                "🦠",
    "Ataque de fuerza bruta": "🔨",
    "Fuga de datos":          "💧",
    "Acceso no autorizado":   "🚪",
}


def aplicar_estilos():
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .stApp {
        background-color: #0a0f1e;
        color: #e2e8f0;
    }

    section[data-testid="stSidebar"] { display: none !important; }
    .stAppDeployButton { display: none !important; }

    .hero {
        background: linear-gradient(135deg, #0d1526 0%, #111827 100%);
        border-bottom: 1px solid #1e2d4a;
        padding: 20px 10px;      /* Más espacio arriba y abajo del bloque */
        margin-bottom: 40px;
        text-align: center;
        min-height: auto;        /* Nos aseguramos de que no haya altura fija */
    }

    .hero-title {
        /* ¡Aquí está la clave! Añadimos !important para que Streamlit no lo ignore */
        font-size: 30px !important; 
        font-weight: 900 !important;
        
        background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        
        line-height: 1.4 !important;
        letter-spacing: 1px;
        display: block;
        margin: 0 auto;
        padding: 10px 0;
    }

    .hero-sub {
        color: #94a3b8;
        font-size: 24px; 
        font-weight: 400;
        margin-top: 10px;
        text-align: center;        /* Centramos también el subtítulo */
    }

    h2 {
        font-weight: 700 !important;
        color: #93c5fd !important;
        border-bottom: 1px solid #1e2d4a;
        padding-bottom: 0.4rem;
        margin-top: 0 !important;
    }
    h3 { font-weight: 600 !important; color: #a5b4fc !important; }

    .stTabs [data-baseweb="tab-list"] {
        background: #0d1526;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid #1e2d4a;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 0.88rem;
        color: #64748b !important;
        border-radius: 9px;
        padding: 0.5rem 1.2rem;
        border: none !important;
        background: transparent !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
        color: white !important;
    }
    .stTabs [data-baseweb="tab-border"] { display: none !important; }

    .stButton > button {
        border-radius: 10px;
        background: linear-gradient(135deg, #3b82f6, #6366f1);
        color: white !important;
        font-weight: 600;
        font-size: 0.88rem;
        border: none;
        padding: 0.55rem 1.2rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb, #4f46e5);
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(99,102,241,0.4);
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #111827 !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }
                
    .stSelectbox > div > div {
        background-color: #111827 !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }

    .stCheckbox label { color: #94a3b8 !important; }

    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #111827, #0d1f35);
        border: 1px solid #1e3a5f;
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    [data-testid="metric-container"] label {
        color: #64748b !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="stMetricValue"] {
        color: #60a5fa !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    .rec-card {
        background: linear-gradient(145deg, #111827, #0d1f35);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
        display: flex;
        align-items: flex-start;
        gap: 0.9rem;
    }
    .rec-icon  { font-size: 1.6rem; line-height: 1; margin-top: 2px; }
    .rec-tipo  { font-weight: 700; color: #93c5fd; font-size: 0.9rem; margin-bottom: 0.15rem; }
    .rec-texto { color: #94a3b8; font-size: 0.85rem; line-height: 1.5; }

    .badge {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        margin-left: 0.4rem;
        vertical-align: middle;
    }

    .stDataFrame { border-radius: 12px; overflow: hidden; border: 1px solid #1e3a5f; }

    .main .block-container {
        padding-top: 0 !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px;
    }
    </style>
    """, unsafe_allow_html=True)


def cargar_datos_json(gestor):
    try:
        from src.utils import persistence
        datos = persistence.cargar_json(ARCHIVO_JSON)
        for d in datos:
            try:
                tipo = d.get("tipo", "")
                if tipo == "Phishing":
                    obj = Phishing(d["canal"], d["enlace_sospechoso"], d["remitente_desconocido"])
                elif tipo == "Malware":
                    obj = Malware(d["persistencia"], d["propagacion"], d["sigilo"], d["payload"])
                elif tipo == "Ataque de fuerza bruta":
                    obj = AtaqueFuerzaBruta(d["intentos"], d["red"], d["acceso_admin"], d["utiliza_contrasenas"])
                elif tipo == "Fuga de datos":
                    obj = FugaDatos(d["datos_afectados"], d["numero_registros"], d["origen_fuga"])
                elif tipo == "Acceso no autorizado":
                    obj = AccesoNoAutorizado(d["usuario_afectado"], d["sistema_afectado"], d["privilegios_admin"])
                else:
                    continue
                gestor.lista_incidencias.append(obj)
            except Exception:
                continue  
    except Exception:
        pass  


>>>>>>> Stashed changes
def iniciar_dashboard():

    st.set_page_config(
        page_title="Sistema de Incidencias",
        layout="wide"
    )

    st.title("Sistema de Incidencias de Ciberseguridad")

    st.write(
        "Aplicación para registrar, clasificar, analizar y visualizar "
        "incidencias de ciberseguridad."
    )

    if "gestor" not in st.session_state:
        st.session_state.gestor = GestorIncidencias("Gestor principal")

    gestor = st.session_state.gestor

    st.sidebar.header("Registrar incidencia")

    tipo = st.sidebar.selectbox(
        "Tipo de incidencia",
        [
            "Phishing",
            "Malware",
            "Ataque de fuerza bruta",
            "Fuga de datos",
            "Acceso no autorizado"
        ]
    )

    try:

        if tipo == "Phishing":

            canal = st.sidebar.text_input("Canal", "Correo electrónico")
            enlace_sospechoso = st.sidebar.checkbox("Enlace sospechoso")
            remitente_desconocido = st.sidebar.checkbox("Remitente desconocido")

            if st.sidebar.button("Registrar phishing"):

                incidencia = Phishing(
                    canal,
                    enlace_sospechoso,
                    remitente_desconocido
                )

                gestor.agregar_incidencia(incidencia)
                st.sidebar.success("Incidencia registrada correctamente")

        elif tipo == "Malware":

            persistencia = st.sidebar.checkbox("Persistencia")
            propagacion = st.sidebar.checkbox("Propagación")
            sigilo = st.sidebar.checkbox("Sigilo")
            payload = st.sidebar.text_input("Payload", "Robo de credenciales")

            if st.sidebar.button("Registrar malware"):

                incidencia = Malware(
                    persistencia,
                    propagacion,
                    sigilo,
                    payload
                )

                gestor.agregar_incidencia(incidencia)
                st.sidebar.success("Incidencia registrada correctamente")

        elif tipo == "Ataque de fuerza bruta":

            intentos = st.sidebar.number_input(
                "Número de intentos",
                min_value=0,
                step=1
            )

            red = st.sidebar.number_input(
                "Red",
                min_value=0,
                step=1
            )

            acceso_admin = st.sidebar.checkbox("Acceso admin")
            utiliza_contrasenas = st.sidebar.checkbox("Utiliza contraseñas")

            if st.sidebar.button("Registrar ataque"):

                incidencia = AtaqueFuerzaBruta(
                    intentos,
                    red,
                    acceso_admin,
                    utiliza_contrasenas
                )

                gestor.agregar_incidencia(incidencia)
                st.sidebar.success("Incidencia registrada correctamente")

        elif tipo == "Fuga de datos":

            datos_afectados = st.sidebar.text_input(
                "Datos afectados",
                "Correos y contraseñas"
            )

            numero_registros = st.sidebar.number_input(
                "Número de registros",
                min_value=1,
                step=1
            )

            origen_fuga = st.sidebar.text_input(
                "Origen de la fuga",
                "Servidor externo"
            )

            if st.sidebar.button("Registrar fuga"):

                incidencia = FugaDatos(
                    datos_afectados,
                    numero_registros,
                    origen_fuga
                )

                gestor.agregar_incidencia(incidencia)
                st.sidebar.success("Incidencia registrada correctamente")

        elif tipo == "Acceso no autorizado":

            usuario_afectado = st.sidebar.text_input(
                "Usuario afectado",
                "admin01"
            )

            sistema_afectado = st.sidebar.text_input(
                "Sistema afectado",
                "Panel interno"
            )

            privilegios_admin = st.sidebar.checkbox("Privilegios admin")

            if st.sidebar.button("Registrar acceso"):

                incidencia = AccesoNoAutorizado(
                    usuario_afectado,
                    sistema_afectado,
                    privilegios_admin
                )

                gestor.agregar_incidencia(incidencia)
                st.sidebar.success("Incidencia registrada correctamente")

    except ErrorIncidencia as error:
        st.sidebar.error(error)

    except Exception as error:
        st.sidebar.error(error)

    st.header("Incidencias registradas")

    df = gestor.convertir_a_dataframe()

    if len(df) == 0:

        st.info("Todavía no hay incidencias registradas")

    else:

        col1, col2 = st.columns(2)

        with col1:
            filtro_tipo = st.selectbox(
                "Filtrar por tipo",
                ["Todos"] + list(df["tipo"].unique())
            )

        with col2:
            filtro_riesgo = st.selectbox(
                "Filtrar por nivel de riesgo",
                ["Todos"] + list(df["nivel_riesgo"].unique())
            )

        df_filtrado = df

        if filtro_tipo != "Todos":
            df_filtrado = df_filtrado[df_filtrado["tipo"] == filtro_tipo]

        if filtro_riesgo != "Todos":
            df_filtrado = df_filtrado[df_filtrado["nivel_riesgo"] == filtro_riesgo]

        st.dataframe(df_filtrado)

        st.header("Recomendaciones")

        for incidencia in gestor.lista_incidencias:
            st.write(
                incidencia.tipo,
                "-",
                incidencia.obtener_recomendacion()
            )

        st.header("Estadísticas visuales")

        st.subheader("Incidencias por tipo")
        st.bar_chart(df["tipo"].value_counts())

        st.subheader("Incidencias por nivel de riesgo")
        st.bar_chart(df["nivel_riesgo"].value_counts())

        st.header("Guardar y cargar datos")

        col3, col4 = st.columns(2)

        with col3:
            if st.button("Guardar JSON"):
                gestor.guardar_en_json("incidencias.json")
                st.success("Datos guardados en incidencias.json")

        with col4:
            if st.button("Guardar CSV"):
                gestor.guardar_en_csv("incidencias.csv")
                st.success("Datos guardados en incidencias.csv")