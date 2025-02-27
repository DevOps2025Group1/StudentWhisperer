//Sidebar constants
const toggle_button = document.getElementById("toggle-btn")
const sidebar = document.getElementById("sidebar")
// Select DOM elements using your variable names
const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");
let userText = null;

/* CHATBOT */
// Load saved chats and theme from local storage
const loadDataFromLocalstorage = () => {
    const themeColor = localStorage.getItem("themeColor");
    document.body.classList.toggle("light-mode", themeColor === "light_mode");
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
    const defaultText = `<div class="default-text">
                            <h1>The Student Whisperer</h1>
                            <p>Start a conversation to receive your student data.<br>
                            Your chat history will be displayed here.</p>
                        </div>`;
    chatContainer.innerHTML = localStorage.getItem("all-chats") || defaultText;
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
};

// Utility function to create a chat element with given HTML content and a class (e.g., outgoing/incoming)
const createChatElement = (content, className) => {
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);
    chatDiv.innerHTML = content;
    return chatDiv;
};

// Get chat response from the Flask backend and update the incoming chat element
const getChatResponse = async (incomingChatDiv) => {
    const pElement = document.createElement("p");
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userText })
        });
        const data = await response.json();
        pElement.textContent = data.response;
    } catch (error) {
        pElement.classList.add("error");
        pElement.textContent = "Oops! Something went wrong while retrieving the response. Please try again.";
    }
    // Remove the typing animation and append the response text
    incomingChatDiv.querySelector(".typing-animation").remove();
    incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
    localStorage.setItem("all-chats", chatContainer.innerHTML);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
};

// Copy response text to clipboard
const copyResponse = (copyBtn) => {
    const responseTextElement = copyBtn.parentElement.querySelector("p");
    navigator.clipboard.writeText(responseTextElement.textContent);
    copyBtn.textContent = "done";
    setTimeout(() => copyBtn.textContent = "content_copy", 1000);
};

// Show typing animation and then request the chat response
const showTypingAnimation = () => {
    const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="static/images/chatbot.png" alt="chatbot-img">
                        <div class="typing-animation">
                            <div class="typing-dot" style="--delay: 0.2s"></div>
                            <div class="typing-dot" style="--delay: 0.3s"></div>
                            <div class="typing-dot" style="--delay: 0.4s"></div>
                        </div>
                    </div>
                    <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
                </div>`;
    const incomingChatDiv = createChatElement(html, "incoming");
    chatContainer.appendChild(incomingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    getChatResponse(incomingChatDiv);
};

// Handle outgoing chat: get user input, display it, then trigger the typing animation and backend call
const handleOutgoingChat = () => {
    userText = chatInput.value.trim();
    if (!userText) return;
    // Clear the input field and reset its height
    chatInput.value = "";
    chatInput.style.height = `${initialInputHeight}px`;
    const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="static/images/user.png" alt="user-img">
                        <p>${userText}</p>
                    </div>
                </div>`;
    const outgoingChatDiv = createChatElement(html, "outgoing");
    // Remove default text if present and append the new message
    chatContainer.querySelector(".default-text")?.remove();
    chatContainer.appendChild(outgoingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    setTimeout(showTypingAnimation, 500);
};

// Delete chat history from local storage
deleteButton.addEventListener("click", () => {
    if (confirm("Are you sure you want to delete all the chats?")) {
        localStorage.removeItem("all-chats");
        loadDataFromLocalstorage();
    }
});

// Adjust input field height dynamically based on content
const initialInputHeight = chatInput.scrollHeight;
chatInput.addEventListener("input", () => {
    chatInput.style.height = `${initialInputHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

// Send message when Enter is pressed (without Shift) in the chat input
chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleOutgoingChat();
    }
});

// Also send message when the send button is clicked
sendButton.addEventListener("click", handleOutgoingChat);

// Initialize page with stored chats and theme
loadDataFromLocalstorage();

/* Sidebar */
function toggleSidebar() {
    sidebar.classList.toggle('close');
    toggle_button.classList.toggle("rotate");
}

/* Theme */
themeButton.addEventListener("click", () => {
    document.body.classList.toggle("light-mode");
    localStorage.setItem("themeColor", themeButton.innerText);
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
});


