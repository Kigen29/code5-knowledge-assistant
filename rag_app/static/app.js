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
  renderList(citations, data.citations, (item) => `${item.title} (${item.heading || item.chunk_id})`);
  renderList(snippets, data.snippets, (item) => `${item.title}: ${item.snippet}`);
}

function renderList(node, rows, mapper) {
  node.classList.toggle("muted", !rows.length);
  if (!rows.length) {
    node.textContent = "None returned.";
    return;
  }
  node.innerHTML = "";
  rows.forEach((row) => {
    const div = document.createElement("div");
    div.className = "evidence-item";
    div.textContent = mapper(row);
    node.appendChild(div);
  });
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

  function renderPage() {
    const start = (page - 1) * pageSize;
    const end = start + pageSize;
    items.forEach((item, index) => {
      item.hidden = index < start || index >= end;
    });
    label.textContent = `Page ${page} of ${totalPages}`;
    prev.disabled = page === 1;
    next.disabled = page === totalPages;
  }

  prev.addEventListener("click", () => {
    page = Math.max(1, page - 1);
    renderPage();
  });
  next.addEventListener("click", () => {
    page = Math.min(totalPages, page + 1);
    renderPage();
  });
  renderPage();
});
