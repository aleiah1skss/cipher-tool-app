import streamlit as st
import string

# --- CORE CIPHER LOGIC (Keep these functions unchanged) ---

def caesar_cipher(text, shift, mode):
    result = ""
    shift = -shift if mode == 'decrypt' else shift

    for char in text:
        if 'a' <= char <= 'z':
            start_char_ascii = ord('a')
        elif 'A' <= char <= 'Z':
            start_char_ascii = ord('A')
        else:
            result += char
            continue

        old_position = ord(char) - start_char_ascii
        new_position = (old_position + shift + 26) % 26
        
        new_char_ascii = start_char_ascii + new_position
        result += chr(new_char_ascii)

    return result

def vigenere_cipher(text, key, mode):
    result = ""
    key = key.upper()
    key_index = 0
    key_length = len(key)

    for char in text:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
            
            # Get the shift value for the current character
            shift = ord(key[key_index % key_length]) - ord('A')
            
            # Adjust shift for decryption
            if mode == 'decrypt':
                shift = -shift
            
            start_char_ascii = ord('a') if 'a' <= char <= 'z' else ord('A')
            
            # Apply Vigenère Shift
            old_position = ord(char) - start_char_ascii
            new_position = (old_position + shift + 26) % 26
            
            new_char_ascii = start_char_ascii + new_position
            result += chr(new_char_ascii)

            # ADVANCE THE KEY INDEX ONLY FOR LETTERS
            key_index += 1
            
        else:
            # Keep non-alphabetic characters as they are, DO NOT ADVANCE KEY INDEX
            result += char

    return result

# --- STREAMLIT WEB APP INTERFACE ---

# Set up the title and layout
st.set_page_config(
    page_title="Advanced Cipher Tool",
    layout="centered"
)

st.title("Advanced Cipher Tool 🔒")
st.markdown("##### SkillCraft Technology Internship Project")

# 1. CIPHER SELECTION
cipher_type = st.radio(
    "Select Cipher Type:",
    ("Caesar", "Vigenère"),
    horizontal=True
)

# 2. MESSAGE INPUT
message = st.text_input("Message:")

# 3. OPERATION MODE
mode = st.radio(
    "Operation:",
    ("Encrypt", "Decrypt"),
    horizontal=True
).lower() # Convert to 'encrypt' or 'decrypt'

# --- KEY INPUTS (Conditional based on Cipher Type) ---

# CAESAR KEY INPUT
if cipher_type == "Caesar":
    st.markdown("---")
    shift_value = st.number_input("Caesar Shift Value:", min_value=1, value=3, step=1)
    # Ensure shift is an integer for the function call
    key_input = int(shift_value)

# VIGENÈRE KEY INPUT
elif cipher_type == "Vigenère":
    st.markdown("---")
    key_word = st.text_input("Vigenère Key Word:", value="LEMON")
    # Validation: Ensure key is alphabetic
    if not key_word.isalpha():
        st.error("Vigenère Key must be an alphabetic word.")
        st.stop() # Stop execution if key is invalid
    key_input = key_word


# --- PROCESSING BUTTON ---
if st.button("Process Cipher"):
    if not message:
        st.warning("Please enter a message to process.")
    else:
        # Determine which function to call
        if cipher_type == "Caesar":
            processed_text = caesar_cipher(message, key_input, mode)
        elif cipher_type == "Vigenère":
            processed_text = vigenere_cipher(message, key_input, mode)
        
        st.success(f"Operation: {mode.capitalize()} with {cipher_type}")
        st.code(processed_text) # Display result in a clean code block