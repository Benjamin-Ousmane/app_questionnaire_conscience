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
if 'date' not in st.session_state:
    st.session_state.date = datetime.today().date()
if 'hour' not in st.session_state:
    st.session_state.hour = datetime.now().time()
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

# Function to reset the session state
def reset_widgets():
    # reset widget values
    st.session_state.date = datetime.today().date()
    st.session_state.hour = datetime.now().time()
    st.session_state.matricule = ""
    st.session_state.evaluator = None
    st.session_state.presence = 0.0
    st.session_state.eveil = 0.0
    st.session_state.conscient = None
    st.session_state.changement = None
    st.session_state.commentaire = ""

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
    inp1, inp2, inp3= st.columns([1, 1, 1])
    with inp1:
        date = st.date_input(
            label="Date", 
            format="DD/MM/YYYY", 
            key="date"
        )
    with inp2:
        hour = st.time_input(
            label="Heure", 
            step=60, 
            key="hour"
        )
    with inp3:
        matricule = st.text_input( 
            label="Matricule HCL", 
            key="matricule"
        )

    options = [
    "Médecin", 
    "MK", 
    "IDE", 
    "AS",
    "Proche"
    ]

    evaluator = st.radio(
        label="Personne", 
        options=options, 
        horizontal=True, 
        key="evaluator"
    )

    st.divider()

    #----------------------------

    st.subheader("Selon vous, à quel point le/la patiente est présent.e ?")
    st.caption("Fait d'être là ; d'être disponible à la sollicitation, à la relation")


    presence = st.slider(
        label="Indiquez l'intensité de présence sur cette échelle",
        min_value=-1.0,
        max_value=1.0,
        key="presence"
    )
    pre1, pre2, pre3 = st.columns([1,7,1])
    with pre1 :
        st.caption("ABSENT")
    with pre3 :
        st.caption("PRÉSENT")

    st.divider()
    #----------------------------


    st.subheader("Selon vous, à quel point le/la patiente est éveillé.e ?")
    st.caption("Se reférant aux différents niveaux d'éveil : du sommeil profond au total éveil")

    eveil = st.slider(
        label="Indiquez l'intensité d'éveil sur cette échelle", 
        min_value=-1.0,
        max_value=1.0,
        key="eveil"
    )

    ev1, ev2, ev3 = st.columns([1,7,1])
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

    st.info("Assurez-vous d'avoir fermé le fichier Excel '`eval_conscience_data.xlsx`' présent dans le dossier '`C:/Users/(User)/conscience_data/`' avant de cliquer sur le bouton '`Valider`'") 


    # Vérifier si tous les champs sont remplis
    all_filled = date and hour and matricule.strip() and evaluator and conscient and changement

    # Button to validate and save
    if st.button("Valider", disabled=not all_filled):
        # Prepare the data to be saved
        new_data = {
            "date": date,
            "heure": hour,
            "matricule": matricule,
            "evaluateur": evaluator,
            "presence": presence,
            "eveil": eveil,
            "conscient": conscient,
            "changement": changement,
            "commentaire" : commentaire
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
        st.success("Les données ont été enregistrées avec succès dans le fichier Excel ")
        
        # Wait for 5 seconds
        time.sleep(5)

        for key in st.session_state.keys():
            del st.session_state[key]

        reset_widgets()
        st.rerun()

