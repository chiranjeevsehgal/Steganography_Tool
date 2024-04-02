import streamlit as st
from stegano import lsb
import stegano
from PIL import Image
from cryptography.fernet import Fernet


def display_home():
    st.header("Welcome to the Steganography Tool!")
    st.write("""
    This tool allows you to securely hide text within images using steganography techniques.
    Whether you're looking to encode secret messages or decode them, this tool has you covered.
    
    **Features:**
    - **Encoding:**
    - **Decoding**
    - **Encryption**
    
    Get started by selecting either "Encode" or "Decode" from the sidebar menu. For more details, select the About option. Enjoy exploring the capabilities of digital steganography!
    """)

def display_about():
    st.header("About")
    st.write("""
    ### Steganography Tool
    This tool is designed to facilitate secure communication by enabling users to encode and decode hidden messages within images and also encrypt the data using cryptography techniques if needed.
    
    - **Encode:** Hide messages in images with optional encryption for enhanced security.
    - **Decode:** Extract and decrypt messages hidden within images.
    - **Encrypt:** To ensure that only those with the correct key can access the hidden information.


    
    Developed with the aim of privacy and security in digital communication.
    
    **Technologies Used:**
    - Python
    - Streamlit
    - Cryptography for encryption and decryption
    - Stegano library for steganography
    
    Developed by Chiranjeev Sehgal.
    ****
    """)

def encode_text():
    if option == "Encode":
        st.subheader('Encode')

        uploaded_image = st.file_uploader("Choose an image to encode text:", type=["jpg", "png", "jpeg"])
        text_to_hide = st.text_input("Enter the text you want to hide:")
        encrypt_text = st.checkbox("Encrypt text before hiding?")


        if st.button('Hide Text in Image'):
            if uploaded_image is not None and text_to_hide != "":

                # Encryption
                if encrypt_text:
                    # Generate a key for encryption
                    key = generate_key()
                    encrypted_text = encrypt_message(text_to_hide, key)
                    encoded_text = encrypted_text.decode('utf-8')
                    message_to_hide = f"{encoded_text}"
                else:
                    message_to_hide = text_to_hide
                
                image = Image.open(uploaded_image)
                
                # Saving it temporarily to perform operation.
                temp_path = "temp_image.png"
                image.save(temp_path)
                
                secret = lsb.hide(temp_path, message_to_hide)
                
                # Saving the image
                secret_image_path = "secret_image.png"
                secret.save(secret_image_path)
                
                # Showing the image
                st.image(secret_image_path, caption='Image with Hidden Text', use_column_width=True)
                
                # Download link to download the image
                with open(secret_image_path, "rb") as file:
                    st.download_button(label="Download Image with Hidden Text",
                                    data=file,
                                    file_name="secret_image.png",
                                    mime="image/png")
                    
                if encrypt_text:
                    st.success("Text encrypted and hidden in image. Make sure to save the key safely!")
                    st.text_area("Encryption Key (keep this safe!):", key.decode('utf-8'), height=100)

            else:
                st.error("Please upload an image and enter some text to hide.")



def decode_text():
    if option == "Decode":
        st.subheader('Decode')

        uploaded_secret_image = st.file_uploader("Choose an image with hidden text:", type=["jpg", "png", "jpeg"])
        decrypt_text = st.checkbox("Decrypt text after revealing?")

        if decrypt_text:
            key_input = st.text_area("Enter the encryption key:")

        if uploaded_secret_image is not None:
            # Opening the uploaded image
            secret_image = Image.open(uploaded_secret_image)

                
            # To decode and decrypt the info
            try:
                revealed_text = lsb.reveal(secret_image)

                if decrypt_text and key_input:
                    try:
                        key = key_input.encode('utf-8')
                        decrypted_text = decrypt_message(revealed_text.encode('utf-8'), key)
                        st.subheader("Decoded and Decrypted Text:")
                        st.write(decrypted_text)
                    except Exception as e:
                        st.error("Failed to decrypt. Ensure the key is correct.")
                else:
                    st.subheader("Decoded Text:")
                    st.write(revealed_text)

        
            except Exception as e:
                st.error("Failed to decode any text. Ensure the image has hidden text.")

def reset_page():
    st.session_state.page = "Home"  

if 'page' not in st.session_state:
    st.session_state.page = 'home'

st.title('Steganographer Tool')

st.sidebar.markdown('---')


st.sidebar.title('Dashboard Options')

option = st.sidebar.radio("Choose an action:", ("Home", "About","Encode", "Decode"),index=0, on_change=reset_page)

st.sidebar.markdown('---')


def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message


if option == "Home":
    display_home()
elif option == "About": 
    display_about()
elif option == "Encode":
    encode_text()
elif option == "Decode":
    decode_text()
