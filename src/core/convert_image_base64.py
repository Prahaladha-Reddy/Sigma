import base64
import re
from pathlib import Path

VALID_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")

def embed_images_as_base64(html_content: str, image_dir: str="data") -> str:
    """Embed only valid image files as base64 and fix incorrect 'data/' prefix."""
    image_dir = Path(image_dir).resolve()
    print(f"\n🔧 Embedding images from: {image_dir}")

    pattern = r'<img\s+[^>]*src="([^"]+\.(?:png|jpe?g|gif|webp|svg))"'

    def replace_src(match):
        img_path = match.group(1)

        if img_path.startswith(("http://", "https://", "//", "data:image/")):
            return match.group(0)

        if img_path.startswith("data/"):
            img_path = img_path[len("data/"):] 

        img_file = image_dir / img_path

        if not img_file.exists():
            print(f"image not found: {img_file}")
            return match.group(0)

        ext = img_file.suffix.lower()
        if ext == ".png":
            mime = "image/png"
        elif ext in (".jpg", ".jpeg"):
            mime = "image/jpeg"
        elif ext == ".gif":
            mime = "image/gif"
        elif ext == ".webp":
            mime = "image/webp"
        elif ext == ".svg":
            mime = "image/svg+xml"
        else:
            return match.group(0)  

        with open(img_file, "rb") as img:
            b64 = base64.b64encode(img.read()).decode("utf-8")

        return match.group(0).replace(
            match.group(1), f"data:{mime};base64,{b64}"
        )

    return re.sub(pattern, replace_src, html_content, flags=re.IGNORECASE)
