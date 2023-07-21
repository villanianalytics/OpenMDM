const API_URL = 'http://localhost:8000';  // Update with your FastAPI application's URL
const nodesList = document.getElementById('nodesList');
const createNodeForm = document.getElementById('createNodeForm');

// Function to fetch all nodes and display them
async function fetchNodes() {
  const response = await fetch(`${API_URL}/nodes`);
  const nodes = await response.json();

  nodesList.innerHTML = '';
  for (const node of nodes) {
    const listItem = document.createElement('li');
    listItem.textContent = `ID: ${node.id}, Name: ${node.name}, Parent ID: ${node.parent_id}`;
    nodesList.appendChild(listItem);
  }
}

// Fetch nodes when the page loads
fetchNodes();

// Function to create a node when the form is submitted
createNodeForm.addEventListener('submit', async function (event) {
  event.preventDefault();

  const nodeName = document.getElementById('nodeName').value;
  const parentId = document.getElementById('parentId').value;

  const response = await fetch(`${API_URL}/node`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: nodeName,
      parent_id: parentId
    })
  });

  if (response.ok) {
    fetchNodes();
    createNodeForm.reset();
  } else {
    const errorData = await response.json();
    alert(`Error creating node: ${errorData.detail}`);
  }
});
