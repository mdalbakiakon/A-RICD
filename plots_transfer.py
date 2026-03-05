import os
import shutil

def organize_plots(startpath):
    # ১. 'plots' ফোল্ডারের পাথ তৈরি করা
    plot_folder = os.path.join(startpath, 'plots')
    
    # ২. ফোল্ডারটি না থাকলে তৈরি করা
    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)
        print(f"Created new folder: {plot_folder}")

    # ৩. রুটে থাকা সব ফাইল চেক করা
    files_moved = 0
    for file in os.listdir(startpath):
        # শুধুমাত্র .png ফাইল এবং যেগুলো সরাসরি রুটে আছে সেগুলোকে টার্গেট করা
        if file.lower().endswith('.png'):
            source_path = os.path.join(startpath, file)
            destination_path = os.path.join(plot_folder, file)
            
            # ফাইলটি ট্রান্সফার করা
            shutil.move(source_path, destination_path)
            print(f"Moved: {file} -> plots/")
            files_moved += 1

    if files_moved == 0:
        print("ℹ️ No PNG files found in the root directory.")
    else:
        print(f"✅ Successfully moved {files_moved} plots to the 'plots' folder.")

# আপনার প্রজেক্ট পাথ ব্যবহার করুন
path = r"D:\Md. Al Baki Akon\A-RICD"
organize_plots(path)