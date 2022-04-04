// Hide all alerts after 5 seconds
setTimeout(function () {
    let elements = document.querySelectorAll('.alert');
    for (index = 0; index < elements.length; index++) {
        elements[index].style.display = 'none';
    }
}, 5000);