import base64
import re
from pathlib import Path
from core.process_context import get_data_dir

VALID_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")

def embed_images_as_base64(html_content: str, image_dir: str | Path | None = None) -> str:
    """Embed only valid image files as base64 and fix incorrect 'data/' prefix."""
    resolved_dir = Path(image_dir).resolve() if image_dir else get_data_dir().resolve()
    print(f"\n🔧 Embedding images from: {resolved_dir}")

    pattern = r'<img\s+[^>]*src="([^"]+\.(?:png|jpe?g|gif|webp|svg))"'

    def replace_src(match):
        img_path = match.group(1)

        if img_path.startswith(("http://", "https://", "//", "data:image/")):
            return match.group(0)

        # Normalize path
        if img_path.startswith("data/"):
            img_path = img_path[len("data/"):]

        candidate = Path(img_path)
        if candidate.is_absolute():
            img_file = candidate
        elif img_path.startswith("processes/"):
            # Path already rooted at repo
            img_file = Path(img_path)
        else:
            img_file = resolved_dir / img_path

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
