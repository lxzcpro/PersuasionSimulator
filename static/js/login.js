// 当注册表单被提交时，阻止默认的提交行为，然后发送一个POST请求到'/register'路由
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
    }).then(response => response.json())
      .then(text => alert(text));
});

// 当登录表单被提交时，阻止默认的提交行为，然后发送一个POST请求到'/login'路由
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
    .then(data => {
        if (data.success) {
            $('#chatbox').append('<p class="user-message"><img class="avatar" src="static/images/user-avatar.png"> You: ' + data.message + '</p>');
            $('#loginModal').modal('hide');
            location.reload();
        } else {
            // 显示错误消息
            alert(data.message);
        }
    })
    .catch(error => {
        // 处理解析 JSON 时的错误
        console.error('Error:', error);
    });
});
// 获取注销按钮
var logoutButton = document.getElementById('logoutButton');

if (logoutButton) {
    logoutButton.addEventListener('click', function(event) {
        event.preventDefault();

        fetch('/logout', {
            method: 'POST',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    });
}