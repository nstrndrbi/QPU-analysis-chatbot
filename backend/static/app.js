document.addEventListener('DOMContentLoaded', function() {
    // Tab navigation
    const navButtons = document.querySelectorAll('.nav-button');
    const sections = document.querySelectorAll('section');
    
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section');
            
            // Update active tab
            navButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Show selected section
            sections.forEach(section => {
                if (section.id === sectionId + '-section') {
                    section.classList.add('active');
                } else {
                    section.classList.remove('active');
                }
            });
        });
    });
    
    // Chat functionality
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.querySelector('.chat-messages');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');
    const toolButtons = document.querySelectorAll('.tool-button');
    
    let chatHistory = [];
    
    // Initialize loading state
    let isLoading = false;
    
    // Function to handle sending messages
    function sendMessage(message) {
        if (!message.trim() || isLoading) return;
        
        // Clear welcome message if it exists
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            chatMessages.removeChild(welcomeMessage);
        }
        
        // Add user message to UI
        const userMessageElement = createMessageElement(message, 'user');
        chatMessages.appendChild(userMessageElement);
        
        // Clear input
        chatInput.value = '';
        
        // Show loading indicator
        isLoading = true;
        const loadingElement = document.createElement('div');
        loadingElement.className = 'loading-indicator';
        loadingElement.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        chatMessages.appendChild(loadingElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Send to backend API
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                history: chatHistory
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading indicator
            chatMessages.removeChild(loadingElement);
            isLoading = false;
            
            // Add bot response to UI
            const botMessageElement = createMessageElement(data.response, 'bot', data.graph);
            chatMessages.appendChild(botMessageElement);
            
            // Update chat history
            chatHistory.push({
                user: message,
                assistant: data.response
            });
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Add quantum particles for visual effect
            addQuantumParticles();
        })
        .catch(error => {
            console.error('Error:', error);
            
            // Remove loading indicator
            chatMessages.removeChild(loadingElement);
            isLoading = false;
            
            // Show error message
            const errorElement = document.createElement('div');
            errorElement.className = 'message error bot';
            errorElement.innerHTML = `
                <div class="message-content">
                    <div class="message-text">Sorry, there was an error processing your request. Please try again.</div>
                </div>
            `;
            chatMessages.appendChild(errorElement);
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }
    
    // Create message element
    function createMessageElement(text, sender, graph = null) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}`;
        
        let messageHTML = `
            <div class="message-content">
                <div class="message-text">${formatText(text)}</div>
            `;
        
        if (graph) {
            messageHTML += `
                <div class="message-graph">
                    <img src="data:image/png;base64,${graph}" alt="Analysis Graph">
                </div>
            `;
        }
        
        messageHTML += `</div>`;
        messageElement.innerHTML = messageHTML;
        
        return messageElement;
    }
    
    // Format text with line breaks
    function formatText(text) {
        return text.replace(/\\n/g, '<br>').replace(/\n/g, '<br>');
    }
    
    // Add some quantum particle effects
    function addQuantumParticles() {
        const particleCount = Math.floor(Math.random() * 3) + 1;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'quantum-particle';
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            chatMessages.appendChild(particle);
            
            // Remove particle after animation
            setTimeout(() => {
                if (particle && particle.parentElement) {
                    particle.parentElement.removeChild(particle);
                }
            }, 5000);
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', () => {
        sendMessage(chatInput.value);
    });
    
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage(chatInput.value);
        }
    });
    
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', () => {
            sendMessage(chip.textContent);
        });
    });
    
    toolButtons.forEach(button => {
        button.addEventListener('click', () => {
            const prompt = button.getAttribute('data-prompt');
            sendMessage(prompt);
        });
    });
    
    // Dashboard functionality
    fetchDashboardData();
    
    function fetchDashboardData() {
        // Fetch the summary data from the API
        Promise.all([
            fetch('/api/summary').then(res => res.json()),
            fetch('/api/efficiency').then(res => res.json())
        ])
        .then(([summaryData, efficiencyData]) => {
            // Hide loading and show content
            document.querySelector('.dashboard-loading').style.display = 'none';
            document.querySelector('.dashboard-content').style.display = 'block';
            
            // Create dashboard cards
            createDashboardCards(summaryData, efficiencyData);
        })
        .catch(error => {
            console.error('Error fetching dashboard data:', error);
            document.querySelector('.dashboard-loading').innerHTML = `
                <p>Error loading data. Please try again later.</p>
                <button onclick="location.reload()" class="action-button">Retry</button>
            `;
        });
    }
    
    function createDashboardCards(summaryData, efficiencyData) {
        const dashboardGrid = document.querySelector('.dashboard-grid');
        
        // Calculate average cost per workload from efficiency data
        const avgCostPerWorkload = efficiencyData.length 
            ? efficiencyData.reduce((sum, day) => sum + day.cost_per_workload, 0) / efficiencyData.length
            : 0;

        // Get the most recent atom block ratio
        const latestAtomRatio = efficiencyData.length 
            ? efficiencyData[efficiencyData.length - 1].atom_block_ratio
            : 0;
        
        // Card 1: QPU Blocks
        const blocksCard = document.createElement('div');
        blocksCard.className = 'dashboard-card';
        blocksCard.innerHTML = `
            <h3>
                <svg viewBox="0 0 24 24" class="icon">
                    <path fill="currentColor" d="M11,7H15V9H11V11H13A2,2 0 0,1 15,13V15A2,2 0 0,1 13,17H9V15H13V13H11A2,2 0 0,1 9,11V9A2,2 0 0,1 11,7M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4Z" />
                </svg>
                QPU Blocks Leased
            </h3>
            <div class="stat-value">${summaryData?.total_blocks_leased || 0}</div>
            <div class="stat-detail">
                <div class="block-type atom">
                    <span class="block-label">Atom</span>
                    <span class="block-value">${summaryData?.atom_blocks || 0}</span>
                </div>
                <div class="block-type photon">
                    <span class="block-label">Photon</span>
                    <span class="block-value">${summaryData?.photon_blocks || 0}</span>
                </div>
                <div class="block-type spin">
                    <span class="block-label">Spin</span>
                    <span class="block-value">${summaryData?.spin_blocks || 0}</span>
                </div>
            </div>
        `;
        dashboardGrid.appendChild(blocksCard);
        
        // Card 2: Workloads
        const workloadsCard = document.createElement('div');
        workloadsCard.className = 'dashboard-card';
        workloadsCard.innerHTML = `
            <h3>
                <svg viewBox="0 0 24 24" class="icon">
                    <path fill="currentColor" d="M21,5C19.89,4.65 18.67,4.5 17.5,4.5C15.55,4.5 13.45,4.9 12,6C10.55,4.9 8.45,4.5 6.5,4.5C4.55,4.5 2.45,4.9 1,6V20.65C1,20.9 1.25,21.15 1.5,21.15C1.6,21.15 1.65,21.1 1.75,21.1C3.1,20.45 5.05,20 6.5,20C8.45,20 10.55,20.4 12,21.5C13.35,20.65 15.8,20 17.5,20C19.15,20 20.85,20.3 22.25,21.05C22.35,21.1 22.4,21.1 22.5,21.1C22.75,21.1 23,20.85 23,20.6V6C22.4,5.55 21.75,5.25 21,5M21,18.5C19.9,18.15 18.7,18 17.5,18C15.8,18 13.35,18.65 12,19.5V8C13.35,7.15 15.8,6.5 17.5,6.5C18.7,6.5 19.9,6.65 21,7V18.5Z" />
                </svg>
                Total Workloads
            </h3>
            <div class="stat-value">${summaryData?.total_workloads?.toLocaleString() || 0}</div>
            <div class="stat-label">
                <span>Avg ${summaryData?.avg_workloads_per_block || 0} workloads per block</span>
            </div>
            <div class="stat-label">
                <span>Avg ${summaryData?.avg_daily_workloads?.toLocaleString() || 0} workloads per day</span>
            </div>
        `;
        dashboardGrid.appendChild(workloadsCard);
        
        // Card 3: Efficiency
        const efficiencyCard = document.createElement('div');
        efficiencyCard.className = 'dashboard-card';
        efficiencyCard.innerHTML = `
            <h3>
                <svg viewBox="0 0 24 24" class="icon">
                    <path fill="currentColor" d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,12.5A1.5,1.5 0 0,1 10.5,11A1.5,1.5 0 0,1 12,9.5A1.5,1.5 0 0,1 13.5,11A1.5,1.5 0 0,1 12,12.5M12,7.2C9.9,7.2 8.2,8.9 8.2,11C8.2,14 12,17.5 12,17.5C12,17.5 15.8,14 15.8,11C15.8,8.9 14.1,7.2 12,7.2Z" />
                </svg>
                Efficiency Metrics
                <span class="quantum-badge">Beta</span>
            </h3>
            <div class="stat-value">$${avgCostPerWorkload.toFixed(2)}</div>
            <div class="stat-label">Average cost per workload</div>
            <div class="efficiency-meter">
                <div class="efficiency-label">Atom Block Ratio</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        style="width: ${latestAtomRatio * 100}%"
                    ></div>
                </div>
                <div class="efficiency-value">${(latestAtomRatio * 100).toFixed(1)}%</div>
            </div>
        `;
        dashboardGrid.appendChild(efficiencyCard);
    }
});