import shutil
from pathlib import Path
from backends.imagemagick import imagemagick_render_image
from config import IMAGE_CACHE


SUPPORTED_FILE_EXT = ["pdf", "djvu"]
RENDER_BACKENDS = {
    "imagemagic": {
        "available": shutil.which("magick") is not None,
        "func": imagemagick_render_image,
    }
}


def render_image(path: Path, page: int) -> Path:
    for backend, prop in RENDER_BACKENDS.items():
        if prop["available"]:
            return prop["func"](path, IMAGE_CACHE, page)
    raise Exception(
        "Cannot render image. No backend is available."
        f"Available backends: {[list(RENDER_BACKENDS.keys())]}"
    )
