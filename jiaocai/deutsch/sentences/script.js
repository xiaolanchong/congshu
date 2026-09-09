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

      // Tag/source line.
      if (line.startsWith("@")) {
        const rawText = line.slice(1).trim();
        const resetSentenceNumber = rawText.startsWith("!");
        const text = resetSentenceNumber ? rawText.slice(1).trim() : rawText;

        return {
          type: "tag",
          text,
          resetSentenceNumber
        };
      }

      const separator = line.indexOf("\t");

      if (separator === -1) {
        console.warn(`Ignoring line ${index + 1}: no TAB separator`);
        return null;
      }

      return {
        type: "sentence",
        learning: line.slice(0, separator).trim(),
        source: line.slice(separator + 1).trim()
      };
    })
    .filter(Boolean);
}

const tbody = document.getElementById("sentenceTableBody");
const displaySource = document.getElementById("displaySource");
const displayLearning = document.getElementById("displayLearning");
const errorElement = document.getElementById("error");

let rows = [];

function render() {
  tbody.innerHTML = "";

  let sentenceNumber = 0;
  let resetSentenceNumber = false;

  rows.forEach(row => {
    // @tag line
    if (row.type === "tag") {
      const tr = document.createElement("tr");
      tr.className = "sentence-tag";

      const td = document.createElement("td");

      // Table has 3 columns: number + source + learning.
      td.colSpan = 3;
      td.textContent = row.text;

      tr.appendChild(td);
      tbody.appendChild(tr);

      resetSentenceNumber = !!row.resetSentenceNumber;
      return;
    }

    if (resetSentenceNumber) {
      sentenceNumber = 0;
      resetSentenceNumber = false;
    }

    // Sentence
    sentenceNumber++;

    const tr = document.createElement("tr");

    // Number
    const number = document.createElement("td");
    number.className = "number";
    number.textContent = sentenceNumber;
    tr.appendChild(number);

    // Learning
    const learning = document.createElement("td");
    learning.textContent = row.learning;
    
    learning.style.visibility =
      displayLearning.checked ? "visible" : "hidden";
    tr.appendChild(learning);

    // Source
    const source = document.createElement("td");
    source.textContent = row.source;

    source.style.visibility =
      displaySource.checked ? "visible" : "hidden";
    tr.appendChild(source);

    tbody.appendChild(tr);
  });
}

displaySource.addEventListener("change", render);
displayLearning.addEventListener("change", render);

loadSentences()
  .then(loadedRows => {
    rows = loadedRows;
    render();
  })
  .catch(error => {
    errorElement.textContent =
      `${error.message}. Open the page through a local web server rather than directly as file://.`;
  });