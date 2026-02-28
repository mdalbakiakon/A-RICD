import os

def list_files(startpath):
    print(f"\n=== Project Directory Map: {startpath} ===\n")
    for root, dirs, files in os.walk(startpath):
        
        if '.git' in dirs: dirs.remove('.git')
        if 'venv' in dirs: dirs.remove('venv')
        if '__pycache__' in dirs: dirs.remove('__pycache__')
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")


# path = "D:\\A-RICD"
path = "D:\\Md. Al Baki Akon\\A-RICD"
list_files(path)