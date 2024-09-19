import os
import shutil
import random

def dividir_dataset(ruta_dataset, ruta_split, porcentaje_test=0.2, extension_imagenes=['.jpg', '.jpeg', '.png']):
    """
    Divide el dataset en conjuntos de train y test.

    :param ruta_dataset: Ruta al directorio original del dataset que contiene 'images' y 'labels'.
    :param ruta_split: Ruta al directorio donde se crearán 'train' y 'test'.
    :param porcentaje_test: Proporción del dataset que se destinará al conjunto de test (entre 0 y 1).
    :param extension_imagenes: Lista de extensiones de archivos de imágenes a considerar.
    """
    # Rutas de origen
    ruta_images = os.path.join(ruta_dataset, 'images')
    ruta_labels = os.path.join(ruta_dataset, 'labels')

    # Verificar que las carpetas existan
    if not os.path.exists(ruta_images):
        raise FileNotFoundError(f"La carpeta de imágenes no existe: {ruta_images}")
    if not os.path.exists(ruta_labels):
        raise FileNotFoundError(f"La carpeta de labels no existe: {ruta_labels}")

    # Crear directorios de destino
    conjuntos = ['train', 'test']
    for conjunto in conjuntos:
        for carpeta in ['images', 'labels']:
            ruta_carpeta = os.path.join(ruta_split, conjunto, carpeta)
            os.makedirs(ruta_carpeta, exist_ok=True)

    # Listar todas las imágenes
    todas_imagenes = [f for f in os.listdir(ruta_images) if os.path.splitext(f)[1].lower() in extension_imagenes]

    # Filtrar imágenes que tienen su correspondiente archivo de label
    imagenes_con_labels = []
    for img in todas_imagenes:
        nombre_base = os.path.splitext(img)[0]
        label = f"{nombre_base}.txt"
        if os.path.exists(os.path.join(ruta_labels, label)):
            imagenes_con_labels.append(nombre_base)
        else:
            print(f"Advertencia: No se encontró el label para la imagen {img}. Se omitirá.")

    # Número total de imágenes con labels
    total = len(imagenes_con_labels)
    if total == 0:
        raise ValueError("No se encontraron imágenes con sus correspondientes labels.")

    # Mezclar las imágenes de manera aleatoria
    random.seed(42)  # Para reproducibilidad
    random.shuffle(imagenes_con_labels)

    # Calcular la cantidad para el conjunto de test
    cantidad_test = int(total * porcentaje_test)
    test_imagenes = imagenes_con_labels[:cantidad_test]
    train_imagenes = imagenes_con_labels[cantidad_test:]

    print(f"Total de imágenes con labels: {total}")
    print(f"Imágenes para train: {len(train_imagenes)}")
    print(f"Imágenes para test: {len(test_imagenes)}")

    # Función para copiar archivos
    def copiar_archivos(imagenes, destino_imagenes, destino_labels):
        for nombre_base in imagenes:
            # Copiar imagen
            for ext in extension_imagenes:
                img_original = os.path.join(ruta_images, nombre_base + ext)
                if os.path.exists(img_original):
                    img_destino = os.path.join(destino_imagenes, nombre_base + ext)
                    shutil.copyfile(img_original, img_destino)
                    break
            else:
                print(f"Advertencia: No se encontró la imagen para {nombre_base} con las extensiones especificadas.")
                continue  # Saltar si no se encuentra la imagen

            # Copiar label
            label_original = os.path.join(ruta_labels, nombre_base + '.txt')
            label_destino = os.path.join(destino_labels, nombre_base + '.txt')
            shutil.copyfile(label_original, label_destino)

    # Copiar archivos a train
    copiar_archivos(train_imagenes,
                    os.path.join(ruta_split, 'train', 'images'),
                    os.path.join(ruta_split, 'train', 'labels'))

    # Copiar archivos a test
    copiar_archivos(test_imagenes,
                    os.path.join(ruta_split, 'test', 'images'),
                    os.path.join(ruta_split, 'test', 'labels'))

    print("División del dataset completada exitosamente.")

if __name__ == "__main__":
    # Configura las rutas según tu estructura de carpetas
    ruta_dataset = '/home/luciano/Documentos/Facultad/4to/2_semestre/ia2-practica/practica_yolo/vehicleDetection/data/train'          # Carpeta que contiene 'images' y 'labels'
    ruta_split = '/home/luciano/Escritorio'      # Carpeta donde se crearán 'train' y 'test'
    porcentaje_test = 0.1                         # 20% para test

    dividir_dataset(ruta_dataset, ruta_split, porcentaje_test)
