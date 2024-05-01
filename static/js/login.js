document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var username = document.getElementById('register-username').value;
    var password = document.getElementById('register-password').value;
    console.log('Registering user: ' + username);
    
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'username': username,
            'password': password,
        }),
    }).then(response => response.text())
      .then(text => alert(text));
});

document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-password').value;
    
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'username': username,
            'password': password,
        }),
    })
    .then(response => response.json())
    .then(messages => {
        messages.forEach(message => {
            if (message.sender === 'user') {
                $('#chatbox').append('<p class="user-message"><img class="avatar" src="static/images/user-avatar.png"> You: ' + message.content + '</p>');
            } else if (message.sender === 'bot') {
                $('#chatbox').append('<p class="bot-message"><img class="avatar" src="static/images/bot-avatar.png"> Bot: ' + message.content + '</p>');
            }
        });
        $('#loginModal').modal('hide');
        location.reload();  // Add this line
    });
});


document.getElementById('logoutButton').addEventListener('click', function(event) {
    event.preventDefault();
    
    fetch('/logout', {
        method: 'POST',
    }).then(response => response.text())
      .then(text => {
        alert(text);
        location.reload();
      });
});
