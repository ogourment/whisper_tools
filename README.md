# Whisper AI Subtitle Transformer

This project provides a small Python library to **transform raw Whisper subtitle text** into a more readable format, grouped by minutes.

## Features

- Converts Whisper output into timestamped paragraphs:
  ```
  [00]
  Bienvenue dans ce podcast…

  [01]
  Nous allons parler de…
  ```
- Simple Python API (`transform_subtitles`).
- Tested with `pytest`.
- Easy setup with `make`.

---

## Setup

Clone the repository and run:

```bash
make venv
make install
```

This will create a virtual environment in `.venv/` and install dependencies.

To run tests:

```bash
make test
```

---

## Usage

You can use the transformer either from Python or the CLI.

### From Python

```python
from subtitle_transformer import transform_subtitles

raw_subs = """[00:00.000 --> 00:04.000] Bienvenue dans ce podcast...
[00:04.000 --> 00:08.000] Aujourd'hui nous allons parler..."""

print(transform_subtitles(raw_subs))
```

Output:

```
[00]
Bienvenue dans ce podcast... Aujourd'hui nous allons parler...
```

### From CLI

After installing in editable mode (`make install`), you can run:

```bash
python -m subtitle_transformer input.srt > output.txt
```
