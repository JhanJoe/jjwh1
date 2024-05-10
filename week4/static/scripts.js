document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const termsCheckbox = document.getElementById('termsCheckbox');

    const squareForm = document.getElementById('squareForm');
    const squareNumberInput = document.querySelector('input[name="square_number"]');

        loginForm.addEventListener('submit', function (event) {
            if (!termsCheckbox.checked) {
                alert("請先勾選同意條款");
                event.preventDefault();
            }
        });

       squareForm.addEventListener('submit', function (event) {
        event.preventDefault();  
        if (!isPositiveInteger(squareNumberInput.value)) {
            alert("請輸入有效的正整數");
            event.preventDefault();
        } else {
            window.location.href = `http://127.0.0.1:8000/square/${squareNumberInput.value}`;
        }
    });

    function isPositiveInteger(str) {
        var n = Math.floor(Number(str));
        return n !== Infinity && String(n) === str && n > 0;
    }
});


