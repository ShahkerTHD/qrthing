import numpy as np
from PIL import Image
import time
import random

def create_base_qr():
    qr = np.ones((21, 21), dtype=np.uint8) * 255  # Start with all white

    # Finder patterns (7x7)
    finder = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 255, 255, 255, 255, 255, 0],
        [0, 255, 0, 0, 0, 255, 0],
        [0, 255, 0, 0, 0, 255, 0],
        [0, 255, 0, 0, 0, 255, 0],
        [0, 255, 255, 255, 255, 255, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ])

    # Place finders with a 1-pixel white border
    qr[1:8, 1:8] = finder
    qr[1:8, -8:-1] = finder
    qr[-8:-1, 1:8] = finder

    return qr

def generate_random_data_block():
    return ''.join(random.choice('01') for _ in range(8))

def generate_qr_combination(base_qr):
    data_area = np.ones((21, 21), dtype=bool)

    # Exclude finder patterns and their borders
    data_area[0:9, 0:9] = False
    data_area[0:9, -9:] = False
    data_area[-9:, 0:9] = False

    # Exclude the outer ring
    data_area[0, :] = False
    data_area[-1, :] = False
    data_area[:, 0] = False
    data_area[:, -1] = False

    num_data_bits = np.sum(data_area)
    num_data_blocks = (num_data_bits + 7) // 8  # Round up to nearest multiple of 8

    data_blocks = [generate_random_data_block() for _ in range(num_data_blocks)]
    data_bits = ''.join(data_blocks)

    qr_copy = base_qr.copy()
    data_positions = np.where(data_area)
    for i, bit in enumerate(data_bits[:num_data_bits]):
        qr_copy[data_positions[0][i], data_positions[1][i]] = int(bit) * 255

    return qr_copy, data_blocks

def display_combination(combo, data_blocks):
    img = Image.fromarray(combo.astype(np.uint8), 'L')
    img = img.resize((210, 210), Image.NEAREST)  # Resize for better visibility
    img.show()

    print("Data blocks:")
    print(data_blocks)
    print("----------------")

    time.sleep(0.5)  # Display for 1 second
    img.close()

def main():
    base_qr = create_base_qr()
    print("Generating and displaying QR code combinations...")
    print("Close each image window to see the next combination.")
    print("Press Ctrl+C in the terminal to stop the program.")

    try:
        while True:
            combo, data_blocks = generate_qr_combination(base_qr)
            display_combination(combo, data_blocks)
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")

if __name__ == "__main__":
    main()
