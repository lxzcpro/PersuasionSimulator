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
});
