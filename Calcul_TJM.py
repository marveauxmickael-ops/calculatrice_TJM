import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Calculateur TJM & Marge Freelance",
    page_icon="💰",
    layout="centered"
)

# --- STYLE CSS ---
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    footer {visibility: hidden;}
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #ffffff;
        color: #555;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR : CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Configuration Annuelle")
    st.info("Ces paramètres définissent votre 'prix de revient' (CJM).")
    
    salaire_brut_cible = st.number_input(
        "Salaire brut annuel visé (€)", 
        min_value=0, value=55000, step=1000
    )
    
    coeff_charges = st.slider(
        "Coefficient de charges/frais",
        min_value=1.0, max_value=2.5, value=1.6, step=0.1,
        help="1.6 signifie que pour 1€ de salaire, vous devez facturer 1.60€ pour couvrir URSSAF, mutuelle, frais, etc."
    )
    
    jours_travailles = st.slider(
        "Jours facturables par an",
        100, 250, 210,
        help="Moyenne après congés et temps administratif."
    )

    st.divider()
    st.markdown("### 👨‍💻 À propos")
    st.write("Cet outil est proposé gratuitement afin d’aider les futurs freelances à suivre et optimiser leur rentabilité.")
    # MODIFIEZ ICI : Vos liens
    st.markdown("[Lien LinkedIn](https://linkedin.com/in/votre-profil)")

# --- CALCULS DE BASE ---
ca_annuel_necessaire = salaire_brut_cible * coeff_charges
cjm_equilibre = ca_annuel_necessaire / jours_travailles if jours_travailles > 0 else 0

# --- INTERFACE PRINCIPALE ---
st.title("🚀 Simulateur de TJM & Marge")
st.markdown("Calculez votre tarif idéal et la rentabilité de vos missions en temps réel.")

# SECTION 1 : POINT D'ÉQUILIBRE
st.subheader("1. Votre Coût de revient (CJM)")
col1, col2 = st.columns(2)
with col1:
    st.metric("CJM Minimum", f"{int(cjm_equilibre)} € HT", help="En dessous, vous n'atteignez pas votre objectif de salaire.")
with col2:
    st.metric("CA Annuel Cible", f"{int(ca_annuel_necessaire):,} €".replace(",", " "))

st.divider()

# SECTION 2 : SIMULATEUR DE MISSION
st.subheader("2. Simulation d'une mission")
col_sim1, col_sim2 = st.columns(2)

with col_sim1:
    tjm_propose = st.number_input("TJM facturé au client (€ HT)", min_value=0, value=int(cjm_equilibre + 100))
with col_sim2:
    duree_mission = st.number_input("Nombre de jours de la mission", min_value=1, value=20)

# Calculs mission
ca_mission = tjm_propose * duree_mission
cout_revient_mission = cjm_equilibre * duree_mission
marge_totale = ca_mission - cout_revient_mission
marge_pourcent = (marge_totale / ca_mission * 100) if ca_mission > 0 else 0

# Affichage résultats mission
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("CA Mission", f"{int(ca_mission):,} €")
m_col2.metric("Marge Brute", f"{int(marge_totale):,} €", delta=f"{int(marge_pourcent)} %")
m_col3.metric("Bénéfice / jour", f"{int(tjm_propose - cjm_equilibre)} €")

# Graphique de répartition
st.write("#### Répartition du CA de la mission")
donnees_chart = {
    "Catégorie": ["Salaire Cible", "Charges & Frais", "Marge Net (Profit)"],
    "Montant": [
        (salaire_brut_cible / jours_travailles) * duree_mission,
        ((ca_annuel_necessaire - salaire_brut_cible) / jours_travailles) * duree_mission,
        max(0, marge_totale)
    ]
}
df = pd.DataFrame(donnees_chart)
st.bar_chart(df.set_index("Catégorie"))

# Alertes
if tjm_propose < cjm_equilibre:
    st.error(f"⚠️ Attention : Votre TJM est inférieur à votre coût de revient ({int(cjm_equilibre)}€).")
elif marge_pourcent > 20:
    st.balloons()
    st.success("✨ Excellente marge ! Cette mission est très rentable.")

# FOOTER
st.markdown("""
    <div class="footer">
        Outil gratuit proposé par <b>Mickael.M</b> • <a href="https://votre-site.com" target="_blank">Portfolio</a>
    </div>
    """, unsafe_allow_html=True)
