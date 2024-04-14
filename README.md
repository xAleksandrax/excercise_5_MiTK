# Steganography Application
This application allows users to hide text inside images using a simple steganography technique and also to reveal hidden text from images.

# Features
Hide Text in Image: Users can select an image and enter text to hide within it. The application encrypts the text using a Caesar cipher with a fixed shift of 3, converts it to binary, and then hides it in the least significant bit (LSB) of the blue channel of each pixel in the image.

Reveal Text from Image: Users can select an image containing hidden text, and the application will extract and decrypt the hidden text, revealing the original message.

# Usage
1. Run the script exercise_5.py.
2. Enter the text you want to hide in the provided text entry field.
3. Click on the "Hide Text in Image" button to hide the text within the selected image.
4. If you wish to save the image with the hidden text, click on the "Select Output Image Path" button and choose a location to save the image.
5. To reveal hidden text from an image, click on the "Select Image with Hidden Text" button and choose the image containing the hidden text.
6. Click on the "Reveal Text from Image" button to reveal the hidden text.
