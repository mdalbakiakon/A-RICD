import os
import shutil

def organize_plots(startpath):
    plot_folder = os.path.join(startpath, 'plots')
    
    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)
        print(f"Created new folder: {plot_folder}")

    files_moved = 0
    for file in os.listdir(startpath):
        if file.lower().endswith('.png'):
            source_path = os.path.join(startpath, file)
            destination_path = os.path.join(plot_folder, file)
            
            shutil.move(source_path, destination_path)
            print(f"Moved: {file} -> plots/")
            files_moved += 1

    if files_moved == 0:
        print("ℹ️ No PNG files found in the root directory.")
    else:
        print(f"✅ Successfully moved {files_moved} plots to the 'plots' folder.")

path = r"D:\Md. Al Baki Akon\A-RICD"
organize_plots(path)