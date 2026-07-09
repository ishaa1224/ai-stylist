document.addEventListener('DOMContentLoaded', () => {
    updateCartBadge();
    
    // Global Cart Modal Trigger
    const cartLinks = document.querySelectorAll('.nav-cart');
    cartLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            renderCart();
            document.getElementById('globalCartModal').classList.add('active');
        });
    });

    // Close Cart Modal
    const closeBtn = document.getElementById('closeGlobalCart');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            document.getElementById('globalCartModal').classList.remove('active');
        });
    }

    // Close on background click
    const overlay = document.getElementById('globalCartModal');
    if (overlay) {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.remove('active');
            }
        });
    }
});

function getCart() {
    return JSON.parse(localStorage.getItem('aiStylistCartItems')) || [];
}

function saveCart(cart) {
    localStorage.setItem('aiStylistCartItems', JSON.stringify(cart));
    updateCartBadge();
}

function updateCartBadge() {
    const cart = getCart();
    const badges = document.querySelectorAll('.cart-badge');
    badges.forEach(badge => {
        if (cart.length > 0) {
            badge.textContent = cart.length;
            badge.style.display = 'block';
        } else {
            badge.style.display = 'none';
        }
    });
}

function renderCart() {
    const cart = getCart();
    const list = document.getElementById('cartItemsList');
    const totalEl = document.getElementById('cartTotalValue');
    
    if (!list) return;

    list.innerHTML = '';
    let total = 0;

    if (cart.length === 0) {
        list.innerHTML = '<p style="text-align:center; color:#aaa; margin-top:20px;">Your cart is empty.</p>';
    } else {
        cart.forEach((item, index) => {
            const itemEl = document.createElement('div');
            itemEl.className = 'cart-item';
            
            // Handle price parsing (INR 12,345 format)
            const priceNum = parseInt(item.price.replace(/[^0-9]/g, '')) || 0;
            total += priceNum;

            itemEl.innerHTML = `
                <img src="${item.img_url}" alt="${item.name}">
                <div class="cart-item-info">
                    <span class="cart-item-name">${item.name}</span>
                    <span class="cart-item-price">${item.price}</span>
                    <div style="display: flex; gap: 10px; margin-top: 5px;">
                        <button class="remove-item" style="margin:0;" onclick="removeFromCart(${index})">Remove</button>
                        ${item.details_url ? `<a href="${item.details_url}" target="_blank" style="color: #F4D03F; text-decoration: none; font-size: 0.8rem; font-weight: 600;">View Details</a>` : ''}
                    </div>
                </div>
            `;
            list.appendChild(itemEl);
        });
    }

    totalEl.textContent = `INR ${total.toLocaleString('en-IN')}`;
}

function removeFromCart(index) {
    const cart = getCart();
    cart.splice(index, 1);
    saveCart(cart);
    renderCart();
}

function addToCartGlobal(name, price, img_url, details_url = '') {
    const cart = getCart();
    cart.push({ name, price, img_url, details_url });
    saveCart(cart);
    
    // Optional: show modal immediately
    renderCart();
    document.getElementById('globalCartModal').classList.add('active');
}
