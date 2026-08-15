async function loadSentences() {
  const response = await fetch("sentences.txt");

  if (!response.ok) {
    throw new Error(`Could not load sentences.txt (${response.status})`);
  }

  const text = await response.text();

  return text
    .split(/\r?\n/)
    .filter(line => line.trim() !== '' && !line.trim().startsWith('#'))
    .map((line, index) => {
      const separator = line.indexOf('\t');

      if (separator === -1) {
        console.warn(`Ignoring line ${index + 1}: no TAB separator`);
        return null;
      }

      return {
        source: line.slice(separator + 1).trim(),
        learning: line.slice(0, separator).trim()
      };
    })
    .filter(Boolean);
}

const tbody = document.getElementById('sentenceTableBody');
const displaySource = document.getElementById('displaySource');
const displayLearning = document.getElementById('displayLearning');
const sourceHeader = document.getElementById('sourceHeader');
const learningHeader = document.getElementById('learningHeader');
const errorElement = document.getElementById('error');

let rows = [];

function render() {
  const showSource = displaySource.checked;
  const showLearning = displayLearning.checked;

  sourceHeader.style.display = showSource ? '' : 'none';
  learningHeader.style.display = showLearning ? '' : 'none';

  tbody.innerHTML = '';

  for (const row of rows) {
    const tr = document.createElement('tr');

    if (showSource) {
      const td = document.createElement('td');
      td.textContent = row.source;
      tr.appendChild(td);
    }

    if (showLearning) {
      const td = document.createElement('td');
      td.textContent = row.learning;
      tr.appendChild(td);
    }

    tbody.appendChild(tr);
  }
}

displaySource.addEventListener('change', render);
displayLearning.addEventListener('change', render);

loadSentences()
  .then(loadedRows => {
    rows = loadedRows;
    render();
  })
  .catch(error => {
    errorElement.textContent =
      `${error.message}. Open the page through a local web server rather than directly as file://.`;
  });
