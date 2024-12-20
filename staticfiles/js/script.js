document.addEventListener('DOMContentLoaded', function() {
    // Existing comment form listener
    const form = document.getElementById('comment-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('Comment submitted!');
        });
    }

    // Existing delete post functionality
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

    // New voting functionality
    const voteButtons = document.querySelectorAll('.vote-icon');
    voteButtons.forEach(button => {
        button.addEventListener('click', handleVote);
    });

    // NEW: Apply saved votes when the page loads
    applySavedVotes();
});

// NEW: Function to apply saved votes
function applySavedVotes() {
    const voteButtons = document.querySelectorAll('.vote-icon');
    voteButtons.forEach(button => {
        const contentId = button.getAttribute('data-content-id');
        const contentType = button.getAttribute('data-content-type');
        const savedVote = localStorage.getItem(`vote_${contentType}_${contentId}`);
        if (savedVote) {
            const voteContainer = button.closest('.vote-container');
            if (voteContainer) {
                const upvoteButton = voteContainer.querySelector('.upvote');
                const downvoteButton = voteContainer.querySelector('.downvote');
                const targetButton = savedVote === '1' ? upvoteButton : downvoteButton;
                targetButton.classList.add(savedVote === '1' ? 'upvoted' : 'downvoted', 'voted');
            }
        }
    });
}

function handleVote(event) {
    const button = event.target;
    const contentId = button.getAttribute('data-content-id');
    const contentType = button.getAttribute('data-content-type');
    const isUpvote = button.classList.contains('upvote');
    const voteValue = isUpvote ? 1 : -1;

    fetch('/vote/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            content_type: contentType,
            object_id: contentId,
            value: voteValue
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Update score display
            const scoreElement = document.getElementById(`score-${contentId}`);
            if (scoreElement) {
                scoreElement.textContent = data.total_votes;
            }

            // Update button styles
            const voteContainer = button.closest('.vote-container');
            if (voteContainer) {
                const upvoteButton = voteContainer.querySelector('.upvote');
                const downvoteButton = voteContainer.querySelector('.downvote');

                if (upvoteButton && downvoteButton) {
                    upvoteButton.classList.remove('upvoted', 'voted');
                    downvoteButton.classList.remove('downvoted', 'voted');

                    if (data.user_vote === 1) {
                        upvoteButton.classList.add('upvoted', 'voted');
                    } else if (data.user_vote === -1) {
                        downvoteButton.classList.add('downvoted', 'voted');
                    }

                    // NEW: Save vote to localStorage
                    if (data.user_vote) {
                        localStorage.setItem(`vote_${contentType}_${contentId}`, data.user_vote);
                    } else {
                        localStorage.removeItem(`vote_${contentType}_${contentId}`);
                    }
                }
            } else {
                console.error('Vote container not found');
            }
        } else {
            throw new Error(data.error || 'Vote failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while voting. Please try again.');
    });
}

// NEW: Function to handle replying to comments
function replyToComment(event, commentId) {
    event.preventDefault();  // Prevent the default anchor behavior
    console.log('Reply function called with commentId:', commentId); // Debugging line

    const form = document.getElementById('comment-form');
    
    // Create a hidden input for parent_id
    const parentInput = document.createElement('input');
    parentInput.type = 'hidden';
    parentInput.name = 'parent_id';
    parentInput.value = commentId;
    
    // Append the hidden input to the form
    form.appendChild(parentInput);

    // Change the heading text
    const heading = document.getElementById('add_comment_form');
    if (heading) {
        heading.textContent = 'Add your reply comment';
    }

    // Scroll to the comment form
    form.scrollIntoView({ behavior: 'smooth' });
}


// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
