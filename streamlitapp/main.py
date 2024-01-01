import streamlit as st
import qrcode
from PIL import Image
import io

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    pil_image = qr.make_image(fill_color="black", back_color="white")
    return pil_image

def main():
    st.title('QR Code Generator')

    # User input
    data = st.text_input('Enter data to encode in QR code:', 'Some data')

    # Generate QR code
    if st.button('Generate QR Code'):
        qr_code_img = generate_qr_code(data)

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
