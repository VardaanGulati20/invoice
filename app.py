from dotenv import load_dotenv
load_dotenv()  
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai
import os
os.environ['GOOGLE_API_KEY']="AIzaSyAmqVV8kQwqmlbW0RxZXq7-yikv93UHcUU"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
## Function to load OpenAI model and get respones
def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,image[0],prompt])
    return response.text
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title="Gemini Image Demo")
st.header("Invoice Analyser")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("invoice1.jpg", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
submit=st.button("Tell me about the image")
input_prompt = """
               You are an expert in understanding invoices.
               If you do not get any relevant information kindly say not could not find relevant answer do not put in anything random,
               We will upload an image as invoice and you will have to answer the question based on the given invoice 
               And in some cases are capable of finding the days difference too when applicable
               
               """

## If ask button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)
