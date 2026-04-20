function renderNav() {
    const nav = document.getElementById('main-nav');
    if (!nav) return;

    const loggedIn = isLoggedIn();
    const user = getCurrentUser();
    const path = window.location.pathname;

    function activeClass(href) {
        return path.endsWith(href) || (href === '/index.html' && path === '/') ? ' class="active"' : '';
    }

    nav.innerHTML = `
        <a href="/index.html" class="brand">DOMOVIE<span class="brand-dot"></span></a>
        <button class="nav-hamburger" id="nav-hamburger" aria-label="Toggle navigation" aria-expanded="false">
            <span></span><span></span><span></span>
        </button>
        <div class="nav-links" id="nav-links">
            <a href="/movies.html"${activeClass('/movies.html')}>Movies</a>
            <span class="nav-sep"></span>
            <a href="/directors.html"${activeClass('/directors.html')}>Directors</a>
            <span class="nav-sep"></span>
            <a href="/dvds.html"${activeClass('/dvds.html')}>DVDs</a>
            ${loggedIn ? `
                <span class="nav-sep"></span>
                <a href="/cart.html"${activeClass('/cart.html')}>Cart</a>
                <a href="/orders.html"${activeClass('/orders.html')}>Orders</a>
                <span class="nav-sep"></span>
                <span class="nav-username">${user.username}</span>
                <button class="nav-out" onclick="logout()">Logout</button>
            ` : `
                <span class="nav-sep"></span>
                <a href="/login.html"${activeClass('/login.html')}>Login</a>
                <a href="/register.html" class="nav-link-register${path.endsWith('/register.html') ? ' active' : ''}">Register</a>
            `}
        </div>
    `;

    const hamburger = document.getElementById('nav-hamburger');
    const links = document.getElementById('nav-links');
    hamburger.addEventListener('click', function () {
        const open = links.classList.toggle('open');
        hamburger.classList.toggle('open', open);
        hamburger.setAttribute('aria-expanded', open);
    });

    links.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () {
            links.classList.remove('open');
            hamburger.classList.remove('open');
            hamburger.setAttribute('aria-expanded', 'false');
        });
    });
}

document.addEventListener('DOMContentLoaded', renderNav);
