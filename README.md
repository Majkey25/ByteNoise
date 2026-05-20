# ByteNoise

[![CI](https://github.com/Majkey25/ByteNoise/actions/workflows/ci.yml/badge.svg)](https://github.com/Majkey25/ByteNoise/actions/workflows/ci.yml)
[![Pages](https://github.com/Majkey25/ByteNoise/actions/workflows/pages.yml/badge.svg)](https://github.com/Majkey25/ByteNoise/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-0f7a5f.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776ab.svg)](pyproject.toml)

ByteNoise is a tiny reversible text obfuscator with a simple desktop UI.

It is not secure encryption. It converts UTF-8 bytes with a fixed XOR mask and
stores the result as Unicode characters. Use it when you want text to stop
looking like plain text, not for secrets.

## Web App

GitHub Pages version:

```text
https://majkey25.github.io/ByteNoise/
```

The web app is static HTML/CSS/JavaScript in [`docs/`](docs/). It has no build
step and no runtime dependencies.

## Run

Double-click:

```text
ByteNoise.pyw
```

Or run from a terminal:

```powershell
python ByteNoise.pyw
```

Or as a package:

```powershell
python -m pip install -e .
python -m bytenoise
```

## Features

- Desktop app with a minimal Tkinter UI.
- Browser app for GitHub Pages.
- Encode typed text to ByteNoise.
- Decode ByteNoise back to plain text.
- Decode older direct-offset ByteNoise text.
- Ignore pasted spaces and line breaks while decoding.
- Open a UTF-8 text file through a file picker.
- Save or copy converted output.
- No third-party runtime dependencies.

## How It Works

ByteNoise encodes text as UTF-8 bytes, XORs each byte with a deterministic mask,
then stores each result as a Unicode character starting at `0x0100`.

```text
encoded_char = chr(0x0100 + (byte ^ ((73 * index + 41) % 256)))
```

Decoding validates the characters, reverses the XOR mask, and decodes the bytes
as UTF-8. If masked decoding fails, ByteNoise tries the older direct-offset
format for backward compatibility.

## Repository Layout

```text
.
├── ByteNoise.pyw              # Windows double-click launcher
├── docs/                      # GitHub Pages web app
├── src/bytenoise/             # Desktop app package
├── .github/workflows/         # CI and Pages deployment
├── README.md
├── LICENSE
└── pyproject.toml
```

## GitHub Pages

This repository includes a Pages workflow at
[`.github/workflows/pages.yml`](.github/workflows/pages.yml). After pushing to
`main`, enable Pages in the repository settings with **Source: GitHub Actions**.

Recommended repository metadata:

- Description: `Tiny reversible text obfuscator for desktop and browser.`
- Website: `https://majkey25.github.io/ByteNoise/`
- Topics: `python`, `tkinter`, `javascript`, `github-pages`,
  `text-obfuscation`

## Development

```powershell
python -m compileall -q ByteNoise.pyw src/bytenoise
python -m pip install ruff
ruff check .
python -m unittest discover -s tests -v
python -m pip install build
python -m build
```

Check the static web app locally:

```powershell
python -m http.server 8765 --directory docs
```

## License

MIT. See [LICENSE](LICENSE).
