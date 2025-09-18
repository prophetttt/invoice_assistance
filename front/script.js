// 聊天机器人功能
document.addEventListener('DOMContentLoaded', function() {
    // 只在聊天页面执行聊天相关代码
    if (document.querySelector('.chat-container')) {
        const chatHistory = document.getElementById('chatHistory');
        const userInput = document.getElementById('userInput');
        const sendButton = document.getElementById('sendButton');
        
        // 添加用户消息到聊天历史
        function addUserMessage(message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'chat-message user-message';
            messageDiv.innerHTML = `
                <div class="avatar"><i class="fas fa-user"></i></div>
                <div class="message-content">${message}</div>
            `;
            chatHistory.appendChild(messageDiv);
            scrollToBottom();
        }
        
        // 添加机器人消息到聊天历史
        function addBotMessage(message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'chat-message bot-message';
            messageDiv.innerHTML = `
                <div class="avatar"><i class="fas fa-robot"></i></div>
                <div class="message-content">${message}</div>
            `;
            chatHistory.appendChild(messageDiv);
            scrollToBottom();
        }
        
        // 滚动到底部
        function scrollToBottom() {
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
        
        // 处理用户输入
        function handleUserInput() {
            const message = userInput.value.trim();
            if (message) {
                addUserMessage(message);
                userInput.value = '';
                
                // 模拟机器人响应
                setTimeout(() => {
                    const responses = [
                        "我明白了，您说的是: " + message,
                        "这是一个有趣的问题，让我想想...",
                        "关于" + message + "，我可以告诉您...",
                        "感谢您的提问，我正在处理...",
                        "我已经记录了您的问题，稍后会回复您。"
                    ];
                    const randomResponse = responses[Math.floor(Math.random() * responses.length)];
                    addBotMessage(randomResponse);
                }, 800);
            }
        }
        
        // 事件监听
        sendButton.addEventListener('click', handleUserInput);
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleUserInput();
            }
        });
        
        // 初始滚动到底部
        scrollToBottom();
    }
    
    // 导航栏活动状态
    const currentPage = location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('nav a').forEach(link => {
        const linkPage = link.getAttribute('href');
        if (currentPage === linkPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});