from tkinter import *
from tkinter import filedialog
from PIL import ImageDraw, Image, ImageFont

OUTPUT_IMAGE_PATH = "sample-out.png"


def upload_image_and_add_watermark():
    # Hide the root window
    root.withdraw()

    # Get file path of the image
    file_path = filedialog.askopenfilename()
    print("Selected file:", file_path)

    # Open a new window
    watermark_window = Toplevel()
    watermark_window.wm_title("")
    watermark_window.config(padx=50, pady=50)

    # Create a new PhotoImage with the uploaded image and display it
    image = PhotoImage(file=file_path)
    image_label = Label(watermark_window, image=image)
    image_label.grid(row=0, column=0)

    # Create buttons
    add_text_button = Button(master=watermark_window, text="Add Text", fg="blue", font=("Arial", 20),
                             command=lambda: add_text(file_path))
    add_text_button.grid(row=1, column=0)
    add_logo_button = Button(master=watermark_window, text="Add Logo", fg="blue", font=("Arial", 20),
                             command=lambda: add_logo(file_path))
    add_logo_button.grid(row=1, column=1)

    watermark_window.mainloop()

    return ""


def add_text(file_path):
    # Open the image file
    image = Image.open(file_path)

    # Open a new window
    text_properties = Toplevel()
    text_properties.wm_title("Properties")
    text_properties.config(padx=80, pady=150)

    # Create label
    label = Label(text_properties, text="Text", font=("Arial", 20))
    label.grid(row=0, column=0)

    # Create text input
    text_input = Text(text_properties, height=5, width=20)
    text_input.grid(row=0, column=1)

    # Create button
    next_step_button = Button(master=text_properties, text="Next Step", fg="blue", font=("Arial", 20),
                              command=lambda: add_watermark_text(image, text_input))
    next_step_button.grid(row=1, column=0)
    return ""


def add_watermark_text(original_image, text_input):
    # Get watermark text from text input
    text = text_input.get(1.0, "end-1c")

    # Make the image editable
    txt = Image.new('RGBA', original_image.size, (255, 255, 255, 0))

    # Choose a font and size
    font = ImageFont.truetype("ARIALNI.TTF", 40)

    # Initialize ImageDraw
    draw = ImageDraw.Draw(txt)

    # Get the width and height of the image
    width, height = original_image.size

    # Get the bounding box of the text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calculate the position for the watermark
    x = width - text_width - 10
    y = height - text_height - 10

    # Add watermark
    draw.text((x, y), text, fill=(255, 255, 255, 128), font=font)

    # Combine original image with watermark
    watermarked = Image.alpha_composite(original_image.convert('RGBA'), txt)

    # Save the result
    watermarked.show()
    watermarked.save(OUTPUT_IMAGE_PATH)
    return ""


def add_logo(file_path):
    # Open image file
    image = Image.open(file_path)

    # Open a new window
    logo_properties = Toplevel()
    logo_properties.wm_title("Properties")
    logo_properties.config(padx=80, pady=150)

    # Add label
    logo_label = Label(logo_properties, text="Logo", font=("Arial", 20))
    logo_label.grid(row=0, column=0)

    # Add button
    add_logo_button = Button(master=logo_properties, text="Upload logo", fg="blue", font=("Arial", 30),
                             command=lambda: upload_logo_and_add_watermark(image))
    add_logo_button.grid(row=0, column=1)
    return ""


def upload_logo_and_add_watermark(original_image):
    # Get logo image file path
    file_path = filedialog.askopenfilename()
    print("Selected file:", file_path)

    # Open the logo image
    logo = Image.open(file_path)

    # Resize the logo image
    logo = resize_image_with_aspect_ratio(logo, 50)

    # Calculate the position for the logo
    x = original_image.width - logo.width - 10
    y = original_image.height - logo.height - 10

    # Paste the logo onto the main image
    original_image.paste(logo, (x, y))

    # Save the result
    original_image.show()
    original_image.save(OUTPUT_IMAGE_PATH)
    return ""


def resize_image_with_aspect_ratio(original_image, base_width):
    # Calculate the new height to preserve the aspect ratio
    width_percent = (base_width / float(original_image.size[0]))
    new_height = int((float(original_image.size[1]) * float(width_percent)))

    # Resize the image using LANCZOS resampling
    resized_image = original_image.resize((base_width, new_height), Image.Resampling.LANCZOS)
    return resized_image


# Create root window
root = Tk()
root.title("Watermark image")
root.config(padx=50, pady=50)

# Create canvas
canvas = Canvas(master=root, width=1200, height=500)
canvas.grid(row=0, column=0)

# Create label
label = Label(root, text="Add watermark to image", font=("Arial", 50))
label.grid(row=0, column=0)

# Create button
button = Button(text="Upload Image", fg="blue", font=("Arial", 30), command=upload_image_and_add_watermark)
button.grid(row=1, column=0)

root.mainloop()
