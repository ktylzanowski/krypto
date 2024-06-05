import time
from stegano import lsb
import os

messages = {
    "short": "Short message",
    "medium": "This is a medium-length message for testing.",
    "long": "This is a long message meant to thoroughly test the capacity of the image and the performance of the steganography library over a large volume of data."
}

image_files = {
    "small": "small_image.jpg",
    "medium": "medium_image.jpg",
    "large": "large_image.jpg"
}

results = []


def get_file_size(file_path):
    return os.path.getsize(file_path)


for image_name, image_path in image_files.items():
    original_size = get_file_size(image_path)

    for msg_label, message in messages.items():
        start_time = time.time()
        encoded_image_path = f"{image_name}_encoded_{msg_label}.png"
        secret = lsb.hide(image_path, message)
        secret.save(encoded_image_path)
        end_time = time.time()
        encode_time = end_time - start_time

        start_time = time.time()
        revealed_message = lsb.reveal(encoded_image_path)
        end_time = time.time()
        decode_time = end_time - start_time

        encoded_size = get_file_size(encoded_image_path)

        results.append({
            "image": image_name,
            "message": msg_label,
            "original_size": original_size,
            "encoded_size": encoded_size,
            "encode_time": encode_time,
            "decode_time": decode_time,
            "revealed_message": revealed_message
        })

with open("README.md", "w") as f:
    f.write("# Steganography Experiment Results\n\n")
    f.write("| Image | Message Length | Original Size (KB) | Encoded Size (KB) | Encode Time (s) | Decode Time (s) |\n")
    f.write("|-------|----------------|--------------------|-------------------|-----------------|-----------------|\n")

    for result in results:
        f.write(
            f"| {result['image']} | {result['message']} | {result['original_size'] / 1024:.2f} | {result['encoded_size'] / 1024:.2f} | {result['encode_time']:.4f} | {result['decode_time']:.4f} |\n")
