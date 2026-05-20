from __future__ import annotations

import unittest

from bytenoise.codec import decode, encode

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

    def test_decode_legacy_direct_offset(self) -> None:
        self.assertTrue(
            decode(f"{LEGACY_DIRECT}\n\n").startswith(
                "I cannot decode this into readable UTF-8."
            )
        )

    def test_decode_rejects_plain_text(self) -> None:
        with self.assertRaises(ValueError):
            decode("plain text")


if __name__ == "__main__":
    unittest.main()
