# Releasing

1. Update `CHANGELOG.md`.
2. Run checks:

   ```powershell
   python -m compileall -q ByteNoise.pyw src/bytenoise
   ruff check .
   python -m unittest discover -s tests -v
   node --test tests/test_web.mjs
   python -m pip install --require-hashes --only-binary=:all: -r requirements-build.txt
   python -m build --no-isolation
   ```

3. Commit changes after review.
4. Tag the release:

   ```powershell
   git tag v0.1.1
   git push origin main v0.1.1
   ```

GitHub Pages deploys from `docs/` after `main` is pushed.
