$(document).ready(function() {
    // 示例头像路径数据结构，可以根据需要进行修改
    var avatarPaths = {
        chat1: {
            user: 'static/images/chat1-user-avatar.png',
            bot: 'static/images/chat1-bot-avatar.png'
        },
        chat2: {
            user: 'static/images/chat2-user-avatar.png',
            bot: 'static/images/chat2-bot-avatar.png'
        },
        chat3: {
            user: 'static/images/chat3-user-avatar.png',
            bot: 'static/images/chat3-bot-avatar.png'
        },
        chat4: {
            user: 'static/images/chat4-user-avatar.png',
            bot: 'static/images/chat4-bot-avatar.png'
        },
        chat5: {
            user: 'static/images/chat5-user-avatar.png',
            bot: 'static/images/chat5-bot-avatar.png'
        }
    };

    // 加载初始聊天历史
    var initialUserId = $('#user-id').val(); // 获取用户ID
    var initialChatId = $('#chat-id').val();
    console.log("User ID: " + initialUserId); // 在控制台打印用户ID
    console.log("Chat ID: " + initialChatId);
    loadChatHistory(initialUserId, initialChatId);

    // 处理表单提交
    $("#message-form").submit(function(event) {
        event.preventDefault();  // 阻止表单正常提交
        var chat_id = $("#chat-id").val();
        var message = $("#message").val().trim(); // FIXME: 删除的时候出错

        if (message === '') {
            alert('消息不能为空！');
            return;
        }

        $('#chatbox').append(createMessageHtml('You', message, 'user', chat_id));
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
                            $('#chatbox').append(createMessageHtml(message.username, message.message, message.username === 'Bot' ? 'bot' : 'user', chat_id));
                        }
                        // Scroll to the bottom
                        $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
                    }
                } catch (error) {
                    console.error('处理响应时出错：', error);
                }
            }
        });
        $("#message").val('');
    });

    $('.chat-link').click(function(event) {
        event.preventDefault();  // 阻止链接的默认行为
        var chatId = $(this).data('chat-id');  // 假设聊天链接有一个 data-chat-id 属性，包含聊天的 ID
        var userId = $('#user-id').val(); // 获取用户ID
        loadChatHistory(userId, chatId);
    });

    function loadChatHistory(userId, chatId) {
        $.get('/load_chat?chat_id=' + chatId, function(data) {  // Update the URL for the $.get method
            try {
                if (data.error) {
                    alert(data.error);
                } else {
                    $('#chatbox').empty();  // 清空聊天框
                    // 添加所有消息到聊天框
                    for (var i = 0; i < data.messages.length; i++) {
                        var message = data.messages[i];
                        $('#chatbox').append(createMessageHtml(message.username, message.message, message.username === 'Bot' ? 'bot' : 'user', chatId));
                    }
                    // Scroll to the bottom
                    $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
                }
            } catch (error) {
                console.error('处理响应时出错：', error);
            }
        });
    }

    // 切换聊天窗口
    $('.chat').click(function() {
        $('.chat').removeClass('active'); // 移除其他聊天的 'active' 类名
        $(this).addClass('active'); // 给被点击的聊天添加 'active' 类名
        var target = $(this).data('target');
        $('#chat-id').val(target);  // 更新 chat_id 字段
        $('.chat-window').removeClass('active');
        $('#' + target).addClass('active');
        // 加载新聊天窗口的聊天历史
        var userId = $('#user-id').val(); // 获取用户ID
        loadChatHistory(userId, target);
    });

    // 处理 API key 表单提交
    $('#api-key-form').submit(function(e) {
        e.preventDefault();  // 阻止表单正常提交
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

    // 清除聊天记录按钮点击处理
    $('#clear-chat').click(function() {
        var chat_id = $("#chat-id").val();
        var user_id = $('#user-id').val(); // 获取用户ID
        if (confirm('你确定要清空所有聊天记录吗？')) {
            fetch('/clear_chat/' + chat_id + '/' + user_id, {  // 包括 user_id 在请求中
                method: 'POST',
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 清空聊天框并刷新页面
                    $('#chatbox').html('');
                    location.reload();
                } else {
                    alert('Failed to clear chat: ' + data.error);
                }
            });
        }
    });

    function createMessageHtml(username, message, userType, chatId) {
        var avatar = avatarPaths[chatId][userType];
        return '<p class="' + userType + '-message"><img class="avatar" src="' + avatar + '"> ' + username + ': ' + message + '</p>';
    }
});
