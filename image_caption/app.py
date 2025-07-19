# import streamlit as st
# import google.generativeai as genai 
# from PIL import Image

# # Configure Gemini API key
# genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# # Load the Gemini model
# model = genai.GenerativeModel("gemini-2.0-flash")

# # Define function to generate response
# def get_gemini_response(image): 
#     # Define a fixed prompt template to generate captions for the uploaded image
#     prompt = "Generate a single, detailed caption or description for the following image, in a natural and coherent paragraph format:"
#     response = model.generate_content([prompt, image]) 
#     return response.text

# # Initialize the Streamlit app
# st.set_page_config(page_title="Image Description")
# st.header("Image Description Generator for Assisting Visually Impaired Individual")

# # File uploader for image input
# uploaded_file = st.file_uploader("Choose any file :) ", type=["jpg", "jpeg", "png"])
# image = ""

# # Logic to display the uploaded image
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Image Uploaded.", use_column_width=True)

# # Button to generate caption
# submit = st.button("Generate Caption about image")

# # If button clicked
# if submit and image:
#     response = get_gemini_response(image)
#     # Display the generated caption
#     st.subheader("Generated Caption is")
#     st.write(response)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------- working without audio
# import streamlit as st
# import google.generativeai as genai 
# from PIL import Image

# # ✅ Must come first
# st.set_page_config(page_title="Image Description Generator", layout="centered")

# # Gemini API config
# genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# model = genai.GenerativeModel("gemini-2.0-flash")

# # 🎨 Custom Styling
# st.markdown("""
#     <style>
#         .stApp {
#             background-color: #f1f5f9;
#             font-family: 'Segoe UI', sans-serif;
#         }
#         h1 {
#             text-align: center;
#             color: #1e293b;
#             font-size: 2.5rem;
#             margin-bottom: 1.5rem;
#         }
#         .stButton > button {
#             background-color: #1e293b;
#             color: white;
#             padding: 0.6rem 1.5rem;
#             border: none;
#             border-radius: 8px;
#             font-size: 1rem;
#             font-weight: 500;
#             margin-top: 1rem;
#             transition: 0.3s ease;
#         }
#         .stButton > button:hover {
#             background-color: #1e293b;
#         }
#         .stFileUploader {
#             background-color: white;
#             border: 1px solid #cbd5e1;
#             border-radius: 10px;
#             padding: 1rem;
#             margin-bottom: 1rem;
#         }
#         .caption-box {
#         background: rgba(255, 255, 255, 0.7);
#         padding: 1.2rem;
#         border-radius: 15px;
#         margin-top: 1.5rem;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Header
# st.markdown("<h1>Image Caption Generator</h1>", unsafe_allow_html=True)


# uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
# image = ""

# # Function to call Gemini
# # def get_gemini_response(image): 
# #     prompt = "Generate a single, detailed caption or description for the following image, in a natural and coherent paragraph format:"
# #     response = model.generate_content([prompt, image]) 
# #     return response.text

# # Function to call Gemini
# def get_gemini_response(image): 
#     prompt = "Generate a short, one-line caption for the image that briefly describes its content."
#     response = model.generate_content([prompt, image]) 
#     return response.text


# # Preview + Caption
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image", use_column_width=True)

# # 🔍 Button
# if st.button("Generate Caption"):
#     if image:
#         with st.spinner("Generating caption..."):
#             response = get_gemini_response(image)
#         # st.subheader("Generated Caption:")
#         # st.write(response)
#         st.markdown(
#     "<h1>Generated Caption:</h1>",
#     unsafe_allow_html=True
# )
#         st.markdown(f"""
# <div style="background-color: #1e1e1e; padding: 1rem; border-radius: 10px;">
#     {response}
# </div>
# """, unsafe_allow_html=True)


#     else:
#         st.warning("Please upload an image first.")
# ----------------------------------------------------------------------------------------------------------------------------------------------------working with audio------------------------------------------------

