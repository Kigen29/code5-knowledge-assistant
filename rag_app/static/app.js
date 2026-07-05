const form = document.querySelector("#chatForm");
const question = document.querySelector("#question");
const answer = document.querySelector("#answer");
const latency = document.querySelector("#latency");
const citations = document.querySelector("#citations");
const snippets = document.querySelector("#snippets");
const healthLabel = document.querySelector("#healthLabel");

async function askPolicy(text) {
  answer.textContent = "Thinking...";
  latency.textContent = "Running retrieval";
  citations.textContent = "";
  snippets.textContent = "";
  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: text }),
  });
  const data = await response.json();
  answer.textContent = data.answer;
  latency.textContent = `${data.latency_ms} ms`;
  renderCitations(data.citations || []);
  renderSnippets(data.snippets || []);
}

function setEmpty(node, message) {
  node.classList.add("muted");
  node.textContent = message;
}

function renderCitations(rows) {
  citations.classList.toggle("muted", !rows.length);
  if (!rows.length) {
    setEmpty(citations, "No citations returned for this answer.");
    return;
  }
  citations.innerHTML = "";
  rows.forEach((row) => {
    const div = document.createElement("div");
    div.className = "evidence-item citation-card";
    div.innerHTML = `
      <div class="evidence-kicker">
        <span>${escapeHtml(row.relevance || "retrieved")}</span>
        <code>${escapeHtml(row.chunk_id || "")}</code>
      </div>
      <strong>${escapeHtml(row.title || "Untitled source")}</strong>
      <p>${escapeHtml(row.heading || "General")}</p>
      <small>${escapeHtml(row.source_path || "")}</small>
    `;
    citations.appendChild(div);
  });
}

function renderSnippets(rows) {
  snippets.classList.toggle("muted", !rows.length);
  if (!rows.length) {
    setEmpty(snippets, "No retrieved snippets to show.");
    return;
  }
  snippets.innerHTML = "";
  rows.forEach((row) => {
    const div = document.createElement("div");
    div.className = "evidence-item snippet-card";
    div.innerHTML = `
      <div class="evidence-kicker">
        <span>${escapeHtml(row.title || "Untitled source")}</span>
        <code>${escapeHtml(row.chunk_id || "")}</code>
      </div>
      <p>${escapeHtml(row.snippet || "")}</p>
    `;
    snippets.appendChild(div);
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

if (form) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const text = question.value.trim();
    if (text) askPolicy(text);
  });
}

document.querySelectorAll(".prompt").forEach((button) => {
  button.addEventListener("click", () => {
    question.value = button.dataset.question;
    askPolicy(button.dataset.question);
  });
});

fetch("/health")
  .then((response) => response.json())
  .then((data) => {
    if (healthLabel) healthLabel.textContent = data.status;
  })
  .catch(() => {
    if (healthLabel) healthLabel.textContent = "offline";
  });

document.querySelectorAll(".paginated-list").forEach((list) => {
  const items = Array.from(list.querySelectorAll(".paginated-item"));
  const pageSize = Number(list.dataset.pageSize || 8);
  const controls = list.nextElementSibling?.classList.contains("pagination")
    ? list.nextElementSibling
    : null;
  if (!controls || items.length <= pageSize) {
    if (controls) controls.hidden = items.length <= pageSize;
    return;
  }

  let page = 1;
  const totalPages = Math.ceil(items.length / pageSize);
  const label = controls.querySelector("[data-page-label]");
  const prev = controls.querySelector("[data-page-action='prev']");
  const next = controls.querySelector("[data-page-action='next']");
  const pageButtons = document.createElement("div");
  pageButtons.className = "page-numbers";
  label.insertAdjacentElement("afterend", pageButtons);

  function renderPage() {
    const start = (page - 1) * pageSize;
    const end = start + pageSize;
    items.forEach((item, index) => {
      item.classList.toggle("is-hidden", index < start || index >= end);
    });
    label.textContent = `Page ${page} of ${totalPages}`;
    prev.disabled = page === 1;
    next.disabled = page === totalPages;
    pageButtons.innerHTML = "";
    for (let index = 1; index <= totalPages; index += 1) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = index === page ? "page-number active" : "page-number";
      button.textContent = index;
      button.setAttribute("aria-label", `Go to page ${index}`);
      button.addEventListener("click", () => {
        page = index;
        renderPage();
        list.scrollIntoView({ behavior: "smooth", block: "start" });
      });
      pageButtons.appendChild(button);
    }
  }

  prev.addEventListener("click", () => {
    page = Math.max(1, page - 1);
    renderPage();
    list.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  next.addEventListener("click", () => {
    page = Math.min(totalPages, page + 1);
    renderPage();
    list.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  renderPage();
});
