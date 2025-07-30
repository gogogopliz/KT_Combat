
import streamlit as st

st.set_page_config(page_title="Simulador Cuerpo a Cuerpo - Kill Team 3", layout="wide")

# ICONOS
ICON_HIT = "🗡️"
ICON_CRIT = "💥"
ICON_BLOCK = "🛡️"

# CONFIGURACIÓN
estrategia = st.sidebar.selectbox("Estrategia", ["Mejor resultado", "Máximo daño", "Defensiva"], index=0)

st.markdown("## Configuración de los combatientes")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Atacante")
    vida_atacante = st.number_input("Vida inicial atacante", min_value=1, value=10, key="vida_a")
    daño_normal_a = st.number_input("Daño por éxito normal", min_value=1, value=3, key="daño_normal_a")
    daño_critico_a = st.number_input("Daño por éxito crítico", min_value=1, value=5, key="daño_critico_a")
    éxitos_normales_a = st.number_input("Éxitos normales", min_value=0, value=2, key="normales_a")
    éxitos_criticos_a = st.number_input("Éxitos críticos", min_value=0, value=1, key="criticos_a")

with col2:
    st.markdown("### Defensor")
    vida_defensor = st.number_input("Vida inicial defensor", min_value=1, value=10, key="vida_d")
    daño_normal_d = st.number_input("Daño por éxito normal", min_value=1, value=2, key="daño_normal_d")
    daño_critico_d = st.number_input("Daño por éxito crítico", min_value=1, value=4, key="daño_critico_d")
    éxitos_normales_d = st.number_input("Éxitos normales", min_value=0, value=2, key="normales_d")
    éxitos_criticos_d = st.number_input("Éxitos críticos", min_value=0, value=1, key="criticos_d")

if st.button("Simular combate"):
    a_hits = ["crit"] * éxitos_criticos_a + ["norm"] * éxitos_normales_a
    d_hits = ["crit"] * éxitos_criticos_d + ["norm"] * éxitos_normales_d

    log = []
    turno = "atacante"
    idx_a = idx_d = 0

    def bloquear(own, enemy):
        for i, e in enumerate(enemy):
            if e == "crit":
                enemy.pop(i)
                return True
        for i, e in enumerate(enemy):
            if e == "norm":
                enemy.pop(i)
                return True
        return False

    while (a_hits or d_hits) and vida_atacante > 0 and vida_defensor > 0:
        if turno == "atacante" and a_hits:
            actual = a_hits.pop(0)
            if estrategia == "Defensiva":
                bloqueado = bloquear(a_hits, d_hits)
                log.append(f"{ICON_BLOCK} Atacante bloquea ({'💥' if actual=='crit' else ICON_HIT})")
            elif estrategia == "Máximo daño" or estrategia == "Mejor resultado":
                dmg = daño_critico_a if actual == "crit" else daño_normal_a
                vida_defensor -= dmg
                log.append(f"{ICON_CRIT if actual == 'crit' else ICON_HIT} Atacante golpea: -{dmg} (Defensor: {max(vida_defensor,0)}❤️)")
        elif turno == "defensor" and d_hits:
            actual = d_hits.pop(0)
            if estrategia == "Defensiva":
                bloqueado = bloquear(d_hits, a_hits)
                log.append(f"{ICON_BLOCK} Defensor bloquea ({'💥' if actual=='crit' else ICON_HIT})")
            elif estrategia == "Máximo daño" or estrategia == "Mejor resultado":
                dmg = daño_critico_d if actual == "crit" else daño_normal_d
                vida_atacante -= dmg
                log.append(f"{ICON_CRIT if actual == 'crit' else ICON_HIT} Defensor golpea: -{dmg} (Atacante: {max(vida_atacante,0)}❤️)")
        turno = "defensor" if turno == "atacante" else "atacante"

        if vida_defensor <= 0:
            log.append("💀 ¡El defensor ha muerto!")
            break
        if vida_atacante <= 0:
            log.append("💀 ¡El atacante ha muerto!")
            break

    st.markdown("## Resultado del combate")
    for evento in log:
        st.markdown(f"- {evento}")
