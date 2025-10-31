document.querySelector('.search-icon').addEventListener('click', function(event) {
    event.preventDefault();
    document.querySelector('.search-container').style.display = 'block';
    document.querySelector('.overlay').style.display = 'block';
});

document.querySelector('.overlay').addEventListener('click', function() {
    document.querySelector('.search-container').style.display = 'none';
    document.querySelector('.overlay').style.display = 'none';
});