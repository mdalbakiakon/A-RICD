import os

def list_files_optimized(startpath):
    exclude_dirs = {
        '.git', 'venv', 'venv_1.3b', 'venv_baichuan', 
        'venv_A-RICD_benchmark', '__pycache__', '.vscode', 
        '.ipynb_checkpoints', 'data'
    }

    print(f"\n=== Searching for Adapters in: {startpath} ===\n")
    
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        folder_name = os.path.basename(root) if os.path.basename(root) else startpath
            
        if files:
            print(f"{indent}{folder_name}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if "adapter" in f or ".safetensors" in f or ".json" in f:
                    print(f"{subindent}--> {f} (IMPORTANT)")
                else:
                    print(f"{subindent}{f}")

path = r"D:\Md. Al Baki Akon\A-RICD"
list_files_optimized(path)