import streamlit as st
import google.generativeai as genai 
from PIL import Image
from gtts import gTTS
import os

# Page Config
st.set_page_config(page_title="Image Caption Generator", layout="centered")

# Gemini API config
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

# 🎨 Custom CSS Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #f1f5f9;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            text-align: center;
            color: #1e293b;
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
        }
        .stButton > button {
            background-color: #1e293b;
            color: white;
            padding: 0.6rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 500;
            margin-top: 1rem;
            transition: 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #0f172a;
        }
        .stFileUploader {
            background-color: white;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .caption-box {
            background: rgba(30, 41, 59, 0.9);
            padding: 1rem;
            border-radius: 12px;
            color: white;
            font-size: 1.1rem;
            margin-top: 1rem;
            text-align: center;
        }
        .audio-wrapper {
            
            padding: 1rem;
            justify-content: center;
        }
        audio {
            width: 100%;
            max-width: 500px;
            outline: none;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>Image Caption Generator</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
image = ""

# Function to call Gemini
def get_gemini_response(image): 
    prompt = "Generate a short, one-line caption for the image that briefly describes its content."
    response = model.generate_content([prompt, image]) 
    return response.text

# Preview image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# # Button
# if st.button("Generate Caption"):
#     if image:
#         with st.spinner("Generating caption..."):
#             response = get_gemini_response(image)

#         st.markdown("<div class='caption-box'>" + response + "</div>", unsafe_allow_html=True)

#         # Generate audio
#         tts = gTTS(text=response)
#         audio_path = "caption_audio.mp3"
#         tts.save(audio_path)

#         # Display audio player
#         st.markdown("<div class='audio-wrapper'>", unsafe_allow_html=True)
#         st.audio(audio_path, format="audio/mp3")
#         st.markdown("</div>", unsafe_allow_html=True)

#     else:
#         st.warning("Please upload an image first.")
        
# # Show regenerate button only after the first caption is generated
# if st.session_state.get('caption_generated', False):
#     if st.button("Generate Another Caption"):
#         if image:
#             with st.spinner("Generating another caption..."):
#                 response = get_gemini_response(image)

#             st.markdown("<div class='caption-box'>" + response + "</div>", unsafe_allow_html=True)

#             tts = gTTS(text=response)
#             audio_path = "caption_audio.mp3"
#             tts.save(audio_path)

#             st.markdown("<div class='audio-wrapper'>", unsafe_allow_html=True)
#             st.audio(audio_path, format="audio/mp3")
#             st.markdown("</div>", unsafe_allow_html=True)
#         else:
#             st.warning("Please upload an image first.")

# Button
if st.button("Generate Caption"):
    if image:
        with st.spinner("Generating caption..."):
            response = get_gemini_response(image)

        st.markdown("<div class='caption-box'>" + response + "</div>", unsafe_allow_html=True)

        # Generate audio
        tts = gTTS(text=response)
        audio_path = "caption_audio.mp3"
        tts.save(audio_path)

        # Display audio player
        st.markdown("<div class='audio-wrapper'>", unsafe_allow_html=True)
        st.audio(audio_path, format="audio/mp3")
        st.markdown("</div>", unsafe_allow_html=True)

        # ✅ Set session flag to show "Generate Another Caption" button
        st.session_state.caption_generated = True

    else:
        st.warning("Please upload an image first.")

# Show regenerate button only after the first caption is generated
if st.session_state.get('caption_generated', False):
    if st.button("Generate Another Caption"):
        if image:
            with st.spinner("Generating another caption..."):
                response = get_gemini_response(image)

            st.markdown("<div class='caption-box'>" + response + "</div>", unsafe_allow_html=True)

            tts = gTTS(text=response)
            audio_path = "caption_audio.mp3"
            tts.save(audio_path)

            st.markdown("<div class='audio-wrapper'>", unsafe_allow_html=True)
            st.audio(audio_path, format="audio/mp3")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Please upload an image first.")

