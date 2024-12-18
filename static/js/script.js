
// Add comment button id="comment-form"

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('comment-form');

    form.addEventListener('submit', function(e) {
        console.log('Comment submitted!');
    });
});

