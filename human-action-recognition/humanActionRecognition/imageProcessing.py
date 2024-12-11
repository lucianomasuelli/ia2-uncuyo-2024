import os
import shutil
import pandas as pd

def move_images_to_folders(image_dir, df):
    # Crear subcarpetas para cada clase
    for class_name in df['label'].unique():
        os.makedirs(os.path.join(image_dir, class_name), exist_ok=True)
        print(f"Created directory: {os.path.join(image_dir, class_name)}")

    # Mover cada imagen a su subcarpeta correspondiente
    for _, row in df.iterrows():
        img_name = row['filename']
        class_name = row['label']
        src_path = os.path.join(image_dir, img_name)
        dest_path = os.path.join(image_dir, class_name, img_name)
        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
            print(f"Moved {src_path} to {dest_path}")
        else:
            print(f"File {src_path} not found")

def main():
    # Directorio base de imágenes
    image_dir = 'data/test/'
    # Cargar el CSV que contiene el nombre de la imagen y la clase
    df = pd.read_csv('data/Testing_set.csv')
    print(f"Loaded CSV with {len(df)} entries")
    move_images_to_folders(image_dir, df)

if __name__ == '__main__':
    main()