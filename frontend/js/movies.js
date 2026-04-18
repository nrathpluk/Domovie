var currentPage = 1;
var currentSearch = '';

async function loadMovies(page, search) {
    var grid = document.getElementById('movies-grid');
    var pager = document.getElementById('pagination');
    grid.innerHTML = '<div class="loading">Loading movies…</div>';

    var url = '/movies/?page=' + page;
    if (search) url += '&search=' + encodeURIComponent(search);

    var res = await apiFetch(url);
    if (!res) return;
    var data = await res.json();

    if (!data.results || !data.results.length) {
        grid.innerHTML = '<div class="empty-state"><p>No movies found.</p></div>';
        pager.innerHTML = '';
        return;
    }

    grid.innerHTML = data.results.map(function(m, i) {
        var idx = String(i + 1).padStart(2, '0');
        var year = m.release_date ? m.release_date.slice(0, 4) : '';
        var meta = [m.director_name || 'Unknown', year].filter(Boolean).join(' \u2022 ');
        return '<div class="card">' +
            '<span class="card-frame">' + idx + '</span>' +
            (m.poster_url
                ? '<img src="' + m.poster_url + '" alt="' + m.title + '" loading="lazy">'
                : '<div class="card-img-placeholder">NO FILM</div>') +
            '<div class="card-body">' +
            '<div class="card-title">' + m.title + '</div>' +
            '<div class="card-meta">' + meta + '</div>' +
            '</div></div>';
    }).join('');

    renderPagination(data.count, page, pager);
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
    loadMovies(page, currentSearch);
    window.scrollTo(0, 0);
}

document.addEventListener('DOMContentLoaded', function() {
    loadMovies(1, '');

    document.getElementById('search-btn').addEventListener('click', function() {
        currentSearch = document.getElementById('search-input').value.trim();
        currentPage = 1;
        loadMovies(1, currentSearch);
    });

    document.getElementById('search-input').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') document.getElementById('search-btn').click();
    });
});
