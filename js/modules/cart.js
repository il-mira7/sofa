/**
 * Shopping Cart Module
 */
import { state } from './state.js';
import { showToast } from './toast.js';

const cartDrawer = document.getElementById('cartDrawer');
const cartBtn = document.getElementById('cartBtn');
const closeCartBtn = document.getElementById('closeCartBtn');
const cartBackdrop = document.getElementById('cartBackdrop');
const cartItemsList = document.getElementById('cartItemsList');
const cartTotalSum = document.getElementById('cartTotalSum');
const cartCount = document.getElementById('cartCount');
const checkoutBtn = document.getElementById('checkoutBtn');

export function addToCart(product) {
  const existing = state.cart.find(i => i.uid === product.uid);
  if (existing) {
    existing.quantity += 1;
  } else {
    state.cart.push({
      uid: product.uid,
      title: product.title,
      price: product.price_gel || 12500,
      price_formatted: product.price_formatted_gel || '12 500 ₾',
      image: product.images[0] || '',
      quantity: 1
    });
  }

  saveCart();
  updateCartUI();
  showToast(`Товар ${product.title} добавлен в корзину`);
}

export function removeFromCart(uid) {
  state.cart = state.cart.filter(i => i.uid !== uid);
  saveCart();
  updateCartUI();
}

export function changeCartQty(uid, delta) {
  const item = state.cart.find(i => i.uid === uid);
  if (!item) return;

  item.quantity += delta;
  if (item.quantity <= 0) {
    removeFromCart(uid);
  } else {
    saveCart();
    updateCartUI();
  }
}

export function saveCart() {
  localStorage.setItem('boca_cart', JSON.stringify(state.cart));
}

export function updateCartUI() {
  const totalCount = state.cart.reduce((acc, item) => acc + item.quantity, 0);
  if (cartCount) cartCount.textContent = totalCount;

  if (!cartItemsList) return;
  cartItemsList.innerHTML = '';

  if (state.cart.length === 0) {
    cartItemsList.innerHTML = `
      <div class="cart-empty">
        <p>Ваша корзина пуста</p>
        <a href="#catalog" class="btn btn--outline btn--sm" id="emptyCartCatalogBtn">Перейти к покупкам</a>
      </div>
    `;
    const emptyBtn = document.getElementById('emptyCartCatalogBtn');
    if (emptyBtn) emptyBtn.addEventListener('click', closeCartDrawer);
    if (cartTotalSum) cartTotalSum.textContent = '0 ₾';
    return;
  }

  let totalSum = 0;

  state.cart.forEach(item => {
    const itemSum = item.price * item.quantity;
    totalSum += itemSum;

    const itemEl = document.createElement('div');
    itemEl.className = 'cart-item';
    itemEl.innerHTML = `
      <img src="${item.image}" alt="${item.title}" class="cart-item__img">
      <div class="cart-item__info">
        <h4 class="cart-item__title">${item.title}</h4>
        <span class="cart-item__price">${item.price_formatted}</span>
        <div class="cart-item__controls">
          <button class="qty-btn" data-minus="${item.uid}">-</button>
          <span class="qty-val">${item.quantity}</span>
          <button class="qty-btn" data-plus="${item.uid}">+</button>
        </div>
      </div>
      <button class="cart-item__remove" data-remove="${item.uid}" aria-label="Удалить">&times;</button>
    `;

    itemEl.querySelector('[data-minus]').addEventListener('click', () => changeCartQty(item.uid, -1));
    itemEl.querySelector('[data-plus]').addEventListener('click', () => changeCartQty(item.uid, 1));
    itemEl.querySelector('[data-remove]').addEventListener('click', () => removeFromCart(item.uid));

    cartItemsList.appendChild(itemEl);
  });

  if (cartTotalSum) {
    cartTotalSum.textContent = `${totalSum.toLocaleString('ru-RU')} ₾`;
  }
}

export function openCartDrawer() {
  if (!cartDrawer) return;
  cartDrawer.classList.add('open');
  document.body.style.overflow = 'hidden';
}

export function closeCartDrawer() {
  if (!cartDrawer) return;
  cartDrawer.classList.remove('open');
  document.body.style.overflow = '';
}

export function initCartEvents() {
  if (cartBtn) cartBtn.addEventListener('click', openCartDrawer);
  if (closeCartBtn) closeCartBtn.addEventListener('click', closeCartDrawer);
  if (cartBackdrop) cartBackdrop.addEventListener('click', closeCartDrawer);

  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
      if (state.cart.length === 0) {
        showToast('Добавьте товары в корзину для оформления');
        return;
      }
      closeCartDrawer();
      showToast('Спасибо за заказ! Наш менеджер в Тбилиси свяжется с вами для уточнения деталей.');
      state.cart = [];
      saveCart();
      updateCartUI();
    });
  }
}
