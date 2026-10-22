from __future__ import annotations

FIRST = 0x0100
SIZE = 256
MAX_INPUT_CHARS = 1024 * 1024
MAX_TEXT_BYTES = MAX_INPUT_CHARS
MAX_FILE_BYTES = 2 * MAX_INPUT_CHARS


def check_input(text: str) -> None:
    if len(text) > MAX_INPUT_CHARS:
        raise ValueError("Input exceeds 1,048,576 characters.")


def mask(index: int) -> int:
    return (73 * index + 41) % SIZE


def encode(text: str) -> str:
    check_input(text)
    data = text.encode("utf-8")
    if len(data) > MAX_TEXT_BYTES:
        raise ValueError("Text exceeds 1 MiB of UTF-8 data.")
    return "".join(
        chr(FIRST + (byte ^ mask(i))) for i, byte in enumerate(data)
    )


def compact(code: str) -> str:
    check_input(code)
    return "".join(code.split())


def code_blocks(code: str) -> list[str]:
    check_input(code)
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
