import streamlit as st

st.set_page_config(page_title="Simulador de Combate KT3", layout="wide")

if "vidas" not in st.session_state:
    st.session_state.vidas = {"atacante": 12, "defensor": 12}
if "dados_atacante" not in st.session_state:
    st.session_state.dados_atacante = []
if "dados_defensor" not in st.session_state:
    st.session_state.dados_defensor = []
if "acciones" not in st.session_state:
    st.session_state.acciones = []

st.title("⚔️ Simulador de Combate KT3")

col1, col2 = st.columns(2)
with col1:
    st.header("Atacante")
    vida_ata = st.number_input("Vida", 1, 30, st.session_state.vidas["atacante"], key="vida_ata")
    st.session_state.vidas["atacante"] = vida_ata
    norm_atac = st.number_input("Éxitos normales", 0, 6, 2, key="norm_atac")
    crit_atac = st.number_input("Críticos", 0, 6, 1, key="crit_atac")
    dmg_norm_atac = st.number_input("Daño normal", 1, 10, 3)
    dmg_crit_atac = st.number_input("Daño crítico", 1, 10, 5)

with col2:
    st.header("Defensor")
    vida_def = st.number_input("Vida", 1, 30, st.session_state.vidas["defensor"], key="vida_def")
    st.session_state.vidas["defensor"] = vida_def
    norm_def = st.number_input("Éxitos normales", 0, 6, 2, key="norm_def")
    crit_def = st.number_input("Críticos", 0, 6, 1, key="crit_def")
    dmg_norm_def = st.number_input("Daño normal", 1, 10, 2)
    dmg_crit_def = st.number_input("Daño crítico", 1, 10, 4)

def generar_dados(norm, crit, jugador):
    return [{"tipo": "crítico", "usado": False, "id": f"{jugador}_c_{i}"} for i in range(crit)] + \
           [{"tipo": "normal", "usado": False, "id": f"{jugador}_n_{i}"} for i in range(norm)]

def mostrar_dados(dados_atac, dados_def, dmg_norm_a, dmg_crit_a, dmg_norm_d, dmg_crit_d):
    col_a, col_d = st.columns(2)

    with col_a:
        st.subheader("Atacante")
        st.markdown(f"❤️ Vida: {st.session_state.vidas['atacante']}")
        for dado in dados_atac:
            if st.button(
                f"{dado['tipo'].capitalize()}",
                key=f"{dado['id']}",
                help="Haz clic para usar este dado",
            ):
                aplicar_impacto(dado, "atacante", dados_def, dmg_norm_a, dmg_crit_a)

    with col_d:
        st.subheader("Defensor")
        st.markdown(f"❤️ Vida: {st.session_state.vidas['defensor']}")
        for dado in dados_def:
            if st.button(
                f"{dado['tipo'].capitalize()}",
                key=f"{dado['id']}",
                help="Haz clic para usar este dado",
            ):
                aplicar_impacto(dado, "defensor", dados_atac, dmg_norm_d, dmg_crit_d)

def aplicar_impacto(dado, jugador, oponente_dados, dmg_norm, dmg_crit):
    objetivo = "defensor" if jugador == "atacante" else "atacante"

    # Buscar primer dado no usado del oponente
    for op_dado in oponente_dados:
        if not op_dado["usado"]:
            op_dado["usado"] = True
            return  # Se ha bloqueado un dado

    # Si no hay dados que bloquear, se inflige daño
    daño = dmg_crit if dado["tipo"] == "crítico" else dmg_norm
    st.session_state.vidas[objetivo] = max(0, st.session_state.vidas[objetivo] - daño)

# Botón para iniciar combate
if st.button("🔁 Iniciar nuevo combate"):
    st.session_state.dados_atacante = generar_dados(norm_atac, crit_atac, "atacante")
    st.session_state.dados_defensor = generar_dados(norm_def, crit_def, "defensor")

# Mostrar dados si los hay
if st.session_state.dados_atacante or st.session_state.dados_defensor:
    mostrar_dados(
        st.session_state.dados_atacante,
        st.session_state.dados_defensor,
        dmg_norm_atac,
        dmg_crit_atac,
        dmg_norm_def,
        dmg_crit_def
    )