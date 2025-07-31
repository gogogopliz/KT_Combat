# combate_dados.py
import streamlit as st
import uuid

st.set_page_config(layout="wide")

# Estado inicial
if "dados" not in st.session_state:
    st.session_state.dados = {
        "att": {"crit": [], "norm": [], "hp": 12, "dmg_norm": 3, "dmg_crit": 5},
        "def": {"crit": [], "norm": [], "hp": 12, "dmg_norm": 2, "dmg_crit": 4},
    }
    st.session_state.bloqueados = {"att": set(), "def": set()}
    st.session_state.usados = {"att": set(), "def": set()}
    st.session_state.reset_key = str(uuid.uuid4())

def reiniciar():
    st.session_state.dados = {
        "att": {"crit": [], "norm": [], "hp": st.session_state.hp_att, "dmg_norm": st.session_state.dmg_n_att, "dmg_crit": st.session_state.dmg_c_att},
        "def": {"crit": [], "norm": [], "hp": st.session_state.hp_def, "dmg_norm": st.session_state.dmg_n_def, "dmg_crit": st.session_state.dmg_c_def},
    }
    st.session_state.bloqueados = {"att": set(), "def": set()}
    st.session_state.usados = {"att": set(), "def": set()}
    st.session_state.reset_key = str(uuid.uuid4())

# Inputs
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Atacante")
    st.session_state.hp_att = st.number_input("Vida inicial", 1, 50, 12, key="vida_att")
    st.session_state.dmg_n_att = st.number_input("Daño normal", 1, 10, 3, key="dmg_norm_att")
    st.session_state.dmg_c_att = st.number_input("Daño crítico", 1, 10, 5, key="dmg_crit_att")
    éxitos_normales_att = st.number_input("Éxitos normales", 0, 6, 2, key="norm_att")
    éxitos_criticos_att = st.number_input("Éxitos críticos", 0, 6, 1, key="crit_att")
with col2:
    st.markdown("### Defensor")
    st.session_state.hp_def = st.number_input("Vida inicial", 1, 50, 12, key="vida_def")
    st.session_state.dmg_n_def = st.number_input("Daño normal", 1, 10, 2, key="dmg_norm_def")
    st.session_state.dmg_c_def = st.number_input("Daño crítico", 1, 10, 4, key="dmg_crit_def")
    éxitos_normales_def = st.number_input("Éxitos normales", 0, 6, 2, key="norm_def")
    éxitos_criticos_def = st.number_input("Éxitos críticos", 0, 6, 1, key="crit_def")

# Actualizar dados según inputs
if len(st.session_state.dados["att"]["norm"]) != éxitos_normales_att or len(st.session_state.dados["att"]["crit"]) != éxitos_criticos_att or len(st.session_state.dados["def"]["norm"]) != éxitos_normales_def or len(st.session_state.dados["def"]["crit"]) != éxitos_criticos_def:
    reiniciar()
    st.session_state.dados["att"]["norm"] = [str(uuid.uuid4()) for _ in range(éxitos_normales_att)]
    st.session_state.dados["att"]["crit"] = [str(uuid.uuid4()) for _ in range(éxitos_criticos_att)]
    st.session_state.dados["def"]["norm"] = [str(uuid.uuid4()) for _ in range(éxitos_normales_def)]
    st.session_state.dados["def"]["crit"] = [str(uuid.uuid4()) for _ in range(éxitos_criticos_def)]

def render_dado(id_dado, tipo, bando):
    estilo = {
        "crit": "🟨",
        "norm": "⬜",
        "usado": "⬛",
        "muerto": "💀",
    }
    enemigo = "def" if bando == "att" else "att"
    estado = "muerto" if st.session_state.dados[bando]["hp"] <= 0 else (
        "usado" if id_dado in st.session_state.usados[bando] else tipo
    )
    bloqueado = id_dado in st.session_state.bloqueados[bando]
    opacidad = "50%" if estado in ["usado", "muerto"] or bloqueado else "100%"
    if estado == "muerto":
        st.markdown(f'<div style="display:inline-block; opacity:{opacidad}; font-size:30px;">{estilo[estado]}</div>', unsafe_allow_html=True)
        return

    if st.button(estilo[tipo], key=f"{id_dado}_{bando}", help="Pulsar para usar"):
        if id_dado in st.session_state.usados[bando] or st.session_state.dados[bando]["hp"] <= 0:
            return
        accion = st.radio(f"¿Qué hacer con este {tipo}?", ["Atacar", "Bloquear"], key=f"accion_{id_dado}")
        if accion == "Atacar":
            daño = st.session_state.dados[bando][f"dmg_{tipo}"]
            st.session_state.dados[enemigo]["hp"] -= daño
        elif accion == "Bloquear":
            for d in st.session_state.dados[enemigo]["crit"] + st.session_state.dados[enemigo]["norm"]:
                if d not in st.session_state.bloqueados[enemigo]:
                    st.session_state.bloqueados[enemigo].add(d)
                    break
        st.session_state.usados[bando].add(id_dado)
        st.rerun()

    st.markdown(f'<div style="display:inline-block; opacity:{opacidad}; font-size:30px;">{estilo[tipo]}</div>', unsafe_allow_html=True)

# Mostrar dados
def mostrar_fila(bando):
    enemigo = "def" if bando == "att" else "att"
    st.write(f"**{bando.upper()} - Vida restante: {st.session_state.dados[bando]['hp']}**")
    col_vida, col_dados = st.columns([1, 9])
    with col_vida:
        st.markdown(f"❤️ {st.session_state.dados[bando]['hp']}")
    with col_dados:
        for tipo in ["crit", "norm"]:
            for dado in st.session_state.dados[bando][tipo]:
                render_dado(dado, tipo, bando)

mostrar_fila("att")
mostrar_fila("def")

# Botón de reinicio
st.button("🔁 Reiniciar", on_click=reiniciar, key=st.session_state.reset_key)