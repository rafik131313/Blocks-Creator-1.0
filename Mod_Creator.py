import os
import json
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox


# Funkcja do wyboru folderu głównego projektu
def choose_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_path_var.set(directory)


# Funkcja do wyboru i kopiowania plików obrazów
def choose_images():
    image_files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png")])
    if image_files:
        images_list_var.set(image_files)


# Funkcja do kopiowania obrazów
# Funkcja do kopiowania obrazów
def copy_images(image_files, output_directory):
    textures_dir = os.path.join(output_directory, "src/main/resources/assets/examplemod/textures/block")
    os.makedirs(textures_dir, exist_ok=True)

    if not image_files:
        messagebox.showerror("Błąd", "Nie wybrano żadnych plików obrazów.")
        return

    # Przetwarzanie plików obrazów
    for image_file in image_files:
        image_file = image_file.strip().strip("'\"")  # Usuwa cudzysłowy wokół ścieżki

        if not image_file:  # Jeśli image_file jest pusty
            continue

        image_name = os.path.basename(image_file)
        print(f"Kopiowanie pliku: {image_file} do {os.path.join(textures_dir, image_name)}")  # Debugowanie
        try:
            shutil.copy(image_file, os.path.join(textures_dir, image_name))
        except FileNotFoundError as e:
            messagebox.showerror("Błąd", f"Nie znaleziono pliku obrazu: {image_file}\n{str(e)}")



# Funkcja do aktualizacji pliku językowego en_us.json
def update_lang_file(block_names, output_directory):
    lang_file_path = os.path.join(output_directory, "src/main/resources/assets/examplemod/lang/en_us.json")

    if os.path.exists(lang_file_path):
        with open(lang_file_path, 'r') as lang_file:
            lang_data = json.load(lang_file)
    else:
        lang_data = {}

    for block_name in block_names:
        clean_name = block_name.replace(" ", "").replace(",", "").replace("\"", "").lower()
        display_name = block_name.replace("_", " ").replace("\"", "").replace(",", "").strip().title()
        lang_data[f"block.examplemod.{clean_name}"] = display_name

    with open(lang_file_path, 'w') as lang_file:
        json.dump(lang_data, lang_file, indent=2)


# Funkcja do aktualizacji pliku Java
def update_java_file(block_names, output_directory):
    java_file_path = os.path.join(output_directory, "src/main/java/com/example/examplemod/ExampleMod.java")

    if not os.path.exists(java_file_path):
        messagebox.showerror("Błąd", f"Nie znaleziono pliku ExampleMod.java w: {java_file_path}")
        return

    with open(java_file_path, 'r') as java_file:
        java_code = java_file.readlines()

    for idx, line in enumerate(java_code):
        if "List.of(" in line:
            insert_idx = idx + 1
            break
    else:
        messagebox.showerror("Błąd", "Nie znaleziono miejsca do dodania nowych bloków.")
        return

    for block_name in block_names:
        clean_name = block_name.replace(" ", "").replace(",", "").replace("\"", "").lower()
        java_code.insert(insert_idx, f'            "{clean_name}",\n')
        insert_idx += 1

    with open(java_file_path, 'w') as java_file:
        java_file.writelines(java_code)


