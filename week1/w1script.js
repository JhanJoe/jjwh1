function togglemenu() {
    var popupMenu = document.querySelector('.popup-menu');
    if (popupMenu.style.display === 'block') {
        popupMenu.style.display = 'none';
    } else {
        popupMenu.style.display = 'block';
    }
}

document.addEventListener('DOMContentLoaded', function() {
   document.querySelector('.close-btn').addEventListener('click', function() {
       document.querySelector('.popup-menu').style.display = 'none';
    });
});

