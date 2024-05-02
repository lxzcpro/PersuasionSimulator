$(document).ready(function() {
    // 加载初始聊天历史
    var initialUserId = $('#user-id').val(); // 获取用户ID
    var initialChatId = $('#chat-id').val();
    loadChatHistory(initialUserId, initialChatId);

    // 处理表单提交
    $("#message-form").submit(function(event) {
        event.preventDefault();  // 阻止表单正常提交
        var chat_id = $("#chat-id").val();
        var message = $("#message").val();
        $('#chatbox').append(createMessageHtml('You', message, 'user'));
        $.ajax({
            url: '/reply',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'chat-id': chat_id, message: message }),  // Use 'chat-id' instead of 'chat_id'
            success: function(data) {
                console.log(data);
                try {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        $('#chatbox').empty();  // 清空聊天框
                        // 添加所有消息到聊天框
                        for (var i = 0; i < data.messages.length; i++) {
                            var message = data.messages[i];
                            $('#chatbox').append(createMessageHtml(message.username, message.message, message.username === 'Bot' ? 'bot' : 'user'));
                        }
                    }
                } catch (error) {
                    console.error('处理响应时出错：', error);
                }
            }
        });
        $("#message").val('');
        $('.chat-link').click(function(event) {
            event.preventDefault();  // 阻止链接的默认行为
            var chatId = $(this).data('chat-id');  // 假设聊天链接有一个 data-chat-id 属性，包含聊天的 ID
            loadChatHistory(chatId);
        });
    });
    
    function loadChatHistory(chatId) {
        var userId = $('#user-id').val(); // 获取用户ID
        $.get('/get_chat/' + chatId + '/' + userId, function(data) {  // Provide a URL for the $.get method
            try {
                if (data.error) {
                    alert(data.error);
                } else {
                    $('#chatbox').empty();  // Clear the chatbox
                    // Add all messages to the chatbox
                    for (var i = 0; i < data.messages.length; i++) {
                        var message = data.messages[i];
                        $('#chatbox').append(createMessageHtml(message.username, message.message, message.username === 'Bot' ? 'bot' : 'user'));
                    }
                }
            } catch (error) {
                console.error('Error processing response:', error);
            }
        });
    }

    // Handle chat window switch
    $('.chat').click(function() {
        $('.chat').removeClass('active'); // 移除其他聊天的 'active' 类名
        $(this).addClass('active'); // 给被点击的聊天添加 'active' 类名
        var target = $(this).data('target');
        $('#chat-id').val(target);  // 更新 chat_id 字段
        $('.chat-window').removeClass('active');
        $('#' + target).addClass('active');
        // 加载新聊天窗口的聊天历史
        loadChatHistory(target);
    });

    // Handle API key form submission
    $('#api-key-form').submit(function(e) {
        e.preventDefault();  // Prevent the form from being submitted normally
        var apiKey = $('#api-key').val();

        if (!apiKey) {
            alert('Please provide an API key');
            return;
        }

        $.post('/save_api_key', { 'api-key': apiKey }, function(data) {
            if (data.error) {
                alert(data.error);
            } else {
                alert('API key saved successfully');
            }
        });
    });

    // Handle chat clear button click
    $('#clear-chat').click(function() {
        var chat_id = $("#chat-id").val();
        var user_id = $('#user-id').val(); // 获取用户ID
        if (confirm('你确定要清空所有聊天记录吗？')) {
            fetch('/clear_chat/' + chat_id + '/' + user_id, {  // Include user_id in the request
                method: 'POST',
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Clear the chatbox and refresh the page
                    $('#chatbox').html('');
                    location.reload();
                } else {
                    alert('Failed to clear chat: ' + data.error);
                }
            });
        }
    });
    

    function createMessageHtml(username, message, userType) {
        var avatar = 'static/images/' + (userType === 'bot' ? 'bot-avatar.png' : 'user-avatar.png');
        return '<p class="' + userType + '-message"><img class="avatar" src="' + avatar + '"> ' + username + ': ' + message + '</p>';
    }
});