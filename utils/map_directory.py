import os

def list_files_optimized(startpath):
    # বাদ দেওয়ার ফোল্ডারগুলো (কমা নিশ্চিত করা হয়েছে)
    exclude_dirs = {
        '.git', 'venv', 'venv_1.3b', 'venv_baichuan', 
        'venv_A-RICD_benchmark', '__pycache__', '.vscode', 
        '.ipynb_checkpoints', 'data' # আপাতত ডেটা ফোল্ডার বাদ দিচ্ছি যাতে আউটপুট ছোট হয়
    }

    print(f"\n=== Searching for Adapters in: {startpath} ===\n")
    
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        folder_name = os.path.basename(root) if os.path.basename(root) else startpath
            
        # শুধুমাত্র যদি ফোল্ডারে ফাইল থাকে তবেই প্রিন্ট করবে
        if files:
            print(f"{indent}{folder_name}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                # এডাপ্টার রিলেটেড ফাইলগুলো হাইলাইট করা
                if "adapter" in f or ".safetensors" in f or ".json" in f:
                    print(f"{subindent}--> {f} (IMPORTANT)")
                else:
                    print(f"{subindent}{f}")

path = r"D:\Md. Al Baki Akon\A-RICD"
list_files_optimized(path)