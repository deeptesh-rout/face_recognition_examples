import face_recognition
import os
import logging
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_face_encoding(image_path):
    """
    Loads an image file and returns the face encoding.
    Handles errors if the image or encoding is invalid.
    """
    try:
        # Load image
        image = face_recognition.load_image_file(image_path)
        # Extract face encodings
        encodings = face_recognition.face_encodings(image)
        
        if len(encodings) == 0:
            logging.warning(f"No faces found in {image_path}.")
            return None
        elif len(encodings) > 1:
            logging.warning(f"Multiple faces found in {image_path}. Using the first one.")
        return encodings[0]  # Return the first face encoding
    except FileNotFoundError:
        logging.error(f"Error: File not found - {image_path}")
        return None
    except Exception as e:
        logging.error(f"An error occurred while processing {image_path}: {e}")
        return None

def resize_image(image_path, max_size=(400, 400)):
    """
    Resizes image to a maximum size (keeping aspect ratio).
    """
    try:
        img = Image.open(image_path)
        img.thumbnail(max_size)
        img.save(image_path)  # You can save it in a different file if you prefer
        logging.info(f"Image resized to: {max_size}")
    except Exception as e:
        logging.error(f"Error resizing image {image_path}: {e}")

def compare_faces(known_image_path, unknown_image_path):
    """
    Compares a known image with an unknown image and prints the result.
    """
    logging.info("Loading known image...")
    known_face_encoding = load_face_encoding(known_image_path)
    if not known_face_encoding:
        return

    logging.info("Loading unknown image...")
    unknown_face_encoding = load_face_encoding(unknown_image_path)
    if not unknown_face_encoding:
        return

    # Compare faces
    logging.info("Comparing faces...")
    results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)
    if results[0]:
        logging.info(f"The person in the unknown image matches the known person: {os.path.basename(known_image_path)}")
    else:
        logging.info("The person in the unknown image does NOT match the known person.")

# Paths to images (adjust paths as needed)
known_image_path = './img/known/Bill Gates.jpg'
unknown_image_path = './img/unknown/d-trump.jpg'

# Optionally, resize images for faster processing
resize_image(known_image_path)
resize_image(unknown_image_path)

# Run comparison
compare_faces(known_image_path, unknown_image_path)
