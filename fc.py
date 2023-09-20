import os
import sys
import subprocess
import gradio as gr
import shutil
import cv2
import numpy as np
import insightface
import webbrowser
import logging
import threading
from ifnude import detect

# Function to create a virtual environment
def create_venv():
    if sys.platform == 'win32':
        os.system('python -m venv venv')  # Windows
    else:
        os.system('python3 -m venv venv')  # macOS

# Function to activate the virtual environment
def activate_venv():
    if sys.platform == 'win32':
        os.system('venv\\Scripts\\activate')  # Windows
    else:
        os.system('source venv/bin/activate')  # macOS

# Function to install dependencies
def install_dependencies():
    if sys.platform == 'win32':
        os.system('pip install -r requirements.txt')  # Windows
    else:
        os.system('pip3 install -r requirements.txt')  # macOS

# Function to update dependencies
def update_dependencies():
    if sys.platform == 'win32':
        os.system('pip install --upgrade -r requirements.txt')  # Windows
    else:
        os.system('pip3 install --upgrade -r requirements.txt')  # macOS

# Check the operating system
if sys.platform == 'win32':
    print("Windows OS detected.")
else:
    print("macOS OS detected.")

# Check if venv folder exists
if not os.path.exists('venv'):
    print("Virtual environment not found. Creating venv...")
    create_venv()

# Activate the virtual environment
activate_venv()

# Check if dependencies are installed
try:
    import gradio  # Check if Gradio is importable
    print("Dependencies are already installed.")
except ImportError:
    print("Dependencies not found. Installing...")
    install_dependencies()

# Check for updates to dependencies
print("Checking for updates to dependencies...")
update_dependencies()

# Continue with the rest of the script (Gradio interface, etc.)

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_images(reference_image, source_folder, selected_buckets, nsfw_check, nsfw_sensitivity):
    try:
        # Load the reference image using OpenCV
        ref_img = cv2.imread(reference_image.name)
        ref_img_rgb = cv2.cvtColor(ref_img, cv2.COLOR_BGR2RGB)

        # Initialize InsightFace model
        model = insightface.app.FaceAnalysis()
        model.prepare(ctx_id=-1)

        ref_faces = model.get(ref_img_rgb)
        if not ref_faces:
            return "No face detected in the reference image. Please use a different image."
        ref_embedding = ref_faces[0].embedding

        # Create folders based on selected buckets
        for bucket in selected_buckets:
            os.makedirs(os.path.join(source_folder, f"bucket_{int(float(bucket) * 100)}"), exist_ok=True)
        os.makedirs(os.path.join(source_folder, "rejected"), exist_ok=True)

        # Check if source folder exists
        if not os.path.exists(source_folder):
            return "Invalid source folder path. Please check and try again."

        # Process source images
        image_count = 0
        for filename in os.listdir(source_folder):
            if image_count >= 1000:
                break

            filepath = os.path.join(source_folder, filename)
            src_img = cv2.imread(filepath)
        
            # Check if the image is loaded properly
            if src_img is None:
                print(f"Error loading image: {filename}. Skipping...")
                continue

            # NSFW check
            if nsfw_check:
                nsfw_result = detect(filepath)
                if nsfw_result and any([res['score'] > nsfw_sensitivity for res in nsfw_result]):
                    shutil.move(filepath, os.path.join(source_folder, "rejected"))
                    continue

            src_img_rgb = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
            src_faces = model.get(src_img_rgb)
            if not src_faces:
                shutil.move(filepath, os.path.join(source_folder, "rejected"))
                continue

            src_embedding = src_faces[0].embedding
            similarity = np.dot(ref_embedding, src_embedding) / (np.linalg.norm(ref_embedding) * np.linalg.norm(src_embedding))

            # Move to appropriate bucket
            moved = False
            for bucket in selected_buckets:
                if similarity >= float(bucket):
                    shutil.move(filepath, os.path.join(source_folder, f"bucket_{int(float(bucket) * 100)}"))
                    moved = True
                    break

            if not moved:
                shutil.move(filepath, os.path.join(source_folder, "rejected"))

            image_count += 1

        return f"Processed {image_count} images."
        
    except Exception as e:
        logging.error(f"Error processing images: {e}")
        return f"Error: {e}"

def launch_gradio(event):
    try:
        # Gradio Interface
        iface = gr.Interface(
            process_images,
            [
                gr.components.File(label="Reference Image"),
                gr.components.Textbox(label="Source Folder Path"),
                gr.components.CheckboxGroup(choices=[str(i/10) for i in range(1, 11)], label="Select Buckets (10% increments)"),
                gr.components.Checkbox(label="Enable NSFW Check"),
                gr.components.Slider(minimum=0, maximum=1, default=0.7, label="NSFW Sensitivity")
            ],
            gr.components.Textbox(label="Process Status")
        )
        iface.launch()
        event.set()  # Signal that the Gradio server has started
        
    except Exception as e:
        logging.error(f"Error launching Gradio: {e}")

if __name__ == "__main__":
    try:
        event = threading.Event()
        threading.Thread(target=launch_gradio, args=(event,)).start()
        event.wait()  # Wait for the Gradio server to start
        webbrowser.open("http://127.0.0.1:7860/", new=2)  # new=2 will open in a new tab, if possible
    except Exception as e:
        logging.error(f"Error in main: {e}")
