# Face Similarity Image Processor

This script uses the [InsightFace](https://github.com/deepinsight/insightface) model to process a set of images, comparing them to a reference image and sorting them into different "buckets" based on their similarity to the reference image. It provides a Gradio interface for easy interaction.

## Installation

### Prerequisites

- Python 3.6+
- [InsightFace](https://github.com/deepinsight/insightface) library
- [Gradio](https://github.com/gradio-app/gradio) library

You can install the required libraries using `pip`:
      
    ```bash
    pip install -r requirements.txt

## Usage

### Windows Manual

1. **Clone or download the script:** Download the script to your computer.

2. **Install the required libraries:** Open a command prompt and run the following commands to install the required libraries.

   ```bash
   pip install insightface gradio

3. Run the script: Open a command prompt in the directory where you saved the script and run it using Python.

    ```bash
    python script_name.py

4. Access the Gradio interface: Once the script is running, open your web browser and navigate to http://127.0.0.1:7860/. This will open the Gradio interface for processing images.

## Windows One-Click

1. Run **setup** (`setup.bat`) to install the venv and dependencies
2. Run **run-fc** (`run-fc.bat`) to launch the UI

## MacOS Manual

1. Clone or download the script: Download the script to your computer.
2. Install the required libraries: Open a terminal and run the following commands to install the required libraries.

    ```bash
    pip3 install insightface gradio

3. Run the script: Open a terminal in the directory where you saved the script and run it using Python.

    ```bash
    python script_name.py

Access the Gradio interface: Once the script is running, open your web browser and navigate to [http://127.0.0.1:7860/](http://127.0.0.1:7860/). This will open the Gradio interface for processing images.

## How to Use
1. Reference Image: Upload the reference image that you want to compare other images to.
2. Source Folder Path: Enter the path to the folder containing the images you want to process.
3. Select Buckets (10% increments): Choose the similarity thresholds for sorting the images into buckets. Images with similarity scores equal to or higher than the selected thresholds will be placed in the corresponding buckets.

Process Status: The processing status will be displayed in this textbox.

## Important Notes
- Make sure that the reference image and source images are in a compatible format (e.g., JPEG, PNG).
- The script will create folders for each selected bucket in the source folder and move images accordingly.
- Images with no detected faces in the source folder will be moved to a "rejected" folder.

## Troubleshooting
If you encounter any issues or errors while using this script, please check the following:

- Ensure that you have installed the required libraries (insightface and gradio) as mentioned in the installation instructions.
- Verify that the paths to the reference image and source folder are correct. The reference folder must be contained within the source folder.
- Check the format of the reference and source images.
- Review the error messages displayed in the "Process Status" textbox for more information.
- For additional assistance, refer to the script's source code or consult the documentation of the InsightFace and Gradio libraries.
