import streamlit as st
import qrcode

def generate_qr_code(data, error_correction='L', box_size=10, border=4):
    qr = qrcode.QRCode(
        version=1,
        error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{error_correction.upper()}"),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def main():
    st.title('QR Code Generator')

    # User input
    data = st.text_input('Enter data to encode in QR code:', 'Some data')

    # Additional options
    error_correction = st.selectbox('Error Correction Level:', ['L', 'M', 'Q', 'H'], index=0)
    box_size = st.slider('Box Size:', min_value=1, max_value=50, value=10)
    border = st.slider('Border Size:', min_value=1, max_value=10, value=4)

    # Generate QR code
    if st.button('Generate QR Code'):
        qr_code_img = generate_qr_code(data, error_correction, box_size, border)
        st.image(qr_code_img, caption='Generated QR Code', use_column_width=True)

if __name__ == '__main__':
    main()
