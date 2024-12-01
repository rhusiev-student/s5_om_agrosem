import os
import subprocess
import sys

def install_dependencies():
    """Install dependencies from requirements.txt"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Please check your `requirements.txt` file.")

def run_script(script_name):
    """Run a Python script"""
    print(f"Running {script_name}...")
    try:
        subprocess.check_call([sys.executable, script_name])
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError:
        print(f"Error running {script_name}. Please check the script for issues.")

def main():
    # # Create a virtual environment if one doesn't exist
    # if not os.path.exists("venv"):
    #     print("Creating virtual environment...")
    #     subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    #     print("Virtual environment created. Please activate it before continuing.")
    #     return  # End here to allow the user to activate the venv

    # Install dependencies
    install_dependencies()

    # Run preprocessing script
    run_script("preprocess.py")

    # Plot the distribution by month for each item
    run_script("plot_each_months.py")

    # Split the data by critical code and price
    run_script("split_by_pricepriority.py")

    # Analyze methods to predict next month's buyers
    run_script("analyze.py")

    # Analyze 1.2 task
    run_script("analyze_1_2.py")

    print("All tasks completed.")

if __name__ == "__main__":
    main()
