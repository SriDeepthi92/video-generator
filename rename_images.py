import os

folder_path = r"C:\Users\sride\Downloads\Ramayana"

# Get full file paths
files = [
    os.path.join(folder_path, f)
    for f in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, f))
]

# Sort by modified time (oldest first)
files.sort(key=os.path.getmtime)

# Temporary rename first (prevents overwrite errors)
for i, file in enumerate(files):
    temp_name = os.path.join(folder_path, f"temp_{i:03d}")
    os.rename(file, temp_name)

# Get temp files
temp_files = [
    os.path.join(folder_path, f)
    for f in os.listdir(folder_path)
    if f.startswith("temp_")
]

temp_files.sort()

# Final rename
for i, file in enumerate(temp_files, start=1):
    ext = ".png"  # change if your files are .jpg
    new_name = os.path.join(folder_path, f"{i:03d}{ext}")
    os.rename(file, new_name)

print("✅ Done. Oldest file is 001.")


