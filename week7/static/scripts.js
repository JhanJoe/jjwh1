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
    event.preventDefault(); 

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

document.getElementById('update_name').addEventListener('submit', function(event) {
    event.preventDefault();

    let newName = document.getElementById('new_name_input').value.trim();
    if (newName === "") {
        alert("名稱不得為空");
        return;
    }

    fetch('/api/member', {
        method: 'PATCH', 
        headers: {
            'Content-Type': 'application/json', 
        },
        body: JSON.stringify({ name: newName }) 
    })
    .then(response => response.json()) 
    .then(data => {
        let updateStatus = document.getElementById('update_status');
        if (data.ok) {
            updateStatus.innerHTML = "更新成功"; 
        } else {
            updateStatus.innerHTML = "更新失敗"; 
        }
    })
    .catch(error => {
        console.error('Error updating name:', error);
        document.getElementById('update_status').innerHTML = "更新過程中發生錯誤";
    });
});
