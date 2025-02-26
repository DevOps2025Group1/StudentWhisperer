document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    let inputField = document.getElementById("user-input");
    let userMessage = inputField.value.trim();
    if (userMessage === "") return;

    // Display user message
    let chatBox = document.getElementById("chat-box");
    let userDiv = document.createElement("div");
    userDiv.classList.add("user-message");
    userDiv.textContent = userMessage;
    chatBox.appendChild(userDiv);
    inputField.value = "";

    // Send message to Flask backend
    fetch("/chat", {
        method: "POST",
        body: JSON.stringify({ message: userMessage }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        let botDiv = document.createElement("div");
        botDiv.classList.add("bot-message");
        botDiv.textContent = data.response;
        chatBox.appendChild(botDiv);

        // Auto-scroll to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));
}
