#importing required libraries
import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

SUPPORTED_FORMATS = ["jpg", "jpeg", "png"]#supported image formats as input

#various types of tranformations and filters
def apply_grayscale(img): #grayscale image
    return ImageOps.grayscale(img)

def apply_flip(img): #flip image
    return ImageOps.flip(img)

def apply_blur(img): #apply gaussian blur to image
    return img.filter(ImageFilter.GaussianBlur(radius=2))

def apply_edges(img): #edge detection of image
    return img.filter(ImageFilter.FIND_EDGES)

def apply_brightness(img): #increase brightness of image
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(5.0)

def apply_crop(img): #crop image
    return img.crop((50, 40, 200, 300))

def apply_resize(img):
    return img.resize((300, 300))

def apply_rotate(img): #rotate image
    return img.rotate(45, expand=True)

#validation of image
#checks if the image is supported or not
def is_supported_format(filename):
    extension = filename.split(".")[-1].lower()
    return extension in SUPPORTED_FORMATS

#applying different transformations to the image
def apply_transformations(img, transformations):
    for transformation in transformations:
        if transformation == "Grayscale":
            img = apply_grayscale(img)
        elif transformation == "Flip":
            img = apply_flip(img)
        elif transformation == "Gaussian Blur":
            img = apply_blur(img)
        elif transformation == "Find Edges":
            img = apply_edges(img)
        elif transformation == "Brightness":
            img = apply_brightness(img)
        elif transformation == "Crop":
            img = apply_crop(img)
        elif transformation == "Resize":
            img = apply_resize(img)
        elif transformation == "Rotate":
            img = apply_rotate(img)
    return img

def main():
    st.set_page_config(page_title="Image Processing Application", layout="wide")
    st.title("Image Processing Application")
    st.write("---")

    uploaded_file = st.file_uploader("Upload an image", type=SUPPORTED_FORMATS)

    #for error handling try except are used
    if uploaded_file is not None:
        try:
            filename = uploaded_file.name
            if is_supported_format(filename):
                img = Image.open(uploaded_file)
                st.image(img, caption="Uploaded Image", use_column_width=True)
                st.write("---")
                
                #for selecting multiple tranformations to be applied to the image
                selected_transformations = st.multiselect("Select Transformations", [
                    "Grayscale", "Flip", "Gaussian Blur", "Find Edges", "Brightness", "Crop", "Resize", "Rotate"
                ])

                if st.button("Apply", key="apply_button"):
                    with st.spinner("Applying transformations..."):
                        transformed_img = apply_transformations(img, selected_transformations)
                        st.image(transformed_img, caption="Transformed Image", use_column_width=True)
                        st.success("Transformations applied successfully!")
            else:
                st.error("Invalid image format. Please upload a JPEG, JPG, or PNG image.")
        except Exception as e:
            st.error(f"Error opening the image: {e}")

if __name__ == "__main__":
    main()