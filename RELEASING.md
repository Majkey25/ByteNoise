# Releasing

1. Update `CHANGELOG.md`.
2. Run checks:

   ```powershell
   python -m compileall -q ByteNoise.pyw src/bytenoise
   ruff check .
   python -m unittest discover -s tests -v
   python -m build
   ```

3. Commit changes after review.
4. Tag the release:

   ```powershell
   git tag v0.1.0
   git push origin main v0.1.0
   ```

GitHub Pages deploys from `docs/` after `main` is pushed.
