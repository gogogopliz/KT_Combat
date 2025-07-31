
import streamlit as st

st.set_page_config(page_title="Combate Kill Team", layout="centered")

# Inicialización de estados
if "fase" not in st.session_state:
    st.session_state.fase = "inicio"
    st.session_state.dados = {
        "atacante": {"normales": 0, "criticos": 0},
        "defensor": {"normales": 0, "criticos": 0},
    }
    st.session_state.vidas = {"atacante": 10, "defensor": 10}
    st.session_state.dmg = {"normal": 3, "critico": 5}
    st.session_state.acciones = []
    st.session_state.bloqueados = {"atacante": [], "defensor": []}
    st.session_state.turno = "atacante"

# Función para reiniciar
def reiniciar():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Fase de inicio
if st.session_state.fase == "inicio":
    st.title("Simulador de Combate Cuerpo a Cuerpo - Kill Team 3")

    st.subheader("Datos del atacante")
    st.session_state.dados["atacante"]["normales"] = st.number_input("Éxitos normales (atacante)", 0, 10, 2)
    st.session_state.dados["atacante"]["criticos"] = st.number_input("Éxitos críticos (atacante)", 0, 10, 1)

    st.subheader("Datos del defensor")
    st.session_state.dados["defensor"]["normales"] = st.number_input("Éxitos normales (defensor)", 0, 10, 2)
    st.session_state.dados["defensor"]["criticos"] = st.number_input("Éxitos críticos (defensor)", 0, 10, 1)

    st.subheader("Datos generales")
    st.session_state.vidas["atacante"] = st.number_input("Vida del atacante", 1, 30, 10)
    st.session_state.vidas["defensor"] = st.number_input("Vida del defensor", 1, 30, 10)
    st.session_state.dmg["normal"] = st.number_input("Daño normal", 1, 10, 3)
    st.session_state.dmg["critico"] = st.number_input("Daño crítico", 1, 20, 5)

    if st.button("Iniciar combate"):
        st.session_state.fase = "combate"
        st.experimental_rerun()

# Función para mostrar dados disponibles
def mostrar_dados(jugador):
    normales = st.session_state.dados[jugador]["normales"]
    criticos = st.session_state.dados[jugador]["criticos"]
    bloqueados = st.session_state.bloqueados[jugador]

    st.write(f"**{jugador.upper()}**")
    col1, col2 = st.columns(2)
    with col1:
        for i in range(normales):
            if f"N{i}" not in bloqueados:
                if st.button(f"N{i+1} ({jugador[0]})", key=f"{jugador}_N_{i}"):
                    elegir_accion(jugador, f"N{i}")
    with col2:
        for i in range(criticos):
            if f"C{i}" not in bloqueados:
                if st.button(f"C{i+1} ({jugador[0]})", key=f"{jugador}_C_{i}"):
                    elegir_accion(jugador, f"C{i}")

# Función para elegir acción
def elegir_accion(jugador, dado_id):
    opciones = ["Golpear", "Bloquear"]
    eleccion = st.radio(f"Acción para {dado_id} ({jugador})", opciones, key=f"accion_{jugador}_{dado_id}")
    if st.button("Ejecutar", key=f"ejecutar_{jugador}_{dado_id}"):
        procesar_accion(jugador, dado_id, eleccion)
        st.experimental_rerun()

# Procesar acción del dado
def procesar_accion(jugador, dado_id, accion):
    oponente = "defensor" if jugador == "atacante" else "atacante"
    tipo = "normal" if dado_id.startswith("N") else "critico"
    dmg = st.session_state.dmg[tipo]

    if accion == "Golpear":
        st.session_state.vidas[oponente] -= dmg
    elif accion == "Bloquear":
        # Bloqueo automático del mejor dado válido
        pool = st.session_state.dados[oponente]
        bloqueables = []
        for i in range(pool["criticos"]):
            if f"C{i}" not in st.session_state.bloqueados[oponente]:
                bloqueables.append(("C", i))
        for i in range(pool["normales"]):
            if f"N{i}" not in st.session_state.bloqueados[oponente]:
                bloqueables.append(("N", i))

        bloqueado = None
        if tipo == "normal":
            for t, i in bloqueables:
                if t == "N":
                    bloqueado = f"{t}{i}"
                    break
        else:  # crítico
            for t, i in bloqueables:
                bloqueado = f"{t}{i}"
                break

        if bloqueado:
            st.session_state.bloqueados[oponente].append(bloqueado)

    # El dado usado también se elimina
    st.session_state.bloqueados[jugador].append(dado_id)

    # Cambiar turno
    st.session_state.turno = oponente

# Fase de combate
elif st.session_state.fase == "combate":
    st.header("Resolución del combate")
    st.write(f"Turno actual: **{st.session_state.turno.upper()}**")
    st.write(f"Vida del atacante: {st.session_state.vidas['atacante']}")
    st.write(f"Vida del defensor: {st.session_state.vidas['defensor']}")

    mostrar_dados(st.session_state.turno)

    if all_dados_resueltos() or alguno_muerto():
        st.success("Combate terminado.")
        st.button("Volver al inicio", on_click=reiniciar)

def all_dados_resueltos():
    for jugador in ["atacante", "defensor"]:
        total = (
            st.session_state.dados[jugador]["normales"]
            + st.session_state.dados[jugador]["criticos"]
        )
        if len(st.session_state.bloqueados[jugador]) < total:
            return False
    return True

def alguno_muerto():
    return (
        st.session_state.vidas["atacante"] <= 0
        or st.session_state.vidas["defensor"] <= 0
    )
