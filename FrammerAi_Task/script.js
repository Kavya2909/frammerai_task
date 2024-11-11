document.getElementById('userForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const errorMessage = document.getElementById('errorMessage');

    if (!name || !email || !phone) {
        errorMessage.textContent = 'All fields are required.';
        errorMessage.style.display = 'block';
        return;
    }

    errorMessage.style.display = 'none';

    // Perform AJAX request to submit the form data
    const user = { name, email, phone };
    
    fetch('http://127.0.0.1:8000/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user)
    })
    .then(response => response.json())
    .then(data => {
        console.log('User added:', data);
        fetchUsers();  // Update the displayed user list
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function fetchUsers() {
    fetch('http://127.0.0.1:8000/api/users')
    .then(response => response.json())
    .then(users => {
        const userListContainer = document.getElementById('userListContainer');
        userListContainer.innerHTML = '';  // Clear existing list

        users.forEach(user => {
            const userItem = document.createElement('li');
            userItem.textContent = `${user.name} - ${user.email} - ${user.phone}`;
            userListContainer.appendChild(userItem);
        });
    })
    .catch(error => console.error('Error fetching users:', error));
}

// Initial fetch to load users
fetchUsers();
