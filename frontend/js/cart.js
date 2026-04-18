function getCart() {
    const raw = localStorage.getItem('cart');
    return raw ? JSON.parse(raw) : [];
}

function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function addToCart(dvdId, quantity) {
    if (quantity === undefined) quantity = 1;
    const cart = getCart();
    const existing = cart.find(function(item) { return item.dvd === dvdId; });
    if (existing) {
        existing.quantity += quantity;
    } else {
        cart.push({ dvd: dvdId, quantity: quantity });
    }
    saveCart(cart);
}

function removeFromCart(dvdId) {
    saveCart(getCart().filter(function(item) { return item.dvd !== dvdId; }));
}

function updateCartQuantity(dvdId, quantity) {
    if (quantity <= 0) {
        removeFromCart(dvdId);
        return;
    }
    const cart = getCart();
    const item = cart.find(function(i) { return i.dvd === dvdId; });
    if (item) {
        item.quantity = quantity;
        saveCart(cart);
    }
}

function clearCart() {
    localStorage.removeItem('cart');
}

function getCartCount() {
    return getCart().reduce(function(total, item) { return total + item.quantity; }, 0);
}
