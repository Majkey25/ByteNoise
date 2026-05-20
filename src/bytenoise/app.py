from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from bytenoise.codec import decode, encode


def main() -> None:
    root = tk.Tk()
    root.title("ByteNoise")
    root.geometry("760x520")

    mode = tk.StringVar(value="encode")
    source = tk.Text(root, height=11, wrap="word")
    result = tk.Text(root, height=11, wrap="word")

    def source_text() -> str:
        return source.get("1.0", "end-1c")

    def result_text() -> str:
        return result.get("1.0", "end-1c")

    def show(text: str) -> None:
        result.delete("1.0", "end")
        result.insert("1.0", text)

    def convert() -> None:
        try:
            text = source_text()
            show(encode(text) if mode.get() == "encode" else decode(text))
        except (UnicodeError, ValueError) as exc:
            messagebox.showerror("Error", str(exc))

    def open_file() -> None:
        path = filedialog.askopenfilename(title="Open text file")
        if path:
            try:
                source.delete("1.0", "end")
                source.insert("1.0", Path(path).read_text(encoding="utf-8"))
            except (OSError, UnicodeError) as exc:
                messagebox.showerror("Read error", str(exc))

    def save_file() -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".txt", title="Save result"
        )
        if path:
            try:
                Path(path).write_text(result_text(), encoding="utf-8")
            except OSError as exc:
                messagebox.showerror("Write error", str(exc))

    def clear() -> None:
        source.delete("1.0", "end")
        show("")

    toolbar = tk.Frame(root)
    tk.Radiobutton(
        toolbar, text="Text to ByteNoise", variable=mode, value="encode"
    ).pack(side="left")
    tk.Radiobutton(
        toolbar, text="ByteNoise to text", variable=mode, value="decode"
    ).pack(side="left")
    tk.Button(toolbar, text="Open file", command=open_file).pack(side="left", padx=8)
    tk.Button(toolbar, text="Convert", command=convert).pack(side="left")
    tk.Button(toolbar, text="Save result", command=save_file).pack(side="left", padx=8)
    tk.Button(toolbar, text="Clear", command=clear).pack(side="left")
    toolbar.pack(fill="x", padx=8, pady=8)

    tk.Label(root, text="Input").pack(anchor="w", padx=8)
    source.pack(fill="both", expand=True, padx=8)
    tk.Label(root, text="Output").pack(anchor="w", padx=8, pady=(8, 0))
    result.pack(fill="both", expand=True, padx=8, pady=(0, 8))
    root.mainloop()
