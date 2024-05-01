$(document).ready(function() {
    // Load chat history
    $.get('/load_chat', function(data) {
        if (data.error) {
            alert(data.error);
        } else {
            // Add all messages to the chatbox
            for (var i = 0; i < data.messages.length; i++) {
                var message = data.messages[i];
                var text = '<p class="' + (message.username === 'Bot' ? 'bot-message' : 'user-message') + '"><img class="avatar" src="static/images/' + (message.username === 'Bot' ? 'bot-avatar.png' : 'user-avatar.png') + '"> ' + message.username + ': ' + message.message + '</p>';
                $('#chatbox').append(text);
            }
        }
    });

    $('#send').click(function() {
        var message = $('#message').val();
        $('#chatbox').append('<p class="user-message"><img class="avatar" src="static/images/user-avatar.png"> You: ' + message + '</p>');

        $.post('/reply', { message: message }, function(data) {
            if (data.error) {
                alert(data.error);
            } else {
                $('#chatbox').empty();  // Clear the chatbox
                // Add all messages to the chatbox
                for (var i = 0; i < data.messages.length; i++) {
                    var message = data.messages[i];
                    var text = '<p class="' + (message.username === 'Bot' ? 'bot-message' : 'user-message') + '"><img class="avatar" src="static/images/' + (message.username === 'Bot' ? 'bot-avatar.png' : 'user-avatar.png') + '"> ' + message.username + ': ' + message.message + '</p>';
                    $('#chatbox').append(text);
                }
            }
        });

        $('#message').val('');
    });
    $('.pane').click(function() {
        var target = $(this).data('target');
    
        $('.chat-window').removeClass('active');
        $('#' + target).addClass('active');
    });
});

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

document.getElementById('clear-chat').addEventListener('click', function() {
    if (confirm('你确定要清空所有聊天记录吗？')) {
        fetch('/clear_chat', {
            method: 'POST',
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  // Clear the chatbox and refresh the page
                  document.getElementById('chatbox').innerHTML = '';
                  location.reload();
              } else {
                  alert('Failed to clear chat: ' + data.error);
              }
          });
    }
});