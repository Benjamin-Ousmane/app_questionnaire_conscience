import streamlit as st
import pandas as pd
import time

from datetime import datetime

# Path of the output excel file
file_path = "/mnt/eval_conscience_data.xlsx" # to run with .exe app
# file_path = "eval_conscience_data.xlsx" # to run in streamlit app 
#-----------------------------------------------------------------------
st.set_page_config(layout="wide")

# Initialize widget values
if 'hour' not in st.session_state:
    st.session_state.hour = None
if 'minutes' not in st.session_state:
    st.session_state.minutes = None
if 'matricule' not in st.session_state:
    st.session_state.matricule = ""
if 'evaluator' not in st.session_state:
    st.session_state.evaluator = None
if 'presence' not in st.session_state:
    st.session_state.presence = 0.0
if 'eveil' not in st.session_state:
    st.session_state.eveil = 0.0
if 'conscient' not in st.session_state:
    st.session_state.conscient = None
if 'changement' not in st.session_state:
    st.session_state.changement = None
if 'commentaire' not in st.session_state:
    st.session_state.commentaire = ""
    
# Pour désactiver le button 
if 'run_button' in st.session_state and st.session_state.run_button is True:
    st.session_state.running = True
else:
    st.session_state.running = False

hour_list = [f"{i:02}" for i in range(24)]  # '00' to '23'
minutes_list = [f"{i:02}" for i in range(60)]  # '00' to '59'

#-----------------------------------------------------------------------
# Custom CSS to hide settings and custom the slider widget
hide_slider_labels = """
    <style>
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>

    <style>
        hr {
            margin-top: 5px !important;
            margin-bottom: 5px !important;
        }
    </style>

    <style>
        h3 {
            font-size: 18px !important;  /* Modifier la taille du texte */
            margin-bottom: 0px !important;  /* Réduire l'espacement en bas */
            margin-top: 0px !important;  /* Réduire l'espacement en haut */
        }
    </style>

    <style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }
    </style>

    <style>
    /* Hide min/max labels */
    div[data-baseweb="slider"] div:nth-of-type(2) {
        display: none !important;
    }
    
    /* Hide tooltip that shows selected value */
    div[data-testid="stSliderThumbValue"] {
        display: none !important;
    }

    /* Add a thick blue tick mark in the middle of the slider */
    div[data-baseweb="slider"]::before {
        content: "|";  /* The tick */
        font-size: 28px;  /* Make it bigger */
        font-weight: bold;  /* Make it thicker */
        color: rgba(172, 177, 195, 0.25);  /* Set tick color to blue */
        position: absolute;
        left: 50%; /* Center it */
        top: 50%;
        transform: translate(-50%, -50%);
    }

    </style>
"""
st.markdown(hide_slider_labels, unsafe_allow_html=True)

#-----------------------------------------------------------------------

st.title("Échelle d'évalution subjective de la conscience")

col1, col2, col3= st.columns([8, 1, 8])

with col1 :
    inp1, inp2, inp3, inp4= st.columns([1, 1, 1, 3])
    
    with inp1:
        hour = st.selectbox(
            label="Heures", 
            options= hour_list,
            key="hour",
            placeholder=""
        )       
    with inp2:
        minutes = st.selectbox(
            label="Minutes", 
            options= minutes_list, 
            key="minutes",
            placeholder=""
        )
    with inp3:
        matricule = st.text_input( 
            label="Matricule HCL", 
            key="matricule"
        )  
    with inp4:
        options = [
        "Médecin", 
        "MK", 
        "IDE", 
        "AS",
        "Proche"
        ]

        evaluator = st.radio(
            label="Evaluateur", 
            options=options, 
            horizontal=True, 
            key="evaluator"
        )

    st.divider()

    #----------------------------

    st.subheader("Selon vous, à quel point le/la patiente est présent.e ?")
    st.caption("Fait d'être là ; d'être disponible à la sollicitation, à la relation")


    presence = st.slider(
        label="Déplacer le curseur sur l'échelle pour indiquer l'intensité de PRÉSENCE du patient",
        min_value=-1.0,
        max_value=1.0,
        key="presence"
    )
    pre1, pre2, pre3 = st.columns([1,6,1])
    with pre1 :
        st.caption("ABSENT")
    with pre3 :
        st.caption("PRÉSENT")

    st.divider()
    #----------------------------


    st.subheader("Selon vous, à quel point le/la patiente est éveillé.e ?")
    st.caption("Se reférant aux différents niveaux d'éveil : du sommeil profond au total éveil")

    eveil = st.slider(
        label="Déplacer le curseur sur l'échelle pour indiquer l'intensité d'ÉVEIL du patient", 
        min_value=-1.0,
        max_value=1.0,
        key="eveil"
    )

    ev1, ev2, ev3 = st.columns([1,6,1])
    with ev1 :
        st.caption("ENDORMI")
    with ev3 :
        st.caption("ÉVEILLÉ")

#-----------------------------------------------------------------------

with col3 :
    st.subheader("Selon vous, le/la patiente est conscient.e ?")

    conscient = st.radio(
        "Conscient.e ? (choisir l'option qui vous semble la plus appropriée)",
        ["OUI", "NON"], 
        horizontal=True,
        key="conscient"
    )
    st.divider()
    #----------------------------

    st.subheader("Avez-vous observé un changement chez le/la patiente suite à votre visite ?")

    changement = st.radio(
        "Changement ? (choisir l'option qui vous semble la plus appropriée)", 
        ["OUI", "NON"], 
        horizontal=True,
        key="changement"
    )

    st.divider()

    commentaire = st.text_input( 
            label="Commentaire (optionnel)", 
            key="commentaire"
        )
     
    st.divider()
    #-----------------------------------------------------------------------

    # Vérifier si tous les champs sont remplis
    all_filled = hour and minutes and matricule.strip() and evaluator and conscient and changement

    # Button to validate and save
    if st.button("Valider", disabled=not all_filled or st.session_state.running, key='run_button'):

        new_data = {
            "date": datetime.today().date(),
            "heure": f"{hour}:{minutes}",
            "matricule": matricule,
            "evaluateur": evaluator,
            "presence": presence,
            "eveil": eveil,
            "conscient": conscient,
            "changement": changement,
            "commentaire" : commentaire,
            "temps_validation" : datetime.today()
        }
        
        # Check if the Excel file exists or create a new one
        
        try:
            # Try to load the existing Excel file
            df = pd.read_excel(file_path)
        except FileNotFoundError:
            # If the file doesn't exist, create a new one with the headers
            df = pd.DataFrame(columns=new_data.keys())

        # Use pd.concat to append the new data
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)

        # Save the updated Excel file
        df.to_excel(file_path, index=False)

        # Inform the user that the data has been saved
        st.success("""
            Les données ont été enregistrées avec succès. 
            Merci pour votre participation !       
                   """, icon="✅")
        
        # Wait for 2 seconds
        time.sleep(2)

        for key in st.session_state.keys():
            del st.session_state[key]

        st.rerun()

