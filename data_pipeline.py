import os
import subprocess

def gather_data():
    print("Step 1: Gathering Data")
    gather_data_command = "python gather_data.py"
    subprocess.call(gather_data_command, shell=True)
    print("Data Gathering Completed.")

def data_augmentation():
    print("Step 2: Data Augmentation")
    data_augmentation_command = "python data_augmentation.py"
    subprocess.call(data_augmentation_command, shell=True)
    print("Data Augmentation Completed.")

if __name__ == "__main__":
    gather_data()
    data_augmentation()
