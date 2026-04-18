function getCurrentUser() {
    const data = localStorage.getItem('user');
    return data ? JSON.parse(data) : null;
}

function isLoggedIn() {
    return !!localStorage.getItem('access_token');
}

function setAuth(data) {
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('user', JSON.stringify(data.user));
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login.html';
}

function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = '/login.html';
    }
}

