# ByteNoise

ByteNoise is a tiny reversible text obfuscator with a simple desktop UI.

It is not secure encryption. It converts UTF-8 bytes with a fixed XOR mask and
stores the result as Unicode characters. Use it when you want text to stop
looking like plain text, not for secrets.

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

- Encode typed text to ByteNoise.
- Decode ByteNoise back to plain text.
- Decode older direct-offset ByteNoise text.
- Ignore pasted spaces and line breaks while decoding.
- Open a UTF-8 text file through a file picker.
- Save the converted result.
- No third-party runtime dependencies.

## Development

```powershell
python -m compileall -q ByteNoise.pyw src/bytenoise
python -m pip install ruff
ruff check .
```

## License

MIT. See [LICENSE](LICENSE).
