/*
 * Bilingual TSV reader.
 *
 * Usage: bilingual-text.html?file=path/to/text.tsv
 * The value can be relative to the viewer page or an absolute URL.
 */
(function () {
  "use strict";

  const params = new URLSearchParams(window.location.search);
  const file = params.get("file") || params.get("tsv") || params.get("src");
  const root = document.createElement("main");
  const popup = document.createElement("section");
  let activeSentence = null;

  document.title = "Bilingual text";
  root.className = "bilingual-text";
  root.setAttribute("aria-live", "polite");
  popup.className = "bilingual-popup";
  popup.hidden = true;
  popup.setAttribute("role", "dialog");
  popup.setAttribute("aria-modal", "false");
  popup.setAttribute("aria-label", "Translation");

  document.body.append(root, popup);

  function message(text, className) {
    root.replaceChildren();
    const paragraph = document.createElement("p");
    paragraph.className = className;
    paragraph.textContent = text;
    root.append(paragraph);
  }

  function closePopup() {
    if (activeSentence) activeSentence.classList.remove("is-active");
    activeSentence = null;
    popup.hidden = true;
    popup.replaceChildren();
  }

  function positionPopup(button) {
    const gap = 10;
    const margin = 12;
    const sentence = button.getBoundingClientRect();
    const width = popup.offsetWidth;
    const height = popup.offsetHeight;
    const left = Math.max(margin, Math.min(
      sentence.left + (sentence.width / 2) - (width / 2),
      window.innerWidth - width - margin,
    ));
    const below = sentence.bottom + gap;
    const top = below + height <= window.innerHeight - margin
      ? below
      : Math.max(margin, sentence.top - height - gap);

    popup.style.left = `${left}px`;
    popup.style.top = `${top}px`;
  }

  function showTranslation(button, rows, index) {
    closePopup();
    activeSentence = button;
    button.classList.add("is-active");

    const close = document.createElement("button");
    close.type = "button";
    close.className = "close";
    close.setAttribute("aria-label", "Close translation");
    close.textContent = "×";
    close.addEventListener("click", closePopup);
    const navigation = document.createElement("div");
    navigation.className = "navigation";
    const previous = document.createElement("button");
    previous.type = "button";
    previous.textContent = "↑";
    previous.disabled = index === 0;
    previous.setAttribute("aria-label", "Show translation from previous TSV line");
    previous.addEventListener("click", (event) => {
      event.stopPropagation();
      showTranslation(button, rows, index - 1);
    });
    const next = document.createElement("button");
    next.type = "button";
    next.textContent = "↓";
    next.disabled = index === rows.length - 1;
    next.setAttribute("aria-label", "Show translation from next TSV line");
    next.addEventListener("click", (event) => {
      event.stopPropagation();
      showTranslation(button, rows, index + 1);
    });
    navigation.append(previous, next);
    const translated = document.createElement("div");
    translated.className = "translation";
    translated.setAttribute("aria-live", "polite");
    translated.textContent = rows[index].translation || "—";
    popup.replaceChildren(close, navigation, translated);
    popup.hidden = false;
    positionPopup(button);
  }

  function makeSentence(source, rows, index) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "bilingual-sentence";
    button.textContent = source;
    button.setAttribute("aria-haspopup", "dialog");
    button.setAttribute("aria-label", `Show translation: ${source}`);
    button.addEventListener("click", () => showTranslation(button, rows, index));
    return button;
  }

  function parseTsv(text) {
    return text.replace(/^\uFEFF/, "").split(/\r?\n/).reduce((rows, line, index) => {
      if (!line.trim() || line.trimStart().startsWith("#")) return rows;
      const columns = line.split("\t");
      if (columns.length < 2) {
        rows.invalid.push(index + 1);
      } else {
        rows.valid.push({ source: columns[0], translation: columns[1] });
      }
      return rows;
    }, { valid: [], invalid: [] });
  }

  function render(text, fileUrl) {
    const { valid, invalid } = parseTsv(text);
    if (!valid.length) {
      message("The TSV contains no valid source/translation rows.", "error");
      return;
    }
    root.replaceChildren();
    const heading = document.createElement("h1");
    heading.textContent = decodeURIComponent(fileUrl.pathname.split("/").pop() || "Bilingual text");
    const hint = document.createElement("p");
    hint.className = "hint";
    hint.textContent = "Click or tap a sentence to show its translation. Press Escape to close it.";
    const textBlock = document.createElement("article");
    textBlock.lang = params.get("lang") || "";
    valid.forEach((row, index) => textBlock.append(makeSentence(row.source, valid, index)));
    root.append(heading, hint, textBlock);
    if (invalid.length) {
      const warning = document.createElement("p");
      warning.className = "error";
      warning.textContent = `Skipped malformed line${invalid.length === 1 ? "" : "s"}: ${invalid.join(", ")}.`;
      root.append(warning);
    }
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closePopup();
  });
  document.addEventListener("click", (event) => {
    if (!popup.hidden && !popup.contains(event.target) && !event.target.closest(".bilingual-sentence")) closePopup();
  });
  window.addEventListener("resize", () => {
    if (activeSentence) positionPopup(activeSentence);
  });

  if (!file) {
    message("Add a TSV file in the URL, for example: ?file=example.tsv", "error");
    return;
  }

  let fileUrl;
  try {
    fileUrl = new URL(file, window.location.href);
  } catch (_) {
    message("The TSV file URL is invalid.", "error");
    return;
  }
  fetch(fileUrl)
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.text();
    })
    .then((text) => render(text, fileUrl))
    .catch((error) => message(`Could not load the TSV file (${error.message}).`, "error"));
}());
