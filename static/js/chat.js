$(document).ready(function() {
    $('#send').click(function() {
        var message = $('#message').val();
        $('#chatbox').append('<p class="user-message"><img class="avatar" src="static/images/user-avatar.png"> You: ' + message + '</p>');

        $.post('/reply', { message: message }, function(data) {
            $('#chatbox').append('<p class="bot-message"><img class="avatar" src="static/images/bot-avatar.png"> Bot: ' + data.reply + '</p>');
        });

        $('#message').val('');
    });
});