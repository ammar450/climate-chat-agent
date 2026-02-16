const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const welcomeScreen = document.getElementById('welcomeScreen');
const chatList = document.getElementById('chatList');

// Chat Management
let currentSessionId = null;
let allChats = {};

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function loadChats() {
    const storedChats = localStorage.getItem('climate_chats');
    if (storedChats) {
        allChats = JSON.parse(storedChats);
    }

    // If no chats exist, create the first one
    if (Object.keys(allChats).length === 0) {
        createNewChat();
    } else {
        // Load the last active chat or first chat
        const lastActive = localStorage.getItem('last_active_chat');
        const chatId = lastActive && allChats[lastActive] ? lastActive : Object.keys(allChats)[0];
        loadChat(chatId);
    }
    
    renderChatList();
}

function saveChats() {
    localStorage.setItem('climate_chats', JSON.stringify(allChats));
}

function createNewChat() {
    const sessionId = generateUUID();
    const timestamp = new Date().toLocaleString();
    
    allChats[sessionId] = {
        id: sessionId,
        title: 'New Chat',
        messages: [],
        createdAt: timestamp,
        lastActive: timestamp
    };
    
    saveChats();
    loadChat(sessionId);
    renderChatList();
}

function loadChat(sessionId) {
    currentSessionId = sessionId;
    localStorage.setItem('last_active_chat', sessionId);
    
    // Update last active time
    if (allChats[sessionId]) {
        allChats[sessionId].lastActive = new Date().toLocaleString();
        saveChats();
    }

    // Clear current chat display
    chatContainer.innerHTML = '';
    
    // Load messages from this chat
    const chat = allChats[sessionId];
    if (chat && chat.messages.length > 0) {
        chat.messages.forEach(msg => {
            addMessage(msg.content, msg.role, msg.sparql, msg.technicalDetails, false);
        });
    } else {
        // Show welcome screen for empty chat
        showWelcomeScreen();
    }

    renderChatList();
}

function deleteChat(sessionId, event) {
    event.stopPropagation();
    
    if (!confirm('Delete this chat?')) {
        return;
    }

    delete allChats[sessionId];
    saveChats();

    // If we deleted the current chat, load another
    if (currentSessionId === sessionId) {
        const remainingChats = Object.keys(allChats);
        if (remainingChats.length > 0) {
            loadChat(remainingChats[0]);
        } else {
            createNewChat();
        }
    } else {
        renderChatList();
    }
}

function renderChatList() {
    chatList.innerHTML = '';
    
    // Sort chats by last active (newest first)
    const sortedChats = Object.values(allChats).sort((a, b) => {
        return new Date(b.lastActive) - new Date(a.lastActive);
    });

    sortedChats.forEach(chat => {
        const chatItem = document.createElement('div');
        chatItem.className = 'chat-item' + (chat.id === currentSessionId ? ' active' : '');
        chatItem.onclick = () => loadChat(chat.id);
        
        const titleSpan = document.createElement('span');
        titleSpan.className = 'chat-item-title';
        titleSpan.textContent = chat.title;
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-chat-button';
        deleteBtn.textContent = '🗑️';
        deleteBtn.onclick = (e) => deleteChat(chat.id, e);
        
        chatItem.appendChild(titleSpan);
        chatItem.appendChild(deleteBtn);
        chatList.appendChild(chatItem);
    });
}

function updateChatTitle(sessionId, firstMessage) {
    if (allChats[sessionId]) {
        // Use first 40 characters of first message as title
        const title = firstMessage.substring(0, 40) + (firstMessage.length > 40 ? '...' : '');
        allChats[sessionId].title = title;
        saveChats();
        renderChatList();
    }
}

function saveMessage(content, role, sparql = null, technicalDetails = null) {
    if (currentSessionId && allChats[currentSessionId]) {
        allChats[currentSessionId].messages.push({
            content,
            role,
            sparql,
            technicalDetails,
            timestamp: new Date().toISOString()
        });
        
        // Update title from first user message
        if (role === 'user' && allChats[currentSessionId].messages.filter(m => m.role === 'user').length === 1) {
            updateChatTitle(currentSessionId, content);
        }
        
        saveChats();
    }
}

