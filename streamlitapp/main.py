import streamlit as st
import qrcode
from PIL import Image, ImageDraw
import io

def generate_qr_code(data, error_correction='L', box_size=10, border=4, style=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{error_correction.upper()}"),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    if style:
        qr_code_img = style(qr.make_image(fill_color="black", back_color="white"))
    else:
        qr_code_img = qr.make_image(fill_color="black", back_color="white")
    
    return qr_code_img

def main():
    st.title('QR Code Generator')

    # User input
    data = st.text_input('Enter data to encode in QR code:', 'Some data')

    # Additional options (in an expandable box)
    with st.expander('Additional Options'):
        error_correction = st.selectbox('Error Correction Level:', ['L', 'M', 'Q', 'H'], index=0)
        box_size = st.slider('Box Size:', min_value=1, max_value=50, value=10)
        border = st.slider('Border Size:', min_value=1, max_value=10, value=4)

    # Styling options (in another expandable box)
    with st.expander('Styling Options'):
        # Add styling options here
        style_option = st.selectbox('Choose Style Option:', ['None', 'StyledPilImage', 'SvgSquareDrawer', 'SvgCircleDrawer'], index=0)
        size_ratio = st.slider('Size Ratio:', min_value=0.1, max_value=1.0, value=1.0, step=0.1)

    # Generate QR code
    if st.button('Generate QR Code'):
        if style_option == 'StyledPilImage':
            style = qrcode.image.styles.StyledPilImage
        elif style_option == 'SvgSquareDrawer':
            style = qrcode.image.styles.SvgSquareDrawer(size_ratio=size_ratio)
        elif style_option == 'SvgCircleDrawer':
            style = qrcode.image.styles.SvgCircleDrawer(size_ratio=size_ratio)
        else:
            style = None

        qr_code_img = generate_qr_code(data, error_correction, box_size, border, style)
        
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
