import streamlit as st
import pandas as pd
import plotly.express as px

from src.controllers.GestorIncidencias import GestorIncidencias
from src.clases.Phishing import Phishing
from src.clases.malware import Malware
from src.clases.ataque_fuerza_bruta import AtaqueFuerzaBruta
from src.clases.fuga_datos import FugaDatos
from src.clases.acceso_no_autorizado import AccesoNoAutorizado
from src.clases.excepciones import ErrorIncidencia

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


def iniciar_dashboard():

    st.set_page_config(
        page_title="Sistema de Incidencias de Ciberseguridad",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    aplicar_estilos()

    if "gestor" not in st.session_state:
        st.session_state.gestor = GestorIncidencias("Gestor principal")
        cargar_datos_json(st.session_state.gestor)

    gestor = st.session_state.gestor

    st.markdown("""
    <div class="hero">
        <p class="hero-title">Sistema de Incidencias de Ciberseguridad</p>
        <p class="hero-sub">Registra, clasifica y analiza incidencias en tiempo real</p>
    </div>
    """, unsafe_allow_html=True)

    df    = gestor.convertir_a_dataframe()
    total = len(df)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("Total",    total)
    with c2: st.metric("Criticas", int(len(df[df["nivel_riesgo"] == "Critico"])) if total > 0 else 0)
    with c3: st.metric("Altas",    int(len(df[df["nivel_riesgo"] == "Alto"]))    if total > 0 else 0)
    with c4: st.metric("Medias",   int(len(df[df["nivel_riesgo"] == "Medio"]))   if total > 0 else 0)
    with c5: st.metric("Bajas",    int(len(df[df["nivel_riesgo"] == "Bajo"]))    if total > 0 else 0)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Nueva incidencia",
        "Incidencias",
        "Estadisticas",
        "Recomendaciones",
    ])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("## Registrar nueva incidencia")
        st.markdown("<p style='color:#475569'>Selecciona el tipo e introduce los datos del incidente.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Selector del tipo de incidencia
        tipo = st.selectbox(
            "Tipo de incidencia",
            ["Phishing", "Malware", "Ataque de fuerza bruta", "Fuga de datos", "Acceso no autorizado"],
            key="tipo_select"
        )

        incidencia = None  

        try:
            if tipo == "Phishing":
                col1, _ = st.columns(2)
                with col1:
                    canal = st.text_input("Canal", "Correo electronico")
                enlace    = st.checkbox("Contiene enlace sospechoso")
                remitente = st.checkbox("Remitente desconocido")
                if st.button("Registrar Phishing", use_container_width=True):
                    incidencia = Phishing(canal, enlace, remitente)

            elif tipo == "Malware":
                payload = st.text_input("Payload detectado", "Robo de credenciales")
                c1, c2, c3 = st.columns(3)
                with c1: persistencia_v = st.checkbox("Persistencia")
                with c2: propagacion_v  = st.checkbox("Propagacion")
                with c3: sigilo_v       = st.checkbox("Sigilo")
                if st.button("Registrar Malware", use_container_width=True):
                    incidencia = Malware(persistencia_v, propagacion_v, sigilo_v, payload)

            elif tipo == "Ataque de fuerza bruta":
                col1, col2 = st.columns(2)
                with col1: intentos = st.number_input("Numero de intentos", min_value=0, step=1)
                with col2: red      = st.number_input("Red (ID)",            min_value=0, step=1)
                c1, c2 = st.columns(2)
                with c1: acceso_admin = st.checkbox("Acceso admin")
                with c2: usa_contra   = st.checkbox("Utiliza contrasenas comunes")
                if st.button("Registrar Ataque de fuerza bruta", use_container_width=True):
                    incidencia = AtaqueFuerzaBruta(intentos, red, acceso_admin, usa_contra)

            elif tipo == "Fuga de datos":
                col1, col2 = st.columns(2)
                with col1:
                    datos_afectados = st.text_input("Datos afectados", "Correos y contrasenas")
                    origen          = st.text_input("Origen de la fuga", "Servidor externo")
                with col2:
                    num_registros = st.number_input("Numero de registros", min_value=1, step=1)
                if st.button("Registrar Fuga de datos", use_container_width=True):
                    incidencia = FugaDatos(datos_afectados, num_registros, origen)

            elif tipo == "Acceso no autorizado":
                col1, col2 = st.columns(2)
                with col1: usuario = st.text_input("Usuario afectado", "admin01")
                with col2: sistema = st.text_input("Sistema afectado", "Panel interno")
                priv_admin = st.checkbox("Tiene privilegios de administrador")
                if st.button("Registrar Acceso no autorizado", use_container_width=True):
                    incidencia = AccesoNoAutorizado(usuario, sistema, priv_admin)

            if incidencia:
                gestor.agregar_incidencia(incidencia)
                gestor.guardar_en_json(ARCHIVO_JSON)
                nivel = incidencia.nivel_riesgo
                color = COLORES_RIESGO.get(nivel, "#94a3b8")
                st.markdown(f"""
                <div style="background:#0d2b1f; border:1px solid #22c55e; border-left:4px solid #22c55e;
                    border-radius:10px; padding:1rem 1.2rem; margin-top:1rem;">
                    <div style="color:#22c55e; font-weight:700; font-size:1rem; margin-bottom:0.3rem;">
                        Incidencia registrada correctamente
                    </div>
                    <div style="color:#94a3b8; font-size:0.88rem;">
                        Tipo: <strong style="color:#e2e8f0">{tipo}</strong>
                        &nbsp;&nbsp;|&nbsp;&nbsp;
                        Nivel de riesgo:
                        <span style="background:{color}33; color:{color}; border:1px solid {color}66;
                              border-radius:20px; padding:0.1rem 0.55rem; font-size:0.78rem; font-weight:600;">
                            {nivel}
                        </span>
                    </div>
                    <div style="color:#64748b; font-size:0.82rem; margin-top:0.35rem;">
                        {incidencia.obtener_recomendacion()}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.rerun()

        except ErrorIncidencia as e:
            st.error(f"Error de validacion: {e}")
        except Exception as e:
            st.error(f"Error inesperado: {e}")

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("## Incidencias registradas")

        if total == 0:
            st.info("No hay incidencias registradas todavia.")
        else:
            # Filtros de tipo y nivel de riesgo
            col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
            with col_f1:
                filtro_tipo   = st.selectbox("Filtrar por tipo",   ["Todos"] + list(df["tipo"].unique()))
            with col_f2:
                filtro_riesgo = st.selectbox("Filtrar por riesgo", ["Todos", "Critico", "Alto", "Medio", "Bajo"])
            with col_f3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Borrar todo"):
                    st.session_state.gestor = GestorIncidencias("Gestor principal")
                    from src.utils import persistence
                    persistence.guardar_json([], ARCHIVO_JSON)
                    st.rerun()

            df_filtrado = df.copy()
            if filtro_tipo   != "Todos":
                df_filtrado = df_filtrado[df_filtrado["tipo"]         == filtro_tipo]
            if filtro_riesgo != "Todos":
                df_filtrado = df_filtrado[df_filtrado["nivel_riesgo"] == filtro_riesgo]

            st.markdown(
                f"<p style='color:#475569; font-size:0.85rem'>{len(df_filtrado)} incidencia(s) encontrada(s)</p>",
                unsafe_allow_html=True
            )

            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "tipo":          st.column_config.TextColumn("Tipo",            width="medium"),
                    "nivel_riesgo":  st.column_config.TextColumn("Nivel de riesgo", width="small"),
                    "recomendacion": st.column_config.TextColumn("Recomendacion",   width="large"),
                }
            )

            st.markdown("<br>", unsafe_allow_html=True)

            col_e1, col_e2 = st.columns(2)
            with col_e1:
                if st.button("Guardar JSON", use_container_width=True):
                    gestor.guardar_en_json(ARCHIVO_JSON)
                    st.success("Guardado en incidencias.json")
            with col_e2:
                if st.button("Exportar CSV", use_container_width=True):
                    gestor.guardar_en_csv("incidencias.csv")
                    st.success("Guardado en incidencias.csv")

    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("## Estadisticas visuales")

        if total == 0:
            st.info("Añade incidencias para ver las estadisticas.")
        else:
            col_g1, col_g2 = st.columns(2)

            # Grafica de barras por tipo de incidencia
            with col_g1:
                st.markdown("### Por tipo")
                conteo_tipo = df["tipo"].value_counts().reset_index()
                conteo_tipo.columns = ["Tipo", "Cantidad"]
                fig1 = px.bar(
                    conteo_tipo,
                    x="Tipo",
                    y="Cantidad",
                    template="plotly_dark",
                )
                fig1.update_traces(
                    marker_color="#93c5fd", 
                    marker_line_width=0
                )
                fig1.update_layout(
                    paper_bgcolor="#111827",
                    plot_bgcolor="#0d1526",
                    font=dict(
                        family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                        color="#cbd5e1"
                    ),
                    xaxis=dict(tickangle=0, title=None, gridcolor="#1e2d4a"),
                    yaxis=dict(title="Cantidad", dtick=1, tickformat="d", gridcolor="#1e2d4a"),
                    margin=dict(t=20, b=10, l=10, r=10),
                    showlegend=False,
                )
                st.plotly_chart(fig1, use_container_width=True)

            # Grafica de barras por nivel de riesgo 
            with col_g2:
                st.markdown("### Por nivel de riesgo")
                orden          = ["Bajo",    "Medio",   "Alto",    "Critico"]
                paleta_clara   = ["#6ee7b7", "#fde68a", "#fdba74", "#fca5a5"]

                conteo_riesgo = (
                    df["nivel_riesgo"]
                    .value_counts()
                    .reindex(orden)
                    .dropna()
                    .reset_index()
                )
                conteo_riesgo.columns = ["Nivel", "Cantidad"]

                colores_usados = [
                    paleta_clara[orden.index(n)]
                    for n in conteo_riesgo["Nivel"]
                ]

                fig2 = px.bar(
                    conteo_riesgo,
                    x="Nivel",
                    y="Cantidad",
                    template="plotly_dark",
                )
                fig2.update_traces(
                    marker_color=colores_usados,
                    marker_line_width=0
                )
                fig2.update_layout(
                    paper_bgcolor="#111827",
                    plot_bgcolor="#0d1526",
                    font=dict(
                        family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                        color="#cbd5e1"
                    ),
                    xaxis=dict(tickangle=0, title=None, gridcolor="#1e2d4a"),
                    yaxis=dict(title="Cantidad", dtick=1, tickformat="d", gridcolor="#1e2d4a"),
                    margin=dict(t=20, b=10, l=10, r=10),
                    showlegend=False,
                )
                st.plotly_chart(fig2, use_container_width=True)

    # Recomendaciones
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("## Recomendaciones por tipo")

        if total == 0:
            st.info("Registra incidencias para ver las recomendaciones.")
        else:
            vistas = set()
            for inc in gestor.lista_incidencias:
                if inc.tipo not in vistas:
                    vistas.add(inc.tipo)
                    icono = ICONOS_TIPO.get(inc.tipo, "")
                    nivel = inc.nivel_riesgo
                    color = COLORES_RIESGO.get(nivel, "#94a3b8")
                    st.markdown(f"""
                    <div class="rec-card">
                        <div class="rec-icon">{icono}</div>
                        <div>
                            <div class="rec-tipo">{inc.tipo}
                                <span class="badge" style="background:{color}33; color:{color}; border:1px solid {color}66">
                                    {nivel}
                                </span>
                            </div>
                            <div class="rec-texto">{inc.obtener_recomendacion()}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)