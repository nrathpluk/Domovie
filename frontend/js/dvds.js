var currentPage = 1;
var currentSearch = '';

async function loadDVDs(page, search) {
    var grid = document.getElementById('dvds-grid');
    var pager = document.getElementById('pagination');
    grid.innerHTML = '<div class="loading">Loading DVDs…</div>';

    var url = '/dvds/?page=' + page;
    if (search) url += '&search=' + encodeURIComponent(search);

    var res = await apiFetch(url);
    if (!res) return;
    var data = await res.json();

    if (!data.results || !data.results.length) {
        grid.innerHTML = '<div class="empty-state"><p>No DVDs found.</p></div>';
        pager.innerHTML = '';
        return;
    }

    grid.innerHTML = data.results.map(function(dvd, i) {
        var idx = String(i + 1).padStart(2, '0');
        var oos = dvd.stock === 0 ? '<div class="card-oos">OUT OF STOCK</div>' : '';
        var addBtn = dvd.stock > 0
            ? '<button class="btn btn-primary btn-sm" onclick="handleAddToCart(' + dvd.id + ')">Add to Cart</button>'
            : '';

        return '<div class="card">' +
            oos +
            '<span class="card-frame">' + idx + '</span>' +
            (dvd.cover_image
                ? '<img src="' + dvd.cover_image + '" alt="' + dvd.movie_title + '" loading="lazy">'
                : '<div class="card-img-placeholder">DISC</div>') +
            '<div class="card-body">' +
            '<div class="card-title">' + dvd.movie_title + '</div>' +
            '<div class="card-price">$' + parseFloat(dvd.price).toFixed(2) + '</div>' +
            '<div class="card-meta">Stock: ' + dvd.stock + '</div>' +
            (addBtn ? '<div style="margin-top:0.5rem">' + addBtn + '</div>' : '') +
            '</div></div>';
    }).join('');

    renderPagination(data.count, page, pager);
}

function handleAddToCart(dvdId) {
    if (!isLoggedIn()) {
        window.location.href = '/login.html';
        return;
    }
    addToCart(dvdId);
    var alertEl = document.getElementById('alert');
    alertEl.textContent = 'Added to cart!';
    alertEl.className = 'alert alert-success';
    alertEl.style.display = 'block';
    setTimeout(function() { alertEl.style.display = 'none'; }, 2500);
}

function renderPagination(total, page, container) {
    var pages = Math.ceil(total / 10);
    if (pages <= 1) { container.innerHTML = ''; return; }

    var btns = [];
    if (page > 1) btns.push('<button onclick="go(' + (page - 1) + ')">‹ Prev</button>');
    for (var i = 1; i <= pages; i++) {
        btns.push('<button class="' + (i === page ? 'active' : '') + '" onclick="go(' + i + ')">' + i + '</button>');
    }
    if (page < pages) btns.push('<button onclick="go(' + (page + 1) + ')">Next ›</button>');
    container.innerHTML = btns.join('');
}

function go(page) {
    currentPage = page;
    loadDVDs(page, currentSearch);
    window.scrollTo(0, 0);
}

document.addEventListener('DOMContentLoaded', function() {
    loadDVDs(1, '');

    document.getElementById('search-btn').addEventListener('click', function() {
        currentSearch = document.getElementById('search-input').value.trim();
        currentPage = 1;
        loadDVDs(1, currentSearch);
    });

    document.getElementById('search-input').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') document.getElementById('search-btn').click();
    });
});
