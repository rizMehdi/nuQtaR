import streamlit as st
import qrcode
from PIL import Image
import io
import mods #for custom modifications to default streamlit app style

from qrcode.image.styledpil import StyledPilImage
# from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer
# , CircleModuleDrawer, RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer, SquareModuleDrawer
# ^mistake in lib\

from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer, SquareModuleDrawer
from qrcode.image.styles.moduledrawers.pil import RhombusModuleDrawer

# import qrcode.image.styles.moduledrawers #.pil.GappedSquareModuleDrawer 
# qrcode/image/styles/moduledrawers/pil.py

from qrcode.image.styles.colormasks import RadialGradiantColorMask


def generate_qr_code(data, error_correction='L', box_size=30, border=4,dotStyle='Nuqta (Rhombus)'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{error_correction.upper()}"),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    if   dotStyle=='Sqaure with gaps':
        pil_image = qr.make_image(image_factory=StyledPilImage, module_drawer= GappedSquareModuleDrawer())
    elif dotStyle=='Dots':
        pil_image = qr.make_image(image_factory=StyledPilImage, module_drawer= CircleModuleDrawer())
    elif dotStyle=='Nuqta (Rhombus)':
        pil_image = qr.make_image(image_factory=StyledPilImage, module_drawer= RhombusModuleDrawer())
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

    return pil_image

def main():

    #################################################################################à
    #apply custom modifications to default streamlit app style
    # st.set_page_config(page_title="nuQtaR",page_icon=None,layout="wide",initial_sidebar_state="expanded")
    st.set_page_config(page_title="nuQtaR",page_icon=None)
    st.markdown(mods.hide_menu_style, unsafe_allow_html=True)
    st.markdown(mods.hide_img_fs, unsafe_allow_html=True)
    # st.markdown(mods.fix_sidebar,unsafe_allow_html=True)
    st.markdown(mods.fix_tabs, unsafe_allow_html=True)
    st.markdown(mods.hide_top_padding, unsafe_allow_html=True)

    ########################### main app ########################################à
    st.title('nuQtaR - a nuqta-sytled QR Code Generator')
    # User input
    data = st.text_input('Enter text or URL to encode in QR code:', 'your text or URL')
    error_correction='H'

    
    with st.expander('+ Additional Settings'):
        dotStyle = st.selectbox('Style:', ['Nuqta (Rhombus)', 'Square', 'Dots', 'Sqaure with gaps',  'Rounded Square', 'Vertical Bars', 'Horizontal Bars'], index=0)
        # error_correction = st.selectbox('Error Correction Level:', ['L', 'M', 'Q', 'H'], index=0)
        box_size = st.slider('QR Code Size:', min_value=1, max_value=50, value=30)
        border = st.slider('Border around QR code:', min_value=1, max_value=10, value=4)
    
 
    

    # Generate QR code
    if st.button('Generate QR Code'):
        qr_code_img = generate_qr_code(data, error_correction, box_size, border,dotStyle)
        
        # Convert PIL Image to bytes
        img_byte_array = io.BytesIO()
        qr_code_img.save(img_byte_array, format='PNG')
        
        image_col, padding1 = st.columns([1,1])
        with image_col:    
        # Display the generated QR code
            st.image(img_byte_array, caption='QR Code for: '+data, use_column_width=True)

            # Download button
        st.download_button(
            label='Download QR Code',
            data=img_byte_array.getvalue(),
            file_name='generated_qr_code.png',
            mime='image/png',
        )
    st.markdown("""---""")
    badge="""
    [![Mehdi Rizvi](https://img.shields.io/badge/Author-@rizMehdi-grey.svg?colorA=gray&colorB=dodgerblue&logo=github)](https://github.com/rizMehdi/)
    """
    st.markdown(badge,  unsafe_allow_html=False)

if __name__ == '__main__':
    main()
