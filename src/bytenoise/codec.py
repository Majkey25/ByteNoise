from __future__ import annotations

FIRST = 0x0100
SIZE = 256


def mask(index: int) -> int:
    return (73 * index + 41) % SIZE


def encode(text: str) -> str:
    return "".join(
        chr(FIRST + (byte ^ mask(i))) for i, byte in enumerate(text.encode("utf-8"))
    )


def compact(code: str) -> str:
    return "".join(code.split())


def code_blocks(code: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    for line in code.splitlines():
        if line.strip():
            current.append(line)
        elif current:
            blocks.append(compact("".join(current)))
            current = []
    if current:
        blocks.append(compact("".join(current)))
    return blocks


def decode_block(code: str) -> str:
    values: list[int] = []
    for char in compact(code):
        value = ord(char) - FIRST
        if not 0 <= value < SIZE:
            raise ValueError(f"Invalid ByteNoise character: {char!r}")
        values.append(value)

    try:
        return bytes(value ^ mask(i) for i, value in enumerate(values)).decode("utf-8")
    except UnicodeDecodeError as masked_error:
        try:
            return bytes(values).decode("utf-8")
        except UnicodeDecodeError:
            raise masked_error from None


def decode(code: str) -> str:
    blocks = code_blocks(code)
    if len(blocks) > 1:
        return "\n\n".join(decode_block(block) for block in blocks)
    return decode_block(code)
