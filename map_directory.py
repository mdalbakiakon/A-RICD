import os

def list_files(startpath):
    # ডিরেক্টরিগুলোর নাম স্ল্যাশ ছাড়া এবং সঠিক বানানে দিন
    exclude_dirs = {
        '.git', 
        'venv', 
        'venv_1.3b',       # ছোট হাতের 'b' নিশ্চিত করুন
        'venv_baichuan', 
        '__pycache__', 
        '.vscode',
        '.ipynb_checkpoints' # জুপিটারের এই হিডেন ফোল্ডারটিও বাদ দেওয়া ভালো
    }

    print(f"\n=== Project Directory Map: {startpath} ===\n")
    
    for root, dirs, files in os.walk(startpath):
        # dirs[:] আপডেট করার মাধ্যমে এই ফোল্ডারগুলো আর স্ক্যান হবে না
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        
        folder_name = os.path.basename(root)
        if not folder_name:
            folder_name = startpath
            
        print(f"{indent}{folder_name}/")
        
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            # শুধুমাত্র পাইথন বা জেএসএন ফাইল দেখাতে চাইলে এখানে ফিল্টার যোগ করতে পারেন
            print(f"{subindent}{f}")

# আপনার পাথ রান করুন
path = r"D:\Md. Al Baki Akon\A-RICD"
list_files(path)