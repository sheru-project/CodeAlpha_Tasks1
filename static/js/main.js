// CSRF Token Setup
const csrftoken = document.querySelector('[name=csrf-token]').content;

// Like Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Like buttons
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            
            try {
                const response = await fetch('/api/toggle-like/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ post_id: postId })
                });
                
                const data = await response.json();
                
                if (data.liked !== undefined) {
                    const likeCount = this.querySelector('.like-count');
                    likeCount.textContent = data.like_count;
                    
                    if (data.liked) {
                        this.classList.add('liked');
                    } else {
                        this.classList.remove('liked');
                    }
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
    
    // Comment toggle buttons
    document.querySelectorAll('.comment-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const postId = this.dataset.postId;
            const commentsSection = document.getElementById(`comments-${postId}`);
            
            if (commentsSection.style.display === 'none') {
                commentsSection.style.display = 'block';
            } else {
                commentsSection.style.display = 'none';
            }
        });
    });
    
    // Comment forms
    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const textarea = this.querySelector('textarea');
            const content = textarea.value.trim();
            
            if (!content) return;
            
            try {
                const response = await fetch('/api/add-comment/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        post_id: postId,
                        content: content
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Add comment to the list
                    const commentsList = document.querySelector(`#comments-${postId} .comments-list`);
                    const newComment = document.createElement('div');
                    newComment.className = 'comment';
                    newComment.innerHTML = `
                        <strong>${data.comment.user}</strong>
                        <p>${data.comment.content}</p>
                        <small>${data.comment.created_at}</small>
                    `;
                    commentsList.appendChild(newComment);
                    
                    // Clear textarea
                    textarea.value = '';
                    
                    // Update comment count
                    const commentCountSpan = document.querySelector(`.comment-btn[data-post-id="${postId}"] .comment-count`);
                    const currentCount = parseInt(commentCountSpan.textContent) || 0;
                    commentCountSpan.textContent = currentCount + 1;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
    
    // Follow buttons
    const followBtn = document.querySelector('.follow-btn');
    if (followBtn) {
        followBtn.addEventListener('click', async function() {
            const userId = this.dataset.userId;
            
            try {
                const response = await fetch('/api/toggle-follow/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ user_id: userId })
                });
                
                const data = await response.json();
                
                if (data.following !== undefined) {
                    // Update button text
                    this.textContent = data.following ? 'Following' : 'Follow';
                    if (data.following) {
                        this.classList.add('following');
                    } else {
                        this.classList.remove('following');
                    }
                    
                    // Update follower count
                    const followerCountSpan = document.querySelector('.follower-count');
                    if (followerCountSpan) {
                        followerCountSpan.textContent = data.follower_count;
                    }
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }
    
    // Edit profile toggle
    const editProfileBtn = document.getElementById('edit-profile-btn');
    const editProfileForm = document.getElementById('edit-profile-form');
    const cancelEditBtn = document.getElementById('cancel-edit');
    
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', () => {
            editProfileForm.style.display = 'block';
            editProfileBtn.style.display = 'none';
        });
    }
    
    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', () => {
            editProfileForm.style.display = 'none';
            if (editProfileBtn) editProfileBtn.style.display = 'inline-block';
        });
    }
});

// Auto-resize textareas
document.querySelectorAll('textarea').forEach(textarea => {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
});