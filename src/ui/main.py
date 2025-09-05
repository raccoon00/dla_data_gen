from PIL import Image
from typing import Optional
from pathlib import Path
from nicegui import ui, app
from nicegui.events import MouseEventArguments, KeyEventArguments

from backends.doc_ops import render_image, SUPPORTED_FILE_EXT
from config import PDF_PATH, RENDER_HEIGHT, RENDER_WIDTH


class State:
    def __init__(self):
        self._doc_path: Path = None

        self._cur_image: Path = None
        self._cur_url: str = None
        self._cur_size: tuple[int, int] = None

        self._image: ui.interactive_image = None
        self._image_pos: tuple[float, float] = None
        self._image_zoom: float = None

    def set_interactive_image(self, image):
        self._image = image

    @property
    def doc_path(self):
        return self._doc_path

    @doc_path.setter
    def doc_path(self, doc: str):
        self._doc_path = Path(doc)

    @property
    def doc_exists(self):
        if self._doc_path:
            return self._doc_path.exists()
        return False

    def load(self) -> None:
        self._cur_image = render_image(state.doc_path, 0)
        if not self.is_loaded():
            raise Exception("Unknown error while loading image")
        self._cur_size = self.get_image_size()
        self.add_image()

    def is_loaded(self) -> bool:
        return self._cur_image is not None and self._cur_image.exists()

    def get_image_path(self) -> Optional[Path]:
        return self._cur_image

    def get_image_size(self) -> tuple[int, int]:
        if not self.is_loaded():
            raise Exception("Tried to get the size of unloaded image.")
        img = Image.open(self._cur_image)
        size = img.size
        img.close()
        return size

    def add_image(self) -> None:
        if not self.is_loaded():
            return

        self._cur_url = f"/tmp/{self._cur_image.name}"
        app.add_media_file(local_file=self._cur_image, url_path=self._cur_url)

        self.fit_image()

    def fit_image(self, margin=0.9):
        width, height = self._cur_size
        if width / RENDER_WIDTH < height / RENDER_HEIGHT:
            zoom = RENDER_HEIGHT / height
        else:
            zoom = RENDER_WIDTH / width

        self.pos_image(0.5, 0.5, zoom * margin)

    def pos_image(self, center_x: float, center_y: float, zoom: float):
        if self._image is None:
            raise Exception("Interactive image is not set in state.")

        self._image_pos = (center_x, center_y)
        self._image_zoom = zoom

        x, y, width, height = self._get_x_y_width_height()

        self._image.content = f"<image href='{self._cur_url}' x='{x}' y='{y}' width='{width}' height='{height}' />"

    def _get_x_y_width_height(self):
        width, height = self._cur_size
        width *= self._image_zoom
        height *= self._image_zoom

        center_x, center_y = self._image_pos

        x = RENDER_WIDTH * center_x - width * 0.5
        y = RENDER_HEIGHT * center_y - height * 0.5

        return x, y, width, height

    def move_image(self, *, dx=0, dy=0, rel_zoom=1.0):
        x, y = self._image_pos
        self.pos_image(x + dx, y + dy, self._image_zoom * rel_zoom)

    def get_rel_image_coord(self, x: int, y: int) -> tuple[float, float]:
        if self.is_loaded():
            img_x, img_y, width, height = self._get_x_y_width_height()
            return (x - img_x) / width, (y - img_y) / height

        return None, None


state = State()


def handle_key(e: KeyEventArguments):
    if e.key == "w" and e.action.keydown:
        state.move_image(dy=-0.05)
    if e.key == "s" and e.action.keydown:
        state.move_image(dy=0.05)
    if e.key == "a" and e.action.keydown:
        state.move_image(dx=-0.05)
    if e.key == "d" and e.action.keydown:
        state.move_image(dx=0.05)
    if e.key == "=" and e.action.keydown:
        state.move_image(rel_zoom=1.1)
    if e.key == "-" and e.action.keydown:
        state.move_image(rel_zoom=0.9)


def mouse_handler(event: MouseEventArguments):
    print(state.get_rel_image_coord(event.image_x, event.image_y))


@ui.page("/")
def main_page() -> None:
    container = ui.column()
    ui.keyboard(on_key=handle_key)

    with container:
        load_row = ui.row()

        with load_row:
            ui.select(
                book_names,
                label="document",
                with_input=True,
            ).bind_value(state, "doc_path")
            state.doc_path = book_names.keys().__iter__().__next__()

            ui.button("Load", on_click=lambda x: state.load()).bind_enabled(
                state, "doc_exists"
            )

        image = ui.interactive_image(
            size=(RENDER_WIDTH, RENDER_HEIGHT),
            cross=True,
            on_mouse=mouse_handler,
        ).classes("w-[500px] bg-gray-500")
        state.set_interactive_image(image)

    state.load()


if __name__ in ["__main__", "__mp_main__"]:
    book_file_list = []
    for ext in SUPPORTED_FILE_EXT:
        book_file_list += list(PDF_PATH.glob(f"*.{ext}"))
    book_names = {p: p.name for p in book_file_list}

    ui.run()
