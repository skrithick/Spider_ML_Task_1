let state = {
  isLoading: false
}

console.log("Hi");

function toggleLoader() {
  const loader = document.getElementById('loader');
  loader.classList.toggle('hidden');
}

function toggleButton() {
  const btn = document.getElementById('btn');
  btn.toggleAttribute('disabled');
}

toggleLoader();

function clearAnswer() {
  const answer = document.getElementById('answer');
  answer.innerHTML = '';
}

function setAnswer(content) {
  const answer = document.getElementById('answer');
  answer.innerHTML = content;
}

async function fetchAnswer(query) {
  // todo: fetch answer to query
  const response = await fetch(`http://127.0.0.1:8000/query?query_content=${query}`);
  const data = await response.json();
  return data['data'];
}

async function handleSubmit(e) {
  e.preventDefault();
  const data = new FormData(e.target);
  const query = data.get('chat-input');
  clearAnswer();
  toggleLoader();
  toggleButton();
  const res = await fetchAnswer(query);
  toggleButton();
  toggleLoader();
  setAnswer(res);
}

document.getElementById('chat').addEventListener('submit', e => handleSubmit(e))