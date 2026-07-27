import os
from PIL import Image

def convert_webp_to_png(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for filename in os.listdir(src_dir):
        if filename.endswith(".webp"):
            img_path = os.path.join(src_dir, filename)
            png_filename = filename.replace(".webp", ".png")
            dest_path = os.path.join(dest_dir, png_filename)

            try:
                with Image.open(img_path) as img:
                    img.save(dest_path, "PNG")
                print(f"Converted: {filename} -> {png_filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")
        elif filename.endswith(".png"):
            # copy existing pngs directly
            import shutil
            src_path = os.path.join(src_dir, filename)
            dest_path = os.path.join(dest_dir, filename)
            shutil.copy2(src_path, dest_path)
            print(f"Copied: {filename}")

if __name__ == "__main__":
    convert_webp_to_png("visuals", "paper/figures")
