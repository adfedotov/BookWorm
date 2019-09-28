dashboardMain() {
    document.getElementById('local-search').oninput = function() {
        let input = this.value
        const cards = document.getElementsByClassName('dashboard-books')[0].children;
        for (i = 0; i < cards.length; i++) {
            let title = cards[i].children[1];
            if (title.innerText.search(new RegExp(input, 'i')) < 0) {
                cards[i].style.display = 'none';
            } else {
                cards[i].style.display = 'flex';
            }
        }
    }
}

function dashboardSearch() {
    const base = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port;
    document.getElementById('book-search-btn').onclick = function() {
        const query = document.getElementById('book-search').value;
        search(query);
        return false;
    }

    function search(query) {
        location.href = base + '/dashboard/search/' + query;
    }
}

window.onload = function(e) {
    if (window.location.pathname === '/dashboard') {
        dashboardMain();
    }
    else if (window.location.pathname.includes('/dashboard/search')) {
        dashboardSearch();
    }
}