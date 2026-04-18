async function loadOrders() {
    requireAuth();
    var container = document.getElementById('orders-container');

    var res = await apiFetch('/orders/');
    if (!res) return;
    var data = await res.json();
    var orders = data.results || data;

    if (!orders.length) {
        container.innerHTML =
            '<div class="empty-state">' +
            '<p>No orders yet.</p>' +
            '<a href="/dvds.html" class="btn btn-primary">Browse DVDs</a>' +
            '</div>';
        return;
    }

    container.innerHTML =
        '<table class="table">' +
        '<thead><tr>' +
        '<th>Order</th><th>Total</th><th>Status</th><th>Date</th><th>Items</th>' +
        '</tr></thead>' +
        '<tbody>' +
        orders.map(function(order) {
            var itemsText = order.items.map(function(i) {
                return 'DVD #' + i.dvd + ' \u00d7 ' + i.quantity + ' @ $' + parseFloat(i.price).toFixed(2);
            }).join(', ');

            return '<tr>' +
                '<td>#' + order.id + '</td>' +
                '<td>$' + parseFloat(order.total_price).toFixed(2) + '</td>' +
                '<td><span class="badge badge-' + order.status + '">' + order.status + '</span></td>' +
                '<td>' + new Date(order.created_at).toLocaleDateString() + '</td>' +
                '<td class="order-items">' + itemsText + '</td>' +
                '</tr>';
        }).join('') +
        '</tbody></table>';
}

document.addEventListener('DOMContentLoaded', loadOrders);
