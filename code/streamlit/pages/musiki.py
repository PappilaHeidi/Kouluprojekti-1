import streamlit as st

# Define file paths (replace with actual paths)
gif_path = 'gigachad.gif'
audio_path = 'BMTH_CYFMH.mp3'

# Function to load GIFs efficiently (using `st.cache_data`)
@st.cache_data
def load_gif(path):
    with open(path, 'rb') as f:
        return f.read()

# Function to load audio (using `st.cache_data`)
@st.cache_data
def load_audio(path):
    with open(path, 'rb') as f:
        return f.read()

# Start button
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

if not st.session_state.button_clicked:
    button_clicked = st.button('Enable GIGAMODE')
    
    if button_clicked:
        audio_data = load_audio(audio_path)
        gif_data = load_gif(gif_path)

        # Display GIF and start audio playback
        st.image(gif_data, caption='GIGAMODE ACTIVATED', use_column_width=True)
        st.audio(audio_data, format='audio/mp3', start_time=0)

        # Hide "Enable GIGAMODE" button
        st.session_state.button_clicked = True
        st.empty()

# Show Reset button
if st.session_state.button_clicked:
    if st.button('Back to PLEBMODE...'):
        st.session_state.button_clicked = False
        st.rerun()

# Aloitus nappulassa bugi, se ei poistu vaikka sen pitäisi
# Ääni ei käynnisty painaessa "Enable GIGAMODE" -nappulaa
