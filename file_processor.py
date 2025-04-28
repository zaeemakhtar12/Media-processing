import os
import random
from PIL import Image, ImageEnhance, ImageFilter
from vidspinner import MontageBuilder
from vidspinner.filters import Filter

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

# List of media files to process
media_files = [
    "media/video.mp4",
    # you can add more files here (images or videos)
]

# Available effects
available_effects = [
    "SEPIA", "RETRO", "BLACK_WHITE", "INVERT", "SKETCH", "VIGNETTE",
    "COLORIZE", "PSYCHEDELIC", "SHARPEN", "BRIGHT_LIGHTS", "DARK_SHADOWS",
    "MIRRORS", "DREAMY", "VINTAGE", "ANIME", "CRACKLE", "FISHEYE"
]

def process_photo(file_path):
    try:
        image = Image.open(file_path)

        effect = random.choice(available_effects)

        if effect == "SEPIA":
            sepia_filter = [(255, 240, 192), (204, 153, 102), (153, 102, 51)]
            image = image.convert("RGB")
            pixels = image.load()

            for i in range(image.width):
                for j in range(image.height):
                    r, g, b = image.getpixel((i, j))
                    tr = int(r * 0.393 + g * 0.769 + b * 0.189)
                    tg = int(r * 0.349 + g * 0.686 + b * 0.168)
                    tb = int(r * 0.272 + g * 0.534 + b * 0.131)
                    pixels[i, j] = (tr, tg, tb)

        elif effect == "RETRO":
            image = ImageEnhance.Color(image).enhance(0.6)
            image = ImageEnhance.Brightness(image).enhance(0.8)

        elif effect == "BLACK_WHITE":
            image = image.convert("L")

        elif effect == "INVERT":
            image = Image.eval(image, lambda x: 255 - x)

        elif effect == "SKETCH":
            image = image.convert("L")
            image = ImageEnhance.Contrast(image).enhance(2.0)

        elif effect == "VIGNETTE":
            image = ImageEnhance.Brightness(image).enhance(0.8)

        elif effect == "COLORIZE":
            image = ImageEnhance.Color(image).enhance(random.uniform(0.5, 1.5))

        elif effect == "PSYCHEDELIC":
            image = ImageEnhance.Color(image).enhance(1.6)

        elif effect == "SHARPEN":
            image = image.filter(ImageFilter.SHARPEN)

        elif effect == "BRIGHT_LIGHTS":
            image = ImageEnhance.Brightness(image).enhance(1.5)

        elif effect == "DARK_SHADOWS":
            image = ImageEnhance.Brightness(image).enhance(0.5)

        elif effect == "MIRRORS":
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

        elif effect == "DREAMY":
            image = ImageEnhance.Contrast(image).enhance(0.6)

        elif effect == "VINTAGE":
            image = ImageEnhance.Color(image).enhance(0.8)
            image = ImageEnhance.Brightness(image).enhance(0.9)

        elif effect == "ANIME":
            image = ImageEnhance.Color(image).enhance(1.2)

        elif effect == "CRACKLE":
            image = image.convert("RGB")
            pixels = image.load()
            for i in range(image.width):
                for j in range(image.height):
                    r, g, b = image.getpixel((i, j))
                    tr = int(r * random.uniform(0.9, 1.1))
                    tg = int(g * random.uniform(0.9, 1.1))
                    tb = int(b * random.uniform(0.9, 1.1))
                    pixels[i, j] = (tr, tg, tb)

        elif effect == "FISHEYE":
            image = image.resize((int(image.width * 0.9), int(image.height * 0.9)))

        # Save the processed image
        output_file = os.path.join(
            "output",
            os.path.basename(file_path).replace(".jpg", f"_{effect}_processed.jpg")
        )
        image.save(output_file)
        print(f"[✓] Processed image with {effect}: {output_file}")
        return output_file

    except Exception as e:
        print(f"[✗] Image error ({file_path}): {e}")
        return None

def process_video(file_path):
    try:
        effect = random.choice(available_effects)

        builder = MontageBuilder()
        builder.input = file_path
        output_file = os.path.join(
            "output",
            os.path.basename(file_path).replace(".mp4", f"_{effect}.mp4")
        )
        builder.output = output_file
        builder.clear_meta_tags = True

        builder.add_filter(getattr(Filter, effect))

        builder.build()
        print(f"[✓] Processed video with {effect}: {output_file}")
        return output_file

    except Exception as e:
        print(f"[✗] Video error ({file_path}): {e}")
        return None

def main():
    success = 0
    for path in media_files:
        if not os.path.exists(path):
            print(f"[!] File not found: {path}")
            continue

        if path.lower().endswith((".jpg", ".jpeg", ".png")):
            result = process_photo(path)
        elif path.lower().endswith(".mp4"):
            result = process_video(path)
        else:
            print(f"[!] Skipped unsupported file: {path}")
            result = None

        if result:
            success += 1

    print(f"\n[✓] Finished processing {success}/{len(media_files)} file(s).")

if __name__ == "__main__":
    main()
