from __future__ import annotations

import sys

from bytenoise.app import main as run_app
from bytenoise.codec import decode, encode


def smoke_test() -> None:
    text = "ByteNoise smoke Příliš žluťoučký kůň"
    if decode(encode(text)) != text:
        raise SystemExit("ByteNoise smoke test failed")
    print("ByteNoise smoke test passed")


def main() -> None:
    if sys.argv[1:] == ["--self-test"]:
        smoke_test()
        return
    run_app()


if __name__ == "__main__":
    main()
