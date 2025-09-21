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
        async function handleUserInput() {
            const message = userInput.value.trim();
            if (message) {
                addUserMessage(message);
                userInput.value = '';

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message })
                    });

                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }

                    const data = await response.json();
                    addBotMessage(data.reply);
                } catch (error) {
                    console.error('Error:', error);
                    addBotMessage('抱歉，我无法处理您的请求，请稍后再试。');
                }
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


// 现在可以安全使用 marked 了！
document.addEventListener('DOMContentLoaded', function() {
  fetch('word_new.md')
    .then(response => response.text())
    .then(markdownText => {
      // marked 已全局可用
      document.getElementById('markdown-container').innerHTML = 
        marked.parse(markdownText);
    });
});