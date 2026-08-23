async function loadSentences() {
  const response = await fetch("sentences.txt");

  if (!response.ok) {
    throw new Error(`Could not load sentences.txt (${response.status})`);
  }

  return (await response.text())
    .split(/\r?\n/)
    .filter(line => line.trim() !== "" && !line.trim().startsWith("#"))
    .map((line, index) => {
      line = line.trim();

      // Section/tag line.
      if (line.startsWith("@")) {
        return {
          type: "tag",
          text: line.slice(1).trim()
        };
      }

      const fields = line.split("\t").map(field => field.trim());

      if (fields.length === 0 || !fields[0]) {
        return null;
      }

      const row = {
        type: "sentence",
        chinese: fields[0],
        pinyin: "",
        source: ""
      };

      switch (fields.length) {
        case 1:
          // Chinese only.
          break;

        case 2:
          // Chinese + translation.
          row.source = fields[1];
          break;

        default:
          // Chinese + pinyin + translation.
          row.pinyin = fields[1];
          row.source = fields.slice(2).join("\t");
          break;
      }

      return row;
    })
    .filter(Boolean);
}

const tbody = document.getElementById("sentenceTableBody");

const displayChinese = document.getElementById("displayChinese");
const displayPinyin = document.getElementById("displayPinyin");
const displaySource = document.getElementById("displaySource");

const errorElement = document.getElementById("error");

let rows = [];

function render() {
  tbody.innerHTML = "";

  let sentenceNumber = 0;

  rows.forEach(row => {
    // @tag line
    if (row.type === "tag") {
      const tr = document.createElement("tr");
      tr.className = "sentence-tag";

      const td = document.createElement("td");
      td.colSpan = 4;
      td.textContent = row.text;

      tr.appendChild(td);
      tbody.appendChild(tr);

      return;
    }

    sentenceNumber++;

    const tr = document.createElement("tr");

    // Number
    const number = document.createElement("td");
    number.className = "number";
    number.textContent = sentenceNumber;
    tr.appendChild(number);

    // Chinese
    const chinese = document.createElement("td");
    chinese.textContent = row.chinese;
    chinese.style.visibility =
      displayChinese.checked ? "visible" : "hidden";
    tr.appendChild(chinese);

    // Pinyin
    const pinyin = document.createElement("td");
    pinyin.textContent = row.pinyin;
    pinyin.style.visibility =
      displayPinyin.checked && row.pinyin
        ? "visible"
        : "hidden";
    tr.appendChild(pinyin);

    // Source / translation
    const source = document.createElement("td");
    source.textContent = row.source;
    source.style.visibility =
      displaySource.checked && row.source
        ? "visible"
        : "hidden";
    tr.appendChild(source);

    tbody.appendChild(tr);
  });
}

displayChinese.addEventListener("change", render);
displayPinyin.addEventListener("change", render);
displaySource.addEventListener("change", render);

loadSentences()
  .then(loadedRows => {
    rows = loadedRows;
    render();
  })
  .catch(error => {
    errorElement.textContent =
      `${error.message}. Open the page through a local web server rather than directly as file://.`;
  });