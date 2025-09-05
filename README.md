# UI for creating elements for dataset synthesis

## Config:

Set documents (pdf or djvu) path and the resulting elements path in `.env`

```sh
CHESS_BOOKS_PATH=/path/to/books
IMAGE_OUTPUT_PATH=/path/to/repo/preprocess/dla_dataset/elements
```

## Run:

```sh
uv sync
uv run --env-file .env src/main.py
```

