// Function that runs once the window is fully loaded
window.onload = function() {
    const savedBaseUrl = localStorage.getItem('apiBaseUrl');
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    const baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    fetch(`${baseUrl}/posts`)
        .then(response => response.json())
        .then(data => {
            window.postsCache = data; // Cache the posts for future use
            displayPosts(data);
        })
        .catch(error => displayFeedback('Error loading posts', true));
}

// Function to send a POST request to the API to add a new post
function addPost() {
    const baseUrl = document.getElementById('api-base-url').value;
    const title = document.getElementById('post-title').value;
    const content = document.getElementById('post-content').value;
    const author = document.getElementById('post-author').value;

    if (!title || !content || !author) {
        displayFeedback('Title, content, and author are required.', true);
        return;
    }

    fetch(`${baseUrl}/posts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content, author })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to add post');
            }
            return response.json();
        })
        .then(post => {
            displayFeedback('Post added successfully');
            loadPosts();
        })
        .catch(error => displayFeedback('Error adding post', true));
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    const baseUrl = document.getElementById('api-base-url').value;

    fetch(`${baseUrl}/posts/${postId}`, { method: 'DELETE' })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to delete post');
            }
            displayFeedback('Post deleted successfully');
            loadPosts();
        })
        .catch(error => displayFeedback('Error deleting post', true));
}

// Function to search posts based on the query
function searchPosts() {
    const baseUrl = document.getElementById('api-base-url').value;
    const searchField = document.getElementById('search-field').value;
    const query = document.getElementById('search-query').value;

    if (!query) {
        displayFeedback('Please enter a search query.', true);
        return;
    }

    fetch(`${baseUrl}/posts/search?${searchField}=${query}`)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                displayFeedback('No posts found for the given query.', true);
                return;
            }
            displayPosts(data);
        })
        .catch(error => displayFeedback('Error searching posts', true));
}

// Function to sort posts based on selected field and direction
function sortPosts() {
    const baseUrl = document.getElementById('api-base-url').value;
    const sortField = document.getElementById('sort-field').value;
    const sortOrder = document.getElementById('sort-order').value;
    const url = `${baseUrl}/posts?direction=${sortOrder}&sort=${sortField}`;
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch sorted posts');
            }
            return response.json();
        })
        .then(data => {
            if (!Array.isArray(data)) {
                displayFeedback('Unexpected response format from server.', true);
                return;
            }
            displayPosts(data); // Use the existing function to display sorted posts
        })
        .catch(error => displayFeedback('Error sorting posts', true));
}

// Utility function to display posts on the page
function displayPosts(posts) {
    const postContainer = document.getElementById('post-container');
    postContainer.innerHTML = '';

    posts.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.className = 'post';
        postDiv.innerHTML = `
            <h2>${post.title}</h2>
            <p>${post.content}</p>
            <div class="meta">Author: ${post.author}</div>
            <div class="meta">Created: ${post.created}</div>
            ${post.updated ? `<div class="meta">Updated: ${post.updated}</div>` : ''}
            <button onclick="deletePost(${post.id})">Delete</button>
            <button onclick="editPost(${post.id}, '${post.title}', '${post.content}', '${post.author}')">Edit</button>
        `;
        postContainer.appendChild(postDiv);
    });
}

// Display feedback to the user
function displayFeedback(message, isError = false) {
    const feedbackElement = document.getElementById('feedback');
    feedbackElement.textContent = message;
    feedbackElement.style.color = isError ? '#ff4444' : '#4466ee';
}

// Function to open an edit form with the selected post's details
function editPost(postId, title, content, author) {
    document.getElementById('post-title').value = title;
    document.getElementById('post-content').value = content;
    document.getElementById('post-author').value = author;

    const addButton = document.querySelector('.input-field button');
    addButton.textContent = 'Update Post';
    addButton.onclick = function () {
        updatePost(postId);
    };
}

// Function to send a PUT request to the API to update an existing post
function updatePost(postId) {
    const baseUrl = document.getElementById('api-base-url').value;
    const title = document.getElementById('post-title').value;
    const content = document.getElementById('post-content').value;
    const author = document.getElementById('post-author').value;

    if (!title || !content || !author) {
        displayFeedback('Title, content, and author are required.', true);
        return;
    }

    fetch(`${baseUrl}/posts/${postId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content, author })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update post');
            }
            return response.json();
        })
        .then(updatedPost => {
            displayFeedback('Post updated successfully');
            loadPosts();

            const addButton = document.querySelector('.input-field button');
            addButton.textContent = 'Add Post';
            addButton.onclick = addPost;
        })
        .catch(error => displayFeedback('Error updating post', true));
}
