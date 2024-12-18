
// Add comment button id="comment-form"

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('comment-form');

    form.addEventListener('submit', function(e) {
        console.log('Comment submitted!');
    });
});

// Delete Post with Modal pop up

document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.btn-delete');
    const deleteForm = document.getElementById('deleteForm');
    
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const slug = this.getAttribute('data-slug');
            deleteForm.action = '/post/' + slug + '/delete/';
            const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
            deleteModal.show();
        });
    });
});