# Funkcja do budowania projektu z pomocą Gradle
def build_project_with_gradle(output_directory):
    gradlew_path = os.path.join(output_directory, "gradlew.bat" if os.name == 'nt' else "gradlew")

    if not os.path.exists(gradlew_path):
        messagebox.showerror("Błąd", "Nie znaleziono pliku gradlew. Upewnij się, że ścieżka jest poprawna.")
        return

    try:
        result = subprocess.run([gradlew_path, "build"], cwd=output_directory, check=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        messagebox.showinfo("Sukces", "Budowanie zakończone sukcesem!\n" + result.stdout.decode())
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Błąd", "Wystąpił błąd podczas budowania projektu.\n" + e.stderr.decode())


# Funkcja do generowania plików JSON
def generate_json_files():
    block_names = block_names_entry.get("1.0", tk.END).strip().splitlines()
    output_directory = output_path_var.get()
    image_files = images_list_var.get().strip("() ").split(',')
    image_files = [image.strip() for image in image_files]

    if not output_directory:
        messagebox.showerror("Błąd", "Wybierz ścieżkę zapisu!")
        return

    if not block_names:
        messagebox.showerror("Błąd", "Wklej listę nazw bloków!")
        return

    # Ścieżki do różnych folderów
    recipe_dir = os.path.join(output_directory, "src/main/resources/data/examplemod/recipe")
    blockstates_dir = os.path.join(output_directory, "src/main/resources/assets/examplemod/blockstates")
    models_block_dir = os.path.join(output_directory, "src/main/resources/assets/examplemod/models/block")
    models_item_dir = os.path.join(output_directory, "src/main/resources/assets/examplemod/models/item")

    os.makedirs(recipe_dir, exist_ok=True)
    os.makedirs(blockstates_dir, exist_ok=True)
    os.makedirs(models_block_dir, exist_ok=True)
    os.makedirs(models_item_dir, exist_ok=True)

    for block_name in block_names:
        clean_name = block_name.replace(" ", "").replace(",", "").replace("\"", "").lower()

        # Plik recipe
        recipe_data = {
            "type": "minecraft:stonecutting",
            "ingredient": {
                "item": "minecraft:dirt"
            },
            "result": {
                "id": f"examplemod:{clean_name}",
                "count": 1
            }
        }
        recipe_path = os.path.join(recipe_dir, f"{clean_name}.json")
        with open(recipe_path, 'w') as json_file:
            json.dump(recipe_data, json_file, indent=2)

        # Plik blockstates
        blockstates_data = {
            "variants": {
                "": {"model": f"examplemod:block/{clean_name}"}
            }
        }
        blockstates_path = os.path.join(blockstates_dir, f"{clean_name}.json")
        with open(blockstates_path, 'w') as json_file:
            json.dump(blockstates_data, json_file, indent=2)

        # Plik models/block
        models_block_data = {
            "parent": "block/cube_all",
            "textures": {
                "all": f"examplemod:block/{clean_name}"
            }
        }
        models_block_path = os.path.join(models_block_dir, f"{clean_name}.json")
        with open(models_block_path, 'w') as json_file:
            json.dump(models_block_data, json_file, indent=2)

        # Plik models/item
        models_item_data = {
            "parent": f"examplemod:block/{clean_name}"
        }
        models_item_path = os.path.join(models_item_dir, f"{clean_name}.json")
        with open(models_item_path, 'w') as json_file:
            json.dump(models_item_data, json_file, indent=2)

    copy_images(image_files, output_directory)
    update_java_file(block_names, output_directory)
    update_lang_file(block_names, output_directory)
    build_project_with_gradle(output_directory)  # Uruchomienie Gradle po dokonaniu zmian

    messagebox.showinfo("Sukces", "Pliki JSON i obrazy zostały wygenerowane, a projekt został zbudowany!")


# Tworzenie okna głównego
root = tk.Tk()
root.title("Generator Plików JSON")
root.geometry("500x400")

output_path_var = tk.StringVar()
images_list_var = tk.StringVar()

# Etykieta i przycisk do wyboru ścieżki zapisu
tk.Label(root, text="Wybierz ścieżkę folderu głównego projektu:").pack(pady=5)
tk.Entry(root, textvariable=output_path_var, width=40).pack(pady=5)
tk.Button(root, text="Wybierz folder", command=choose_directory).pack(pady=5)

# Etykieta i pole do wklejenia listy nazw bloków
tk.Label(root, text="Wklej listę nazw bloków (jeden na linię):").pack(pady=5)
block_names_entry = tk.Text(root, height=10, width=40)
block_names_entry.pack(pady=5)

# Przycisk do wyboru obrazów
tk.Button(root, text="Wybierz obrazy", command=choose_images).pack(pady=5)

# Przycisk do generowania plików JSON i kopiowania obrazów
tk.Button(root, text="Generuj pliki JSON i kopiuj obrazy", command=generate_json_files).pack(pady=10)

# Uruchomienie aplikacji
root.mainloop()
