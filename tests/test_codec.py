from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bytenoise.app import read_input_file
from bytenoise.codec import (
    MAX_FILE_BYTES,
    MAX_INPUT_CHARS,
    MAX_TEXT_BYTES,
    decode,
    encode,
)

LEGACY_DIRECT = (
    "ŉĠţšŮŮůŴĠŤťţůŤťĠŴŨũųĠũŮŴůĠŲťšŤšŢŬťĠŕŔņĭĸĮĠŃůŮŶťŲŴũŮŧĠ"
    "ťšţŨĠţŨšŲšţŴťŲĠŴůĠŢŹŴťĠĽĠţůŤťŰůũŮŴĠĭĠĲĵĶĠŰŲůŤŵţťųĠ"
    "ũŮŶšŬũŤĠŕŔņĭĸĬĠųůĠŉĠŮťťŤĠŴŨťĠťŸšţŴĠţůŮŶťŲųũůŮįūťŹĮ"
)


class CodecTest(unittest.TestCase):
    def test_round_trip_ascii(self) -> None:
        self.assertEqual(decode(encode("hello")), "hello")

    def test_round_trip_utf8(self) -> None:
        text = "Příliš žluťoučký kůň\nByteNoise demo 🙂"
        self.assertEqual(decode(encode(text)), text)

    def test_decode_ignores_pasted_whitespace(self) -> None:
        code = encode("hello")
        self.assertEqual(decode(f"\n\t{code}\n\n"), "hello")

    def test_decode_multiple_pasted_blocks(self) -> None:
        code = f"{encode('first block')}\n\n{encode('second block')}"
        self.assertEqual(decode(code), "first block\n\nsecond block")

    def test_decode_legacy_direct_offset(self) -> None:
        self.assertTrue(
            decode(f"{LEGACY_DIRECT}\n\n").startswith(
                "I cannot decode this into readable UTF-8."
            )
        )

    def test_decode_rejects_plain_text(self) -> None:
        with self.assertRaises(ValueError):
            decode("plain text")

    def test_maximum_outputs_can_be_loaded_and_decoded(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "encoded.txt"
            for text in ("a" * MAX_TEXT_BYTES, "🙂" * (MAX_TEXT_BYTES // 4)):
                with self.subTest(first_character=text[0]):
                    code = encode(text)
                    path.write_text(code, encoding="utf-8")
                    self.assertEqual(path.stat().st_size, MAX_FILE_BYTES)
                    self.assertEqual(decode(read_input_file(path)), text)

    def test_oversized_input_is_rejected_before_whitespace_removal(self) -> None:
        with self.assertRaisesRegex(ValueError, "characters"):
            decode(" " * (MAX_INPUT_CHARS + 1))
        with self.assertRaisesRegex(ValueError, "characters"):
            encode("a" * (MAX_INPUT_CHARS + 1))
        with self.assertRaisesRegex(ValueError, "UTF-8"):
            encode("🙂" * (MAX_TEXT_BYTES // 4 + 1))

    def test_file_limits_and_utf8_newlines(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "input.txt"
            path.write_bytes(b"x" * (MAX_FILE_BYTES + 1))
            with self.assertRaisesRegex(ValueError, "2 MiB"):
                read_input_file(path)
            path.write_bytes(b" " * (MAX_INPUT_CHARS + 1))
            with self.assertRaisesRegex(ValueError, "characters"):
                read_input_file(path)
            path.write_bytes("Příliš\r\nžluťoučký\rkůň".encode())
            self.assertEqual(read_input_file(path), "Příliš\nžluťoučký\nkůň")
            path.write_bytes(b"\xff")
            with self.assertRaises(UnicodeDecodeError):
                read_input_file(path)


if __name__ == "__main__":
    unittest.main()
