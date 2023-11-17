import numpy as np
import cv2

def get_bit_plane(img, bit):
    """ Extract the specified bit plane from the image """
    return (img & (1 << bit)) >> bit

def set_bit_plane(img, bit_plane, bit):
    """ Set the specified bit plane of the image """
    return (img & ~(1 << bit)) | (bit_plane << bit)

def calculate_complexity(block):
    """ Calculate the complexity of a block """
    diff_block = np.diff(block, axis=0) + np.diff(block, axis=1)
    complexity = np.sum(diff_block != 0) / diff_block.size
    return complexity


def embed_message(img, message, threshold=0.3):
    """ Embed a binary message into the least significant bit plane of the image """
    h, w = img.shape
    message_idx = 0
    message_len = len(message)

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            if message_idx >= message_len:
                return img

            block = img[i:i+8, j:j+8]
            complexity = calculate_complexity(block)

            if complexity > threshold:
                # Embed one byte of the message into this blockS
                for k in range(8):
                    for l in range(8):
                        if message_idx >= message_len:
                            return img

                        bit = int(message[message_idx])
                        block[k, l] = set_bit_plane(block[k, l], bit, 0)
                        message_idx += 1

                img[i:i+8, j:j+8] = block

    return img

def extract_message(img, message_len, threshold=0.3):
    """ Extract a binary message from the least significant bit plane of the image """
    h, w = img.shape
    message = ''
    message_idx = 0

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            if message_idx >= message_len:
                return message

            block = img[i:i+8, j:j+8]
            complexity = calculate_complexity(block)

            if complexity > threshold:
                for k in range(8):
                    for l in range(8):
                        if message_idx >= message_len:
                            return message

                        bit = get_bit_plane(block[k, l], 0)
                        message += str(bit)
                        message_idx += 1

    return message

# Example usage
img = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)  # Load an image
binary_message = '010101...'  # Your binary message here

# Embed the message
stego_img = embed_message(img, binary_message)

# Save or further process stego_img
cv2.imwrite('stego_image.png', stego_img)

# To extract the message
extracted_message = extract_message(stego_img, len(binary_message))
print(extracted_message)
