import os
import sys
import subprocess

# Function to create a virtual environment, install, and update dependencies
def create_venv():
    if sys.platform == 'win32':
        os.system('python -m venv venv')  # Windows
        os.system('venv\\Scripts\\activate')  # Activate venv on Windows
        os.system('pip install -r requirements.txt')  # Install dependencies on Windows
        os.system('pip install --upgrade -r requirements.txt')  # Update dependencies on Windows
    else:
        os.system('python3 -m venv venv')  # macOS
        os.system('source venv/bin/activate')  # Activate venv on macOS
        os.system('pip3 install -r requirements.txt')  # Install dependencies on macOS
        os.system('pip3 install --upgrade -r requirements.txt')  # Update dependencies on macOS

# Function to activate the virtual environment
def activate_venv():
    if sys.platform == 'win32':
        os.system('venv\\Scripts\\activate')  # Windows
    else:
        os.system('source venv/bin/activate')  # macOS

# Check the operating system
if sys.platform == 'win32':
    print("Windows OS detected.")
else:
    print("macOS OS detected.")

# Check if venv folder exists
if not os.path.exists('venv'):
    print("Virtual environment not found. Creating venv and installing/updating dependencies...")
    create_venv()
else:
    print("Virtual environment found.")

# Activate the virtual environment
activate_venv()

# Execute launch.py with the appropriate Python executable
if sys.platform == 'win32':
    subprocess.call(["python", "launch.py"])  # Use 'python' on Windows
else:
    subprocess.call(["python3", "launch.py"])  # Use 'python3' on macOS
