import streamlit as st
import qrcode
from PIL import Image
import io

def generate_qr_code(data, error_correction='L', box_size=10, border=4):
    qr = qrcode.QRCode(
        version=1,
        error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{error_correction.upper()}"),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    pil_image = qr.make_image(fill_color="black", back_color="white")
    return pil_image

def main():
    st.title('nuQtaR - a nuqta-sytled QR Code Generator')

    # User input
    data = st.text_input('Enter data to encode in QR code:', 'Some data')

    # Additional options (in an expandable box)
    with st.expander('Additional Options'):
        error_correction = st.selectbox('Error Correction Level:', ['L', 'M', 'Q', 'H'], index=0)
        box_size = st.slider('Box Size:', min_value=1, max_value=50, value=10)
        border = st.slider('Border Size:', min_value=1, max_value=10, value=4)

    # Generate QR code
    if st.button('Generate QR Code'):
        qr_code_img = generate_qr_code(data, error_correction, box_size, border)
        
        # Convert PIL Image to bytes
        img_byte_array = io.BytesIO()
        qr_code_img.save(img_byte_array, format='PNG')
        
        # Display the generated QR code
        st.image(img_byte_array, caption='Generated QR Code', use_column_width=True)

            # Download button
        st.download_button(
            label='Download QR Code',
            data=img_byte_array.getvalue(),
            file_name='generated_qr_code.png',
            mime='image/png',
        )
if __name__ == '__main__':
    main()
