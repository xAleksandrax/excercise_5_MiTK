import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# Global variables to store file paths
input_image_path = ""
output_image_path = ""


def hide_text():
    """Hide text inside an image.

    This function hides text inside an image using a simple steganography technique. It retrieves the input text from the entry field, encrypts it using a Caesar cipher with a fixed shift of 3, converts it to binary, and then hides it in the least significant bit (LSB) of the blue channel of each pixel in the image.

    If no input image is selected, it displays a warning message. Similarly, if no text is entered, it prompts the user to input text.
    """
    global input_image_path, output_image_path

    if not input_image_path:
        messagebox.showwarning("Warning", "Select an input image!")
        return

    img = Image.open(input_image_path)
    img = img.convert("RGB")

    text = entry_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Warning", "Enter text to hide!")
        return

    encrypted_text = caesar_cipher(text, 3)

    binary_text = ''.join(format(ord(char), '08b') for char in encrypted_text)

    img_with_text = hide_text_in_image(img, binary_text)

    if output_image_path:
        img_with_text.save(output_image_path)
        messagebox.showinfo("Success", "Text successfully hidden in the image!")


def reveal_text():
    """Reveal text from an image.

    This function reveals hidden text from an image. It extracts the hidden binary text from the LSB of the blue channel of each pixel in the image, decodes it, and then decrypts it using a Caesar cipher with a shift of 3.

    If no input image is selected, it displays a warning message.
    """
    global input_image_path

    if not input_image_path:
        messagebox.showwarning("Warning", "Select an image!")
        return

    img = Image.open(input_image_path)
    img = img.convert("RGB")

    hidden_text = reveal_text_from_image(img)

    decrypted_text = caesar_decipher(hidden_text, 3)

    messagebox.showinfo("Revealed Text", decrypted_text)


def hide_text_in_image(image, text):
    """Hide text within the image.

    This function hides the binary representation of the provided text within the image by modifying the LSB of the blue channel of each pixel.

    Args:
        image (PIL.Image.Image): The input image.
        text (str): The binary text to be hidden in the image.

    Returns:
        PIL.Image.Image: The image with the text hidden inside.
    """
    pixels = list(image.getdata())
    new_pixels = []

    for i, pixel in enumerate(pixels):
        if i < len(text):
            new_pixel = list(pixel)
            new_pixel[2] = pixel[2] & ~1 | int(text[i])
            new_pixels.append(tuple(new_pixel))
        else:
            new_pixels.append(pixel)

    img_with_text = Image.new(image.mode, image.size)
    img_with_text.putdata(new_pixels)
    return img_with_text


def reveal_text_from_image(image):
    """Reveal text from the image.

    This function reveals the hidden binary text from the image by extracting it from the LSB of the blue channel of each pixel.

    Args:
        image (PIL.Image.Image): The image containing the hidden text.

    Returns:
        str: The binary text extracted from the image.
    """
    pixels = list(image.getdata())
    binary_text = ''

    for pixel in pixels:
        binary_text += str(pixel[2] & 1)

    stop_index = binary_text.find('00000000')

    binary_text = binary_text[:stop_index]

    if len(binary_text) % 8 != 0:
        binary_text = binary_text[:-(len(binary_text) % 8)]

    text = ''.join(chr(int(binary_text[i:i + 8], 2)) for i in range(0, len(binary_text), 8))

    return text


def caesar_cipher(text, shift):
    """Encrypt text using the Caesar cipher.

    This function encrypts the input text using the Caesar cipher with the specified shift value.

    Args:
        text (str): The text to be encrypted.
        shift (int): The shift value for encryption.

    Returns:
        str: The encrypted text.
    """
    result = ''
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            result += chr(shifted)
        else:
            result += char
    return result


def caesar_decipher(text, shift):
    """Decrypt text encrypted with the Caesar cipher.

    This function decrypts the input text encrypted with the Caesar cipher using the specified shift value.

    Args:
        text (str): The text to be decrypted.
        shift (int): The shift value for decryption.

    Returns:
        str: The decrypted text.
    """
    return caesar_cipher(text, -shift)


def select_input_image():
    """Select the input image.

    This function opens a file dialog for the user to select the input image.
    """
    global input_image_path
    input_image_path = filedialog.askopenfilename(title="Select Input Image")
    if input_image_path:
        messagebox.showinfo("Selected", f"Selected input image: {input_image_path}")


def select_output_image():
    """Select the output image path.

    This function opens a file dialog for the user to select the path to save the output image with hidden text.
    """
    global output_image_path
    output_image_path = filedialog.asksaveasfilename(title="Save Image with Hidden Text", defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png")])
    if output_image_path:
        messagebox.showinfo("Selected", f"Selected output image path: {output_image_path}")


def select_image_to_reveal():
    """Select the image containing hidden text to reveal.

    This function opens a file dialog for the user to select the image containing hidden text that they want to reveal.
    """
    global input_image_path
    input_image_path = filedialog.askopenfilename(title="Select Image with Hidden Text")
    if input_image_path:
        messagebox.showinfo("Selected", f"Selected image with hidden text: {input_image_path}")


root = tk.Tk()
root.title("Steganography")

frame_text = tk.Frame(root, padx=10, pady=10)
frame_text.pack()

label_text = tk.Label(frame_text, text="Enter text to hide:")
label_text.pack()

entry_text = tk.Text(frame_text, height=4, width=50)
entry_text.pack()

frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.pack()

button_select_input_image = tk.Button(frame_buttons, text="Select Input Image", command=select_input_image)
button_select_input_image.pack(side=tk.LEFT, padx=5)

button_select_output_image = tk.Button(frame_buttons, text="Select Output Image Path",
                                       command=select_output_image)
button_select_output_image.pack(side=tk.LEFT, padx=5)

button_hide = tk.Button(frame_buttons, text="Hide Text in Image", command=hide_text)
button_hide.pack(side=tk.LEFT, padx=5)

button_select_image_to_reveal = tk.Button(frame_buttons, text="Select Image with Hidden Text",
                                          command=select_image_to_reveal)
button_select_image_to_reveal.pack(side=tk.LEFT, padx=5)

button_reveal = tk.Button(frame_buttons, text="Reveal Text from Image", command=reveal_text)
button_reveal.pack(side=tk.LEFT, padx=5)

root.mainloop()
