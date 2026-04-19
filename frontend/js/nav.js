function renderNav() {
    const nav = document.getElementById('main-nav');
    if (!nav) return;

    const loggedIn = isLoggedIn();
    const user = getCurrentUser();

    nav.innerHTML = `
        <a href="/index.html" class="brand">DOMOVIE<span class="brand-dot"></span></a>
        <div class="nav-links">
            <a href="/movies.html">Movies</a>
            <span class="nav-sep"></span>
            <a href="/directors.html">Directors</a>
            <span class="nav-sep"></span>
            <a href="/dvds.html">DVDs</a>
            ${loggedIn ? `
                <span class="nav-sep"></span>
                <a href="/cart.html">Cart</a>
                <a href="/orders.html">Orders</a>
                <span class="nav-sep"></span>
                <span class="nav-username">${user.username}</span>
                <button class="nav-out" onclick="logout()">Logout</button>
            ` : `
                <span class="nav-sep"></span>
                <a href="/login.html">Login</a>
                <a href="/register.html" class="nav-link-register">Register</a>
            `}
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', renderNav);
