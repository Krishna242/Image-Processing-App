#importing required libraries
import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

SUPPORTED_FORMATS = ["jpg", "jpeg", "png"] #supported image formats as input

#various types of tranformations and filters
def apply_grayscale(img): #grayscale image
    return ImageOps.grayscale(img)

def apply_flip(img): #flip image
    return ImageOps.flip(img)

def apply_edges(img): #edge detection of image
    return img.filter(ImageFilter.FIND_EDGES)

def apply_brightness(img, brightness): #adjust brightness of image
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(brightness)

def apply_blur(img, blur_radius): #apply gaussian blur to image
    return img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

def apply_crop(img, crop_box): #crop image
    return img.crop(crop_box)

def apply_resize(img, width, height): #resize image
    return img.resize((width, height))

def apply_rotate(img, rotation_angle): #rotate image
    return img.rotate(rotation_angle, expand=True)

#validation of image
#checks if the image is supported or not
def is_supported_format(filename):
    extension = filename.split(".")[-1].lower()
    return extension in SUPPORTED_FORMATS

def main():
    #user interface 
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
                    "Grayscale", "Flip", "Edge Detection", "Brightness", "Blur", "Crop", "Resize", "Rotate"
                ])

                #if user wants to adjust brightness
                if "Brightness" in selected_transformations:
                    brightness = st.slider("Brightness", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
                else:
                    brightness = 1.0

                #if user wants to adjust blur
                if "Blur" in selected_transformations:
                    blur_radius = st.slider("Blur Radius", min_value=0, max_value=10, value=2)
                else:
                    blur_radius = 0

                #if user wants to crop according to his needs
                if "Crop" in selected_transformations:
                    crop_x1 = st.number_input("Crop X1", value=0, step=1)
                    crop_y1 = st.number_input("Crop Y1", value=0, step=1)
                    crop_x2 = st.number_input("Crop X2", value=img.width, step=1)
                    crop_y2 = st.number_input("Crop Y2", value=img.height, step=1)
                    crop_box = (crop_x1, crop_y1, crop_x2, crop_y2)
                else:
                    crop_box = (0, 0, img.width, img.height)

                #if user wants to resize according to his needs
                if "Resize" in selected_transformations:
                    resize_width = st.number_input("Resize Width", value=img.width, step=1)
                    resize_height = st.number_input("Resize Height", value=img.height, step=1)
                else:
                    resize_width = img.width
                    resize_height = img.height

                #if user wants to rotate according to his needs
                if "Rotate" in selected_transformations:
                    rotation_angle = st.slider("Rotation Angle", min_value=0, max_value=360, value=0, step=1)
                else:
                    rotation_angle = 0

                #applying different transformations to the image
                if st.button("Apply", key="apply_button"):
                    with st.spinner("Applying transformations..."):
                        transformed_img = img.copy()
                        if "Grayscale" in selected_transformations:
                            transformed_img = apply_grayscale(transformed_img)
                        if "Flip" in selected_transformations:
                            transformed_img = apply_flip(transformed_img)
                        if "Edge Detection" in selected_transformations:
                            transformed_img = apply_edges(transformed_img)
                        if "Brightness" in selected_transformations:
                            transformed_img = apply_brightness(transformed_img, brightness)
                        if "Blur" in selected_transformations:
                            transformed_img = apply_blur(transformed_img, blur_radius)
                        if "Crop" in selected_transformations:
                            transformed_img = apply_crop(transformed_img, crop_box)
                        if "Resize" in selected_transformations:
                            transformed_img = apply_resize(transformed_img, resize_width, resize_height)
                        if "Rotate" in selected_transformations:
                            transformed_img = apply_rotate(transformed_img, rotation_angle)

                        st.image(transformed_img, caption="Transformed Image", use_column_width=True)
                        st.success("Transformations applied successfully!")
            else:
                #if user inputs wrong image format 
                st.error("Invalid image format. Please upload a JPEG, JPG, or PNG image.")
        except Exception as e:
            st.error(f"Error opening the image: {e}")

if __name__ == "__main__":
    main()