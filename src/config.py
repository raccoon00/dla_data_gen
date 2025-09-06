import os
from pathlib import Path


def get_env_var(var, get_path=False):
    env_var = os.getenv(var)
    if env_var is None:
        raise Exception(f"Environment variable {var} is not configured.")

    if get_path:
        path = Path(env_var)
        if not path.exists():
            raise Exception(f"Path {env_var} configured in {var} does not exists")
        return path
    else:
        return env_var


PDF_PATH = get_env_var("DLA_GEN_DOCS_PATH", get_path=True)

OUTPUT_PATH = get_env_var("DLA_GEN_OUTPUT_PATH", get_path=True)

IMAGE_CACHE: Path = OUTPUT_PATH / "cache"
IMAGE_CACHE.mkdir(exist_ok=True)

ELEMENTS_PATH: Path = OUTPUT_PATH / "elements"
ELEMENTS_PATH.mkdir(exist_ok=True)

ELEMENTS_GEN: Path = OUTPUT_PATH / "elem_gen"
ELEMENTS_GEN.mkdir(exist_ok=True)

RENDER_WIDTH = 1920
RENDER_HEIGHT = 1920
