import face_recognition
import os

def load_face_encoding(image_path):
    """
    Loads an image file and returns the face encoding. 
    Handles errors if the image or encoding is invalid.
    """
    try:
        # Load image
        image = face_recognition.load_image_file(image_path)
        # Extract face encoding
        encodings = face_recognition.face_encodings(image)
        if len(encodings) == 0:
            print(f"No faces found in {image_path}.")
            return None
        return encodings[0]
    except FileNotFoundError:
        print(f"Error: File not found - {image_path}")
        return None
    except Exception as e:
        print(f"An error occurred while processing {image_path}: {e}")
        return None

def compare_faces(known_image_path, unknown_image_path):
    """
    Compares a known image with an unknown image and prints the result.
    """
    print("Loading known image...")
    known_face_encoding = load_face_encoding(known_image_path)
    if not known_face_encoding:
        return

    print("Loading unknown image...")
    unknown_face_encoding = load_face_encoding(unknown_image_path)
    if not unknown_face_encoding:
        return

    # Compare faces
    print("Comparing faces...")
    results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)
    if results[0]:
        print(f"The person in the unknown image matches the known person: {os.path.basename(known_image_path)}")
    else:
        print("The person in the unknown image does NOT match the known person.")

# Paths to images (adjust paths as needed)
known_image_path = './img/known/Bill Gates.jpg'
unknown_image_path = './img/unknown/d-trump.jpg'

# Run comparison
compare_faces(known_image_path, unknown_image_path)
