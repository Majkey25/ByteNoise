# Contributing

Keep changes small and direct.

Before opening a pull request, run:

```powershell
python -m compileall -q ByteNoise.pyw src/bytenoise
ruff check .
```

For web changes, also open `docs/index.html` through a local server and verify
desktop and mobile widths.
