import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import vm from "node:vm";

const script = await readFile(new URL("../docs/assets/app.js", import.meta.url), "utf8");

function app() {
  const elements = new Map();
  const document = {
    querySelector(selector) {
      if (!elements.has(selector)) {
        elements.set(selector, {
          value: selector.includes(":checked") ? "encode" : "",
          dataset: {},
          handlers: {},
          addEventListener(event, callback) { this.handlers[event] = callback; },
        });
      }
      return elements.get(selector);
    },
    querySelectorAll() { return []; },
  };
  const context = vm.createContext({ document, TextEncoder, TextDecoder });
  vm.runInContext(script, context);
  return { document, ...vm.runInContext("({ encode, decode, convert })", context) };
}

test("maximum ASCII and UTF-8 output can be loaded and decoded", async () => {
  const { document, encode, decode } = app();
  for (const text of ["a".repeat(1024 * 1024), "🙂".repeat(256 * 1024)]) {
    const encoded = encode(text);
    const file = new File([encoded], "encoded.txt");
    assert.equal(file.size, 2 * 1024 * 1024);
    await document.querySelector("#file").handlers.change({ target: { files: [file] } });
    assert.equal(decode(document.querySelector("#input").value), text);
  }
});

test("raw input and UTF-8 byte limits reject oversized conversion", () => {
  const { encode, decode } = app();
  assert.throws(() => encode("a".repeat(1024 * 1024 + 1)), /characters/);
  assert.throws(() => encode("🙂".repeat(256 * 1024 + 1)), /UTF-8/);
  assert.throws(() => decode(" ".repeat(1024 * 1024 + 1)), /characters/);
  const text = "Příliš žluťoučký kůň 🙂";
  assert.equal(decode(`\n${encode(text)}\n\n${encode("second")}\n`), `${text}\n\nsecond`);
});

test("oversized and unreadable files preserve input; oversized files are not read", async () => {
  const { document } = app();
  const input = document.querySelector("#input");
  input.value = "keep this text";
  const load = document.querySelector("#file").handlers.change;
  let reads = 0;
  await load({ target: { files: [{
    size: 2 * 1024 * 1024 + 1,
    text() { reads++; throw new Error("must not read"); },
  }] } });
  assert.equal(reads, 0);
  assert.match(document.querySelector("#status").textContent, /2 MiB/);
  await load({ target: { files: [{ size: 1, async text() { throw new Error("read failed"); } }] } });
  assert.equal(document.querySelector("#status").textContent, "read failed");
  await load({ target: { files: [new File([" ".repeat(1024 * 1024 + 1)], "large.txt")] } });
  assert.match(document.querySelector("#status").textContent, /characters/);
  assert.equal(input.value, "keep this text");
});
