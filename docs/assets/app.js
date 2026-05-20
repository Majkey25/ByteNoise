const FIRST = 0x0100;
const SIZE = 256;

const input = document.querySelector("#input");
const output = document.querySelector("#output");
const status = document.querySelector("#status");

const encoder = new TextEncoder();
const decoder = new TextDecoder("utf-8", { fatal: true });

function mask(index) {
  return (73 * index + 41) % SIZE;
}

function mode() {
  return document.querySelector("input[name='mode']:checked").value;
}

function setStatus(text, failed = false) {
  status.textContent = text;
  status.dataset.failed = String(failed);
}

function encode(text) {
  return Array.from(encoder.encode(text), (byte, index) =>
    String.fromCharCode(FIRST + (byte ^ mask(index))),
  ).join("");
}

function decodeBytes(bytes) {
  return decoder.decode(Uint8Array.from(bytes));
}

function compact(code) {
  return code.replace(/\s+/gu, "");
}

function codeBlocks(code) {
  const blocks = [];
  let current = [];

  for (const line of code.split(/\r?\n/u)) {
    if (line.trim()) {
      current.push(line);
    } else if (current.length) {
      blocks.push(compact(current.join("")));
      current = [];
    }
  }

  if (current.length) {
    blocks.push(compact(current.join("")));
  }

  return blocks;
}

function decodeBlock(code) {
  const compactCode = compact(code);
  const values = Array.from(compactCode, (char) => {
    const value = char.codePointAt(0) - FIRST;
    if (value < 0 || value >= SIZE) {
      throw new Error(`Invalid ByteNoise character: ${JSON.stringify(char)}`);
    }
    return value;
  });

  try {
    return decodeBytes(values.map((value, index) => value ^ mask(index)));
  } catch (maskedError) {
    try {
      return decodeBytes(values);
    } catch {
      throw maskedError;
    }
  }
}

function decode(code) {
  const blocks = codeBlocks(code);
  if (blocks.length > 1) {
    return blocks.map(decodeBlock).join("\n\n");
  }
  return decodeBlock(code);
}

function convert() {
  try {
    output.value = mode() === "encode" ? encode(input.value) : decode(input.value);
    setStatus("Done");
  } catch (error) {
    output.value = "";
    setStatus(error.message, true);
  }
}

async function copyOutput() {
  if (!output.value) {
    setStatus("Nothing to copy", true);
    return;
  }
  await navigator.clipboard.writeText(output.value);
  setStatus("Copied");
}

function downloadOutput() {
  if (!output.value) {
    setStatus("Nothing to download", true);
    return;
  }
  const blob = new Blob([output.value], { type: "text/plain;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = mode() === "encode" ? "bytenoise.txt" : "decoded.txt";
  link.click();
  URL.revokeObjectURL(link.href);
  setStatus("Downloaded");
}

function swapText() {
  input.value = output.value;
  output.value = "";
  setStatus("Swapped");
}

function loadSample() {
  input.value = "Příliš žluťoučký kůň\nByteNoise demo 🙂";
  document.querySelector("input[value='encode']").checked = true;
  convert();
}

document.querySelector("#convert").addEventListener("click", convert);
document.querySelector("#copy").addEventListener("click", copyOutput);
document.querySelector("#download").addEventListener("click", downloadOutput);
document.querySelector("#swap").addEventListener("click", swapText);
document.querySelector("#sample").addEventListener("click", loadSample);
document.querySelector("#clear").addEventListener("click", () => {
  input.value = "";
  output.value = "";
  setStatus("Ready");
});
document.querySelector("#file").addEventListener("change", async (event) => {
  const [file] = event.target.files;
  if (!file) {
    return;
  }
  input.value = await file.text();
  setStatus("File loaded");
});

input.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    convert();
  }
});
