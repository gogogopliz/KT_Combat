
import streamlit as st

st.set_page_config(page_title="Simulador de Combate Kill Team", layout="centered")

# Inicialización
if "estado" not in st.session_state:
    st.session_state.estado = "inicio"
    st.session_state.atacante = {"vida": 10, "dano_n": 3, "dano_c": 5, "normales": 0, "criticos": 0, "dados": []}
    st.session_state.defensor = {"vida": 10, "dano_n": 3, "dano_c": 5, "normales": 0, "criticos": 0, "dados": []}
    st.session_state.turno = "atacante"
    st.session_state.log = []

# Función para mostrar los dados
def mostrar_dados(jugador):
    dados = []
    for i, d in enumerate(jugador["dados"]):
        if not d["usado"]:
            estilo = "color: red;" if d["critico"] else "color: black;"
            botones = st.columns([1,1])
            with botones[0]:
                if st.button("⚔️", key=f"golpear_{jugador['nombre']}_{i}"):
                    aplicar_golpe(jugador, i)
            with botones[1]:
                if st.button("🛡️", key=f"bloquear_{jugador['nombre']}_{i}"):
                    st.session_state.bloqueando = (jugador['nombre'], i)
            st.markdown(f"<span style='{estilo} font-size: 24px;'>🎲</span>", unsafe_allow_html=True)

# Aplicar golpe
def aplicar_golpe(jugador, i):
    objetivo = st.session_state.defensor if jugador == st.session_state.atacante else st.session_state.atacante
    dado = jugador["dados"][i]
    dano = jugador["dano_c"] if dado["critico"] else jugador["dano_n"]
    objetivo["vida"] -= dano
    dado["usado"] = True
    st.session_state.log.append(f"{jugador['nombre']} golpea por {dano} de daño.")
    comprobar_estado()

# Aplicar bloqueo
def aplicar_bloqueo(bloqueador, id_bloqueo, objetivo, id_objetivo):
    d_bloqueo = bloqueador["dados"][id_bloqueo]
    d_obj = objetivo["dados"][id_objetivo]
    if d_obj["usado"]: return
    if not d_bloqueo["critico"] and d_obj["critico"]:
        st.warning("Un éxito normal no puede bloquear un crítico.")
        return
    d_bloqueo["usado"] = True
    d_obj["usado"] = True
    st.session_state.log.append(f"{bloqueador['nombre']} bloquea un dado de {objetivo['nombre']}.")

# Comprobar fin
def comprobar_estado():
    if st.session_state.atacante["vida"] <= 0:
        st.session_state.estado = "fin"
        st.session_state.log.append("¡Atacante ha sido incapacitado!")
    elif st.session_state.defensor["vida"] <= 0:
        st.session_state.estado = "fin"
        st.session_state.log.append("¡Defensor ha sido incapacitado!")

# ENTRADA DE DATOS
if st.session_state.estado == "inicio":
    st.title("Simulador de Combate - Kill Team")
    st.subheader("Datos del Atacante")
    st.session_state.atacante["vida"] = st.number_input("Vida del Atacante", 1, 30, 10)
    st.session_state.atacante["dano_n"] = st.number_input("Daño normal del Atacante", 1, 10, 3)
    st.session_state.atacante["dano_c"] = st.number_input("Daño crítico del Atacante", 1, 10, 5)
    st.session_state.atacante["normales"] = st.number_input("Éxitos normales Atacante", 0, 10, 2)
    st.session_state.atacante["criticos"] = st.number_input("Éxitos críticos Atacante", 0, 10, 1)

    st.subheader("Datos del Defensor")
    st.session_state.defensor["vida"] = st.number_input("Vida del Defensor", 1, 30, 10)
    st.session_state.defensor["dano_n"] = st.number_input("Daño normal del Defensor", 1, 10, 3)
    st.session_state.defensor["dano_c"] = st.number_input("Daño crítico del Defensor", 1, 10, 5)
    st.session_state.defensor["normales"] = st.number_input("Éxitos normales Defensor", 0, 10, 1)
    st.session_state.defensor["criticos"] = st.number_input("Éxitos críticos Defensor", 0, 10, 1)

    if st.button("Iniciar combate"):
        st.session_state.atacante["dados"] = [{"critico": False, "usado": False} for _ in range(st.session_state.atacante["normales"])]
        st.session_state.atacante["dados"] += [{"critico": True, "usado": False} for _ in range(st.session_state.atacante["criticos"])]
        st.session_state.atacante["nombre"] = "atacante"

        st.session_state.defensor["dados"] = [{"critico": False, "usado": False} for _ in range(st.session_state.defensor["normales"])]
        st.session_state.defensor["dados"] += [{"critico": True, "usado": False} for _ in range(st.session_state.defensor["criticos"])]
        st.session_state.defensor["nombre"] = "defensor"
        st.session_state.estado = "combate"

# COMBATE
elif st.session_state.estado == "combate":
    st.title("Combate en curso")
    st.write(f"Vida Atacante: {st.session_state.atacante['vida']} | Vida Defensor: {st.session_state.defensor['vida']}")

    st.subheader("Dados del Atacante")
    mostrar_dados(st.session_state.atacante)
    st.subheader("Dados del Defensor")
    mostrar_dados(st.session_state.defensor)

    # Si se ha pulsado bloquear
    if "bloqueando" in st.session_state:
        nombre_bloqueador, id_bloqueo = st.session_state.bloqueando
        bloqueador = st.session_state.atacante if nombre_bloqueador == "atacante" else st.session_state.defensor
        objetivo = st.session_state.defensor if bloqueador == st.session_state.atacante else st.session_state.atacante
        st.subheader("Selecciona dado enemigo para bloquear")
        for i, d in enumerate(objetivo["dados"]):
            if d["usado"]: continue
            puede_bloquear = d["critico"] if not bloqueador["dados"][id_bloqueo]["critico"] else True
            if puede_bloquear:
                if st.button(f"Bloquear dado {'crítico' if d['critico'] else 'normal'} ({objetivo['nombre']} #{i})", key=f"bloqueo_final_{i}"):
                    aplicar_bloqueo(bloqueador, id_bloqueo, objetivo, i)
                    del st.session_state.bloqueando
                    break

    st.subheader("Historial de combate")
    for entrada in st.session_state.log:
        st.write(entrada)

# FIN
elif st.session_state.estado == "fin":
    st.title("Combate Finalizado")
    st.write(f"Vida final del Atacante: {st.session_state.atacante['vida']}")
    st.write(f"Vida final del Defensor: {st.session_state.defensor['vida']}")
    for entrada in st.session_state.log:
        st.write(entrada)
    if st.button("Reiniciar"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
