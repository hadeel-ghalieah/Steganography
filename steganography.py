import cv2
import numpy as np
from PIL import Image

# Convert message to binary format
def data2binary(data):
    if type(data) == str:
        binary_data = ''.join([format(ord(i), '08b') for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        binary_data = [format(i, '08b') for i in data]
    return binary_data

# Hide data in the given image
def hide_data(img, data):
    data += "$$"  # '$$' is the secret key
    data_index = 0
    binary_data = data2binary(data)
    len_data = len(binary_data)

    # Iterate over pixels from the image and update pixel values
    for i in range(len(img)):
        for j in range(len(img[i])):
            r, g, b = data2binary(img[i][j])
            if data_index < len_data:
                img[i][j][0] = int(r[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index < len_data:
                img[i][j][1] = int(g[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index < len_data:
                img[i][j][2] = int(b[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index >= len_data:
                break
    return img

# Encode message into image
def encode():
    img_name = input("\nEnter image name: ")
    image = cv2.imread(img_name)
    img = Image.open(img_name, 'r')
    w, h = img.size
    data = input("\nEnter message: ")
    
    if len(data) == 0:
        raise ValueError("Empty data")

    enc_img = input("\nEnter encoded image name (with valid extension, e.g., .png): ")
    enc_data = hide_data(image, data)
    cv2.imwrite(enc_img, enc_data)

    img1 = Image.open(enc_img, 'r')
    img1 = img1.resize((w, h), resample=Image.BICUBIC)

    # Optimize with 95% quality
    img1.save(enc_img, quality=95)

# find message from image
def find_data(img):
    binary_data = ""
    for i in range(len(img)):
        for j in range(len(img[i])):
            r, g, b = data2binary(img[i][j])
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]

    # Group binary data into chunks of 8 bits
    all_bytes = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]

    # Convert each 8-bit chunk to a decimal number and then to a character
    readable_data = "".join([chr(int(byte, 2)) for byte in all_bytes])

    # Find the end of the message marker
    end_marker_index = readable_data.find("$$")

    if end_marker_index != -1:
        return readable_data[:end_marker_index]
    else:
        print("Error: End marker not found in the decoded data.")
        return readable_data


# Decode function
def decode():
    img_name = input("\nEnter Image name: ")
    image = cv2.imread(img_name)
    msg = find_data(image)
    return msg

# Main steganography function
def steganography():
    x = 1
    while x != 0:
        print('''\nImage steganography
        1. Encode
        2. Decode''')
        user_input = int(input("\nEnter your choice: "))
        
        if user_input == 1:
            encode()
        else:
            ans = decode()
            print("\nYour message: " + ans)
        
        x = int(input("\nEnter 1 to continue, otherwise 0: "))

# Run the steganography function
steganography()