function showWelcomeScreen() {
    const welcome = document.createElement('div');
    welcome.className = 'welcome-screen';
    welcome.id = 'welcomeScreen';
    welcome.innerHTML = `
        <h2>Climate Data Assistant</h2>
        <p class="welcome-subtitle">Ask me anything about climate data and observations</p>
        <div class="examples">
            <div class="example-card" onclick="sendExample('What variables are available?')">
                <div class="example-title">📊 Variables</div>
                <div class="example-text">What variables are available?</div>
            </div>
            <div class="example-card" onclick="sendExample('Show me some sample observations')">
                <div class="example-title">🔍 Sample Data</div>
                <div class="example-text">Show me some sample observations</div>
            </div>
            <div class="example-card" onclick="sendExample('What is the temperature data?')">
                <div class="example-title">🌡️ Temperature</div>
                <div class="example-text">What is the temperature data?</div>
            </div>
        </div>
    `;
    chatContainer.appendChild(welcome);
}

function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    const themeToggle = document.getElementById('themeToggle');
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update icon
    themeToggle.textContent = newTheme === 'light' ? '🌙' : '☀️';
}

// Initialize theme
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const themeToggle = document.getElementById('themeToggle');
    document.documentElement.setAttribute('data-theme', savedTheme);
    themeToggle.textContent = savedTheme === 'light' ? '🌙' : '☀️';
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}

// Load available models
async function loadModels() {
    try {
        const response = await fetch('/models');
        const data = await response.json();
        const modelSelector = document.getElementById('modelSelector');
        
        modelSelector.innerHTML = '';
        data.models.forEach(model => {
            const option = document.createElement('option');
            option.value = model.id;
            option.textContent = model.name;
            if (model.id === data.default) {
                option.selected = true;
            }
            modelSelector.appendChild(option);
        });
        
        // Save selected model to localStorage
        const savedModel = localStorage.getItem('selectedModel');
        if (savedModel && data.models.find(m => m.id === savedModel)) {
            modelSelector.value = savedModel;
        }
        
        // Update localStorage when model changes
        modelSelector.addEventListener('change', () => {
            localStorage.setItem('selectedModel', modelSelector.value);
        });
    } catch (error) {
        console.error('Error loading models:', error);
        const modelSelector = document.getElementById('modelSelector');
        modelSelector.innerHTML = '<option value="">Error loading models</option>';
    }
}

// Initialize on load
initTheme();
loadChats();
loadModels();

// Auto-resize textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 200) + 'px';
});

// Send message on Enter (Shift+Enter for new line)
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function sendExample(text) {
    messageInput.value = text;
    sendMessage();
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Hide welcome screen on first message
    const ws = document.getElementById('welcomeScreen');
    if (ws) {
        ws.remove();
    }

    // Add user message
    addMessage(message, 'user', null, null, true);
    messageInput.value = '';
    messageInput.style.height = 'auto';
    sendButton.disabled = true;

    // Add loading indicator with stages
    const loadingId = addLoadingMessage();
    
    // Start stage progression animation
    let currentStageIndex = 0;
    const stages = ['validate', 'resolve', 'plan', 'execute', 'format'];
    
    const progressInterval = setInterval(() => {
        if (currentStageIndex < stages.length) {
            const stage = stages[currentStageIndex];
            const stageEl = document.getElementById(`stage-${stage}`);
            if (stageEl) {
                // Mark previous as completed
                if (currentStageIndex > 0) {
                    const prevStage = stages[currentStageIndex - 1];
                    const prevEl = document.getElementById(`stage-${prevStage}`);
                    if (prevEl) {
                        prevEl.classList.remove('active');
                        prevEl.classList.add('completed');
                    }
                }
                // Mark current as active
                stageEl.classList.remove('pending');
                stageEl.classList.add('active');
                currentStageIndex++;
            }
        }
    }, 400); // Progress every 400ms

    try {
        const modelSelector = document.getElementById('modelSelector');
        const selectedModel = modelSelector.value;
        
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: currentSessionId,
                model: selectedModel || null,
                history: []
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Request failed');
        }
        
        const data = await response.json();
        
        // Clear the progress interval
        clearInterval(progressInterval);
        
        // Mark all stages as completed
        document.querySelectorAll('.stage-item').forEach(stage => {
            stage.classList.remove('active', 'pending');
            stage.classList.add('completed');
        });
        
        // Brief delay to show completion
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Remove loading indicator
        removeLoadingMessage(loadingId);

        // Add assistant response with technical details
        let fullAnswer = data.answer;
        if (data.context) {
            fullAnswer += '\n\n' + data.context;
        }
        addMessage(fullAnswer, 'assistant', data.sparql, data.technical_details, true);
    } catch (error) {
        // Clear the progress interval on error
        clearInterval(progressInterval);
        removeLoadingMessage(loadingId);
        addMessage(`Sorry, there was an error processing your request.\nError: ${error.message}`, 'assistant', null, null, true);
        console.error('Error:', error);
    } finally {
        sendButton.disabled = false;
        messageInput.focus();
    }
}

