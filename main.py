
import streamlit as st


def main():

    st.title("Mi primera app")

    nombre = st.text_input("Introduce tu nombre")

    if st.button("Salida"):
        st.write("Hola {nombre}")
    
if __name__ == "__main__":
    main()