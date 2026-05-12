import streamlit as st
import pandas as pd

from GestorIncidencias import GestorIncidencias
from Phishing import Phishing 
from malware import Malware
from ataque_fuerza_bruta import AtaqueFuerzaBruta
from fuga_datos import FugaDatos
from acceso_no_autorizado import AccesoNoAutorizado
from excepciones import ErrorIncidencia


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

        col3, col4, col5 = st.columns(3)

        with col3:
            if st.button("Guardar JSON"):
                gestor.guardar_en_json("incidencias.json")
                st.success("Datos guardados en incidencias.json")

        with col4:
            if st.button("Guardar CSV"):
                gestor.guardar_en_csv("incidencias.csv")
                st.success("Datos guardados en incidencias.csv")

        with col5:
            if st.button("Cargar JSON"):
                datos = gestor.cargar_desde_json("incidencias.json")
                st.write(datos)