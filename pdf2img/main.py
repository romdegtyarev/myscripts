from PIL import Image
from pdf2image import convert_from_path
import os
import sys

def convert_save_image(pdf_path, page_number, image_name):
    """
    Converts a specific page of a PDF to an image
    :param pdf_path: Path to the input PDF file
    :param page_number: Page number to convert (starting from 0)
    :param image_name: Name of the output image file
    """
    try:
        # Convert PDF to a list of images
        images = convert_from_path(pdf_path, dpi=300)

        # Check if the page exists
        if page_number < len(images):
            # Define the full path to save the image
            image_path = os.path.join(image_name + '.jpg')

            # Save the specified page
            images[page_number].save(image_path, 'JPEG')
            print(f"convert_save_image: Page {page_number + 1} successfully saved as {image_name}.jpg")
        else:
            print(f"convert_save_image: Page {page_number + 1} does not exist in the document")

    except Exception as e:
        print(f"convert_save_image: Error during conversion: {str(e)}")

if __name__ == "__main__":
    try:
        if len(sys.argv) != 4:
            print("Usage: python script.py </path/to/pdf.pdf> <page number> <image name>")
            sys.exit(1)

        pdf_path = sys.argv[1]
        page_number = int(sys.argv[2])
        image_name = sys.argv[3]
        convert_save_image(pdf_path, page_number, image_name)

    except Exception as e:
        print(f"An error occurred: {str(e)}")