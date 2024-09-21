from PIL import Image
import numpy as np
import os

def hide_message(image_path, message, output_image_path):
    # Cargar la imagen
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    # Convertir el mensaje en binario
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    binary_message += '1111111111111110'  # Delimitador de fin de mensaje
    
    # Convertir la imagen en un array de numpy
    img_array = np.array(img)
    
    # Asegúrate de que el mensaje quepa en la imagen
    if len(binary_message) > img_array.size:
        raise ValueError("El mensaje es demasiado largo para la imagen.")
    
    # Insertar el mensaje en los bits menos significativos
    data_index = 0
    for row in img_array:
        for pixel in row:
            for i in range(3):  # R, G, B
                if data_index < len(binary_message):
                    # Cambiar el bit menos significativo
                    pixel[i] = (pixel[i] & ~1) | int(binary_message[data_index])
                    data_index += 1
    
    # Crear la nueva imagen y guardarla
    new_image = Image.fromarray(img_array)
    new_image.save(output_image_path)

def create_image_copy(image_path):
    # Crear una copia de la imagen
    base, ext = os.path.splitext(image_path)
    copy_path = f"{base}_copy{ext}"
    img = Image.open(image_path)
    img.save(copy_path)
    print(f"Copia de la imagen creada: {copy_path}")

def open_image_with_copy(image_path):
    create_image_copy(image_path)
    img = Image.open(image_path)
    img.show()

# Parámetros
image_path = 'imagen_original.png'  # Cambia esto a tu imagen original
output_image_path = 'imagen_resultante.png'
message = 'Hola, este es un mensaje secreto.'

# Escribir el mensaje en la imagen
hide_message(image_path, message, output_image_path)

# Abrir la imagen resultante y crear una copia
open_image_with_copy(output_image_path)
