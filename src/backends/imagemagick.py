import subprocess
from pathlib import Path
from typing import Optional


def create_imagemagick_command(
    src: Path,
    dst: Path,
    page: Optional[int] = None,
    res_ext: str = "png",
) -> (Path, str):
    """ """

    page = "" if page is None else f"[{page}]"
    fname = src.stem
    dst = dst / (fname + page + "." + res_ext)
    command = ["magick", str(src.absolute()) + page, str(dst)]

    return dst, command


def imagemagick_render_image(path: Path, dst, page: int) -> Path:
    dst, command = create_imagemagick_command(path, dst, page)
    res = subprocess.run(command)
    if res.returncode != 0:
        raise Exception(
            f"""imagemagick command failed
stdout: {res.stdout}
stderr: {res.stderr}
command: {command}""",
        )
    return dst
