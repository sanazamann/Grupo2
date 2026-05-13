import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

from src.controllers.GestorIncidencias import GestorIncidencias
from src.clases.Phishing import Phishing
from src.clases.malware import Malware
from src.clases.ataque_fuerza_bruta import AtaqueFuerzaBruta
from src.clases.fuga_datos import FugaDatos
from src.clases.acceso_no_autorizado import AccesoNoAutorizado
from src.clases.excepciones import ErrorIncidencia

ARCHIVO_JSON = "incidencias.json"

COLORES_RIESGO = {
    "Bajo": "#34d399",
    "Medio": "#fbbf24",
    "Alto": "#fb923c",
    "Critico": "#f87171",
}

ICONOS_TIPO = {
    "Phishing": "🎣",
    "Malware": "🦠",
    "Ataque de fuerza bruta": "🔨",
    "Fuga de datos": "💧",
    "Acceso no autorizado": "🚪",
}


def imagen_a_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def normalizar_riesgo(valor):
    if valor == "Crítico":
        return "Critico"
    return valor


def aplicar_estilos(img_b64="", img_ext="jpeg"):

    landing_bg = f"""
        background-image: url('data:image/{img_ext};base64,{img_b64}');
        background-size: cover;
        background-position: center center;
    """ if img_b64 else "background: linear-gradient(135deg, #fdf4ff, #fff0f9);"

    dashboard_bg = """
        background: linear-gradient(135deg, #fff1f7, #fdeff6, #fff7fb);
    """

    st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}

    .stApp > header {{ display: none !important; }}
    header[data-testid="stHeader"] {{ display: none !important; height: 0 !important; }}
    #root > div:first-child {{ padding-top: 0 !important; }}
    .stApp {{ margin-top: 0 !important; }}
    .main .block-container {{ padding-top: 0 !important; }}
    div[data-testid="stToolbar"] {{ display: none !important; }}
    div[data-testid="stDecoration"] {{ display: none !important; }}
    div[data-testid="stStatusWidget"] {{ display: none !important; }}

    section[data-testid="stSidebar"] {{ display: none !important; }}
    .stAppDeployButton {{ display: none !important; }}

    .stApp {{
        {dashboard_bg}
        color: #1e293b;
    }}

    .landing-wrap {{
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
        z-index: 9999;
        overflow: hidden;
        {landing_bg}
    }}

    .landing-overlay {{
        position: absolute;
        inset: 0;
        background: linear-gradient(
            to right,
            rgba(255,255,255,0.55) 0%,
            rgba(255,255,255,0.10) 50%,
            rgba(255,255,255,0.0) 100%
        );
    }}

    .landing-logo {{
        position: absolute;
        top: 2.5rem;
        left: 4vw;
        font-size: 1rem;
        font-weight: 800;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #7c3aed;
    }}

    .navbar-logo {{
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        background: linear-gradient(135deg, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .navbar-title {{
        font-size: 0.88rem;
        color: #64748b;
    }}

    h2 {{
        font-weight: 700 !important;
        color: #7c3aed !important;
        border-bottom: 2px solid #ede9fe;
        padding-bottom: 0.4rem;
        margin-top: 0 !important;
    }}

    h3 {{
        font-weight: 600 !important;
        color: #9333ea !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255,255,255,0.85);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid #e2e8f0;
    }}

    .stTabs [data-baseweb="tab"] {{
        font-weight: 600;
        font-size: 0.88rem;
        color: #94a3b8 !important;
        border-radius: 9px;
        padding: 0.5rem 1.2rem;
        border: none !important;
        background: transparent !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #a855f7, #ec4899) !important;
        color: white !important;
    }}

    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    .stButton > button {{
        border-radius: 50px;
        background: linear-gradient(135deg, #a855f7, #ec4899);
        color: white !important;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        padding: 0.7rem 2rem;
        box-shadow: 0 6px 20px rgba(168,85,247,0.35);
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(168,85,247,0.45);
    }}

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {{
        background-color: rgba(255,255,255,0.95) !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        color: #1e293b !important;
    }}

    .stSelectbox > div > div {{
        background-color: rgba(255,255,255,0.95) !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        color: #1e293b !important;
    }}

    .stCheckbox label {{
        color: #475569 !important;
    }}

    [data-testid="metric-container"] {{
        background: rgba(255,255,255,0.9);
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }}

    [data-testid="stMetricValue"] {{
        color: #7c3aed !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }}

    .rec-card {{
        background: rgba(255,255,255,0.92);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
        display: flex;
        align-items: flex-start;
        gap: 0.9rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    }}

    .rec-icon {{
        font-size: 1.6rem;
    }}

    .rec-tipo {{
        font-weight: 700;
        color: #7c3aed;
        font-size: 0.9rem;
        margin-bottom: 0.15rem;
    }}

    .rec-texto {{
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.5;
    }}

    .badge {{
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-left: 0.4rem;
    }}

    .stDataFrame {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    }}

    .main .block-container {{
        padding-top: 0 !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px;
    }}
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
        page_title="Nexora",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    img_b64, img_ext = "", "jpeg"

    for nombre in ["portada.jpeg", "portada.jpg", "portada.png"]:
        if os.path.exists(nombre):
            img_b64 = imagen_a_base64(nombre)
            img_ext = nombre.split(".")[-1].replace("jpg", "jpeg")
            break

    aplicar_estilos(img_b64, img_ext)

    if "pagina" not in st.session_state:
        st.session_state.pagina = "landing"

    if "gestor" not in st.session_state:
        st.session_state.gestor = GestorIncidencias("Gestor principal")
        cargar_datos_json(st.session_state.gestor)

    gestor = st.session_state.gestor

    if st.session_state.pagina == "landing":

        st.markdown("""
        <div class="landing-wrap">
            <div class="landing-overlay"></div>
            <div class="landing-logo">Nexora</div>
            <button class="landing-btn-html"
                onclick="window.parent.document.querySelectorAll('button').forEach(b=>{ if(b.innerText.trim()=='Entrar al sistema'){b.click()} })">
                Entrar al sistema
            </button>
        </div>

        <style>
        .landing-btn-html {
            position: fixed;
            bottom: 10vh;
            left: 5vw;
            z-index: 99999;
            background: linear-gradient(135deg, #a855f7, #ec4899);
            color: white;
            font-weight: 700;
            font-size: 1.05rem;
            padding: 0.9rem 2.5rem;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            box-shadow: 0 8px 25px rgba(168,85,247,0.4);
        }

        div[data-testid="stButton"] > button {
            position: fixed !important;
            bottom: 10vh !important;
            left: 5vw !important;
            opacity: 0 !important;
            z-index: 99998 !important;
            width: 220px !important;
            height: 55px !important;
            pointer-events: all !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.button("Entrar al sistema", key="btn-entrar"):
            st.session_state.pagina = "app"
            st.rerun()

        return

    col_n1, col_n2, col_n3 = st.columns([1, 4, 1])

    with col_n1:
        st.markdown('<div class="navbar-logo">Nexora</div>', unsafe_allow_html=True)

    with col_n2:
        st.markdown(
            '<div class="navbar-title" style="text-align:center">Sistema de Incidencias de Ciberseguridad</div>',
            unsafe_allow_html=True
        )

    with col_n3:
        if st.button("Volver al inicio"):
            st.session_state.pagina = "landing"
            st.rerun()

    st.markdown("<hr style='border-color:#e2e8f0; margin:0 0 1.5rem'>", unsafe_allow_html=True)

    df = gestor.convertir_a_dataframe()

    if len(df) > 0:
        df["nivel_riesgo"] = df["nivel_riesgo"].replace("Crítico", "Critico")

    total = len(df)

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric("Total", total)

    with c2:
        st.metric("Criticas", int(len(df[df["nivel_riesgo"] == "Critico"])) if total > 0 else 0)

    with c3:
        st.metric("Altas", int(len(df[df["nivel_riesgo"] == "Alto"])) if total > 0 else 0)

    with c4:
        st.metric("Medias", int(len(df[df["nivel_riesgo"] == "Medio"])) if total > 0 else 0)

    with c5:
        st.metric("Bajas", int(len(df[df["nivel_riesgo"] == "Bajo"])) if total > 0 else 0)

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
        st.markdown("<p style='color:#64748b'>Selecciona el tipo e introduce los datos del incidente.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

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

                enlace = st.checkbox("Contiene enlace sospechoso")
                remitente = st.checkbox("Remitente desconocido")

                if st.button("Registrar Phishing", use_container_width=True):
                    incidencia = Phishing(canal, enlace, remitente)

            elif tipo == "Malware":
                payload = st.text_input("Payload detectado", "Robo de credenciales")

                c1, c2, c3 = st.columns(3)

                with c1:
                    persistencia_v = st.checkbox("Persistencia")

                with c2:
                    propagacion_v = st.checkbox("Propagacion")

                with c3:
                    sigilo_v = st.checkbox("Sigilo")

                if st.button("Registrar Malware", use_container_width=True):
                    incidencia = Malware(persistencia_v, propagacion_v, sigilo_v, payload)

            elif tipo == "Ataque de fuerza bruta":
                col1, col2 = st.columns(2)

                with col1:
                    intentos = st.number_input("Numero de intentos", min_value=0, step=1)

                with col2:
                    red = st.number_input("Red ID", min_value=0, step=1)

                c1, c2 = st.columns(2)

                with c1:
                    acceso_admin = st.checkbox("Acceso admin")

                with c2:
                    usa_contra = st.checkbox("Utiliza contrasenas comunes")

                if st.button("Registrar Ataque de fuerza bruta", use_container_width=True):
                    incidencia = AtaqueFuerzaBruta(intentos, red, acceso_admin, usa_contra)

            elif tipo == "Fuga de datos":
                col1, col2 = st.columns(2)

                with col1:
                    datos_afectados = st.text_input("Datos afectados", "Correos y contrasenas")
                    origen = st.text_input("Origen de la fuga", "Servidor externo")

                with col2:
                    num_registros = st.number_input("Numero de registros", min_value=1, step=1)

                if st.button("Registrar Fuga de datos", use_container_width=True):
                    incidencia = FugaDatos(datos_afectados, num_registros, origen)

            elif tipo == "Acceso no autorizado":
                col1, col2 = st.columns(2)

                with col1:
                    usuario = st.text_input("Usuario afectado", "admin01")

                with col2:
                    sistema = st.text_input("Sistema afectado", "Panel interno")

                priv_admin = st.checkbox("Tiene privilegios de administrador")

                if st.button("Registrar Acceso no autorizado", use_container_width=True):
                    incidencia = AccesoNoAutorizado(usuario, sistema, priv_admin)

            if incidencia:
                gestor.agregar_incidencia(incidencia)
                gestor.guardar_en_json(ARCHIVO_JSON)

                nivel = normalizar_riesgo(incidencia.nivel_riesgo)
                color = COLORES_RIESGO.get(nivel, "#94a3b8")

                st.markdown(f"""
                <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-left:4px solid #22c55e;
                    border-radius:10px; padding:1rem 1.2rem; margin-top:1rem;">
                    <div style="color:#16a34a; font-weight:700; font-size:1rem; margin-bottom:0.3rem;">
                        Incidencia registrada correctamente
                    </div>
                    <div style="color:#475569; font-size:0.88rem;">
                        Tipo: <strong style="color:#1e293b">{tipo}</strong>
                        &nbsp;&nbsp;|&nbsp;&nbsp;
                        Nivel de riesgo:
                        <span style="background:{color}22; color:{color}; border:1px solid {color}55;
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
            col_f1, col_f2, col_f3 = st.columns([2, 2, 1])

            with col_f1:
                filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos"] + list(df["tipo"].unique()))

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

            if filtro_tipo != "Todos":
                df_filtrado = df_filtrado[df_filtrado["tipo"] == filtro_tipo]

            if filtro_riesgo != "Todos":
                df_filtrado = df_filtrado[df_filtrado["nivel_riesgo"] == filtro_riesgo]

            st.markdown(
                f"<p style='color:#64748b; font-size:0.85rem'>{len(df_filtrado)} incidencia(s) encontrada(s)</p>",
                unsafe_allow_html=True
            )

            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "tipo": st.column_config.TextColumn("Tipo", width="medium"),
                    "nivel_riesgo": st.column_config.TextColumn("Nivel de riesgo", width="small"),
                    "recomendacion": st.column_config.TextColumn("Recomendacion", width="large"),
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

            with col_g1:
                st.markdown("### Por tipo")

                conteo_tipo = df["tipo"].value_counts().reset_index()
                conteo_tipo.columns = ["Tipo", "Cantidad"]

                fig1 = px.bar(conteo_tipo, x="Tipo", y="Cantidad", template="none")
                fig1.update_traces(marker_color="#a78bfa", marker_line_width=0)

                fig1.update_layout(
                    paper_bgcolor="rgba(255,255,255,1)",
                    plot_bgcolor="rgba(255,255,255,1)",
                    font=dict(family="-apple-system,'Segoe UI',sans-serif", color="#334155", size=12),
                    xaxis=dict(title=None, gridcolor="#e2e8f0", linecolor="#cbd5e1", tickfont=dict(size=11)),
                    yaxis=dict(title="Cantidad", dtick=1, tickformat="d", gridcolor="#e2e8f0", tickfont=dict(size=11)),
                    margin=dict(t=20, b=20, l=20, r=20),
                    showlegend=False,
                    bargap=0.35,
                )

                st.plotly_chart(fig1, use_container_width=True)

            with col_g2:
                st.markdown("### Por nivel de riesgo")

                df_grafica = df.copy()
                df_grafica["nivel_riesgo"] = df_grafica["nivel_riesgo"].replace("Crítico", "Critico")

                orden = ["Bajo", "Medio", "Alto", "Critico"]
                paleta_pastel = ["#6ee7b7", "#fde68a", "#fdba74", "#fca5a5"]

                conteo_riesgo = (
                    df_grafica["nivel_riesgo"]
                    .value_counts()
                    .reindex(orden)
                    .fillna(0)
                    .reset_index()
                )

                conteo_riesgo.columns = ["Nivel", "Cantidad"]
                conteo_riesgo["Cantidad"] = conteo_riesgo["Cantidad"].astype(int)

                colores_usados = [paleta_pastel[orden.index(n)] for n in conteo_riesgo["Nivel"]]

                fig2 = px.bar(conteo_riesgo, x="Nivel", y="Cantidad", template="none")
                fig2.update_traces(marker_color=colores_usados, marker_line_width=0)

                fig2.update_layout(
                    paper_bgcolor="rgba(255,255,255,1)",
                    plot_bgcolor="rgba(255,255,255,1)",
                    font=dict(family="-apple-system,'Segoe UI',sans-serif", color="#334155", size=12),
                    xaxis=dict(title=None, gridcolor="#e2e8f0", linecolor="#cbd5e1", tickfont=dict(size=11)),
                    yaxis=dict(title="Cantidad", dtick=1, tickformat="d", gridcolor="#e2e8f0", tickfont=dict(size=11)),
                    margin=dict(t=20, b=20, l=20, r=20),
                    showlegend=False,
                    bargap=0.35,
                )

                st.plotly_chart(fig2, use_container_width=True)

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
                    nivel = normalizar_riesgo(inc.nivel_riesgo)
                    color = COLORES_RIESGO.get(nivel, "#94a3b8")

                    st.markdown(f"""
                    <div class="rec-card">
                        <div class="rec-icon">{icono}</div>
                        <div>
                            <div class="rec-tipo">{inc.tipo}
                                <span class="badge" style="background:{color}22; color:{color}; border:1px solid {color}55;">
                                    {nivel}
                                </span>
                            </div>
                            <div class="rec-texto">{inc.obtener_recomendacion()}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)