function addMessage(content, role, sparql = null, technicalDetails = null, shouldSave = true) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = `avatar ${role}`;
    avatar.textContent = role === 'user' ? 'U' : 'A';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    // Add technical details section if available (for assistant messages only)
    if (role === 'assistant' && technicalDetails) {
        const technicalSection = document.createElement('details');
        technicalSection.className = 'technical-details';
        
        const summary = document.createElement('summary');
        summary.textContent = '🔧 Show Technical Details';
        summary.className = 'technical-summary';
        
        const technicalContent = document.createElement('pre');
        technicalContent.className = 'technical-content';
        technicalContent.textContent = technicalDetails;
        
        technicalSection.appendChild(summary);
        technicalSection.appendChild(technicalContent);
        contentDiv.appendChild(technicalSection);
    }

    // Note: SPARQL query is now included in technical details, not displayed separately

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Save message to chat history
    if (shouldSave) {
        saveMessage(content, role, sparql, technicalDetails);
    }
}

function addLoadingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = 'loading-message';

    const avatar = document.createElement('div');
    avatar.className = 'avatar assistant';
    avatar.textContent = 'A';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Create stage container
    const stageContainer = document.createElement('div');
    stageContainer.className = 'stage-container';
    stageContainer.id = 'stage-container';
    
    const stages = [
        { id: 'validate', icon: '🔍', text: 'Validating query...' },
        { id: 'resolve', icon: '🔧', text: 'Resolving parameters...' },
        { id: 'plan', icon: '📋', text: 'Planning query...' },
        { id: 'execute', icon: '⚡', text: 'Executing SPARQL...' },
        { id: 'format', icon: '✨', text: 'Formatting response...' }
    ];
    
    stages.forEach((stage, index) => {
        const stageDiv = document.createElement('div');
        stageDiv.className = 'stage-item pending';
        stageDiv.id = `stage-${stage.id}`;
        
        const iconSpan = document.createElement('span');
        iconSpan.className = 'stage-icon';
        iconSpan.textContent = stage.icon;
        
        const textSpan = document.createElement('span');
        textSpan.className = 'stage-text';
        textSpan.textContent = stage.text;
        
        stageDiv.appendChild(iconSpan);
        stageDiv.appendChild(textSpan);
        stageContainer.appendChild(stageDiv);
    });
    
    contentDiv.appendChild(stageContainer);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return 'loading-message';
}

function removeLoadingMessage(id) {
    const loadingMsg = document.getElementById(id);
    if (loadingMsg) {
        loadingMsg.remove();
    }
}

// Reset chat handler
document.getElementById('resetButton').addEventListener('click', async function() {
    if (!confirm('Clear current chat history and reset conversation context?')) {
        return;
    }

    try {
        const response = await fetch('/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ session_id: currentSessionId })
        });

        if (response.ok) {
            // Clear messages from current chat
            if (allChats[currentSessionId]) {
                allChats[currentSessionId].messages = [];
                allChats[currentSessionId].title = 'New Chat';
                saveChats();
            }
            
            // Clear UI and show welcome screen
            chatContainer.innerHTML = '';
            showWelcomeScreen();
            renderChatList();
        }
    } catch (error) {
        console.error('Error resetting session:', error);
        alert('Failed to reset session');
    }
});

// Debug toggle handler
let debugVisible = false;
document.getElementById('debugToggle').addEventListener('click', function() {
    debugVisible = !debugVisible;
    this.textContent = debugVisible ? 'Hide Debug' : 'Show Debug';
    
    const debugSections = document.querySelectorAll('.debug-section');
    debugSections.forEach(section => {
        section.style.display = debugVisible ? 'block' : 'none';
    });
});

// Focus input on load
messageInput.focus();
