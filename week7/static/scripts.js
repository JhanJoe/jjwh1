function confirmDelete(messageId) {
    if (confirm("確定要刪除這條留言嗎？")) {
        window.location.href = '/deleteMessage?message_id=' + messageId;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    let signupForm = document.getElementById('signup');
    signupForm.addEventListener('submit', function (event) {
        let name = document.getElementById('name').value.trim();
        let signupId = document.getElementById('signup_id').value.trim();
        let signupPassword = document.getElementById('signup_password').value.trim();
        if (name === "" || signupId === "" || signupPassword === "") {
            alert("姓名、帳號、密碼不得為空");
            event.preventDefault();
        }
    });

    let signinForm = document.getElementById('signin');
    signinForm.addEventListener('submit', function (event) {
        let signinId = document.getElementById('signin_id').value.trim();
        let signinPassword = document.getElementById('signin_password').value.trim();
        if (signinId === "" || signinPassword === "") {
            alert("帳號、密碼不得為空");
            event.preventDefault();
        }
    });
    
});

document.getElementById('query').addEventListener('submit', function(event) {
    event.preventDefault(); // 防止表單提交刷新頁面

    let queryInput = document.getElementById('query_input').value.trim();
    if (queryInput === "") {
        alert("輸入不得為空");
        return;
    }

    history.pushState(null, '', `/api/member?username=${queryInput}`);
    
    fetch(`/api/member?username=${queryInput}`)
        .then(response => response.json())
        .then(data => {
            let queryResult = document.getElementById('query_result');
            if (data.data) {
                queryResult.innerHTML = `${data.data.name} (${data.data.username})`;
            } else {
                queryResult.innerHTML = "No Data";
            }
        })
        .catch(error => {
            console.error('Error fetching member data:', error);
            document.getElementById('query_result').innerHTML = "Error fetching data";
        });
});


