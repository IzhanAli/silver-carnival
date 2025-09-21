import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Set page config
st.set_page_config(
    page_title="LSA Hack-a-Mini Certificate Generator",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 20px;
    }
    .stSelectbox {
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("LSA Hack-a-Mini Certificate Generator")

def load_names():
    with open("names.txt", "r") as f:
        names = [line.strip() for line in f.readlines() if line.strip()]
    return names

def generate_certificate(name):
    # Open the certificate template
    template_path = "LSA Hack-a-Mini Certificate Sept 21 2025.png"
    img = Image.open(template_path)
    
    # Create a drawing object
    draw = ImageDraw.Draw(img)
    
    # Load Times New Roman from local fonts directory
    try:
        font = ImageFont.truetype("./fonts/Times New Roman.ttf", 60)
    except IOError:
        st.error("Times New Roman font not found in ./fonts directory")
        raise
    
    # Calculate text size and position
    text_width = draw.textlength(name, font=font)
    # Position the text in the center horizontally
    x = (img.width - text_width) / 2
    # Position the text on the blank line above "has successfully participated"
    # Based on the image, this appears to be around 40% down from the top
    y = img.height * 0.45  # Adjusted based on the certificate layout
    
    # Add the name to the certificate
    draw.text((x, y), name, font=font, fill="black")
    
    return img

def main():
    # Create the dropdown for name selection
    selected_name = st.selectbox(
        "Select a name",
        [""] + load_names(),
        index=0
    )
    
    # Generate certificate button
    if selected_name:
        if st.button("Generate and Download Certificate"):
            # Generate the certificate
            certificate = generate_certificate(selected_name)
            
            # Convert the image to bytes
            buf = io.BytesIO()
            certificate.save(buf, format='PNG')
            byte_im = buf.getvalue()
            
            # Create the download button
            st.download_button(
                label="Download Certificate",
                data=byte_im,
                file_name=f"certificate_{selected_name.replace(' ', '_')}.png",
                mime="image/png"
            )
            
            # Display preview
            st.image(certificate, caption="Certificate Preview", use_column_width=True)
    else:
        st.info("Please select a name to generate a certificate")

if __name__ == "__main__":
    main()
