function confirmDelete(messageId) {
    if (confirm("確定要刪除這條留言嗎？")) {
        window.location.href = '/deleteMessage?message_id=' + messageId;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    var signupForm = document.getElementById('signup');
    signupForm.addEventListener('submit', function (event) {
        var name = document.getElementById('name').value.trim();
        var signupId = document.getElementById('signup_id').value.trim();
        var signupPassword = document.getElementById('signup_password').value.trim();
        if (name === "" || signupId === "" || signupPassword === "") {
            alert("姓名、帳號、密碼不得為空");
            event.preventDefault();
        }
    });

    var signinForm = document.getElementById('signin');
    signinForm.addEventListener('submit', function (event) {
        var signinId = document.getElementById('signin_id').value.trim();
        var signinPassword = document.getElementById('signin_password').value.trim();
        if (signinId === "" || signinPassword === "") {
            alert("帳號、密碼不得為空");
            event.preventDefault();
        }
    });

});



