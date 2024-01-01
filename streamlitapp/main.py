import streamlit as st
import qrcode
from PIL import Image
import io


from qrcode.image.styledpil import StyledPilImage
# from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer
# , CircleModuleDrawer, RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer, SquareModuleDrawer
# ^mistake in lib\

# from qrcode.image.styles.moduledrawers.pil.py import GappedSquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer, SquareModuleDrawer

import qrcode.image.styles.moduledrawers.pil as md
# qrcode/image/styles/moduledrawers/pil.py

from qrcode.image.styles.colormasks import RadialGradiantColorMask



def generate_qr_code(data, error_correction='L', box_size=10, border=4,dotStyle='Square'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{error_correction.upper()}"),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    if   dotStyle=='Sqaure with gaps':
        pil_image = qr.make_image(image_factory=StyledPilImage, module_drawer= md.GappedSquareModuleDrawer())
    elif dotStyle=='Dots':
        pil_image = qr.make_image(image_factory=StyledPilImage, module_drawer= CircleModuleDrawer())
    elif dotStyle=='Rounded Square':
        pil_image = qr.make_image(image_factory=StyledPilImage, module_drawer= RoundedModuleDrawer())
    elif dotStyle=='Vertical Bars':
        pil_image = qr.make_image(image_factory=StyledPilImage, module_drawer= VerticalBarsDrawer())
    elif dotStyle=='Horizontal Bars':
        pil_image = qr.make_image(image_factory=StyledPilImage, module_drawer= HorizontalBarsDrawer())
    elif dotStyle=='Square':
        pil_image = qr.make_image(image_factory=StyledPilImage, module_drawer= SquareModuleDrawer())
    else:
        pil_image = qr.make_image(fill_color="black", back_color="white")

        #('Style:', ['Square', 'Sqaure with gaps', 'Dots', 'Rounded Square', 'Vertical Bars', 'Horizontal Bars'], index=0)
            # SquareModuleDrawer
            # GappedSquareModuleDrawer
            # CircleModuleDrawer
            # RoundedModuleDrawer
            # VerticalBarsDrawer
            # HorizontalBarsDrawer


# img_1 = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
# img_2 = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask())
    return pil_image

def main():
    st.title('nuQtaR - a nuqta-sytled QR Code Generator')

    # User input
    data = st.text_input('Enter data to encode in QR code:', 'Some data')

    with st.expander('Styling Options'):
        dotStyle = st.selectbox('Style:', ['Square', 'Sqaure with gaps', 'Dots', 'Rounded Square', 'Vertical Bars', 'Horizontal Bars'], index=0)
            # SquareModuleDrawer
            # GappedSquareModuleDrawer
            # CircleModuleDrawer
            # RoundedModuleDrawer
            # VerticalBarsDrawer
            # HorizontalBarsDrawer
    # Additional options (in an expandable box)
    with st.expander('Additional Options'):
        error_correction = st.selectbox('Error Correction Level:', ['L', 'M', 'Q', 'H'], index=0)
        box_size = st.slider('Box Size:', min_value=1, max_value=50, value=10)
        border = st.slider('Border Size:', min_value=1, max_value=10, value=4)

    # Generate QR code
    if st.button('Generate QR Code'):
        qr_code_img = generate_qr_code(data, error_correction, box_size, border,dotStyle)
        
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
