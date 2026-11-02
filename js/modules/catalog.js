/**
 * Catalog & Products Module
 */
import { state } from './state.js';
import { openProductModal } from './modal.js';

const categoriesTabs = document.getElementById('categoriesTabs');
const productsGrid = document.getElementById('productsGrid');
const currentCategoryTitle = document.getElementById('currentCategoryTitle');
const currentCategoryCount = document.getElementById('currentCategoryCount');
const footerCatLinks = document.getElementById('footerCatLinks');
const desktopCatNav = document.getElementById('desktopCatNav');

export function renderCategoryTabs() {
  if (categoriesTabs) categoriesTabs.innerHTML = '';
  if (footerCatLinks) footerCatLinks.innerHTML = '';

  const categories = Object.keys(state.productsData);

  categories.forEach((catKey) => {
    const cat = state.productsData[catKey];
    if (!cat) return;
    
    // Desktop & Sticky Tab Button
    if (categoriesTabs) {
      const tabBtn = document.createElement('button');
      tabBtn.className = `category-tab ${catKey === state.currentCategory ? 'active' : ''}`;
      tabBtn.textContent = cat.name;
      tabBtn.setAttribute('data-category', catKey);
      tabBtn.addEventListener('click', () => switchCategory(catKey));
      categoriesTabs.appendChild(tabBtn);
    }

    // Footer Links
    if (footerCatLinks) {
      const footLi = document.createElement('li');
      const footLink = document.createElement('a');
      footLink.href = '#catalog';
      footLink.textContent = cat.name;
      footLink.addEventListener('click', (e) => {
        e.preventDefault();
        switchCategory(catKey);
        document.getElementById('catalog')?.scrollIntoView({ behavior: 'smooth' });
      });
      footLi.appendChild(footLink);
      footerCatLinks.appendChild(footLi);
    }
  });
}

export function switchCategory(catKey) {
  state.currentCategory = catKey;
  
  // Update sticky tab buttons
  document.querySelectorAll('.category-tab').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.category === catKey);
  });

  // Update level 2 desktop nav
  if (desktopCatNav) {
    desktopCatNav.querySelectorAll('.cat-nav-link').forEach(link => {
      link.classList.toggle('active', link.dataset.cat === catKey);
    });
  }

  renderProducts(catKey);
}

export function renderProducts(catKey) {
  const category = state.productsData[catKey];
  if (!category) return;

  if (currentCategoryTitle) currentCategoryTitle.textContent = category.name;
  if (currentCategoryCount) currentCategoryCount.textContent = `${category.total || category.products.length} моделей`;

  if (!productsGrid) return;
  productsGrid.innerHTML = '';

  category.products.forEach(product => {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');
    
    const images = product.images && product.images.length > 0 ? product.images : ['assets/images/hero/hero-poster.webp'];
    const mainImg = images[0];
    const secondImg = images[1] || mainImg;
    const formattedPrice = product.price_formatted_gel || `от ${product.price_from_gel || '3 900'} ₾`;

    card.innerHTML = `
      <div class="product-card__img-box">
        <img src="${mainImg}" alt="${product.title}" class="product-card__img" loading="lazy" data-hover="${secondImg}">
        <span class="product-card__tag-badge">${product.badge || 'На заказ'}</span>
        <button class="product-card__quick-btn" aria-label="Быстрый просмотр и расчет">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
          Рассчитать модель
        </button>
      </div>
      <div class="product-card__info">
        <div class="product-card__header-line">
          <h3 class="product-card__title">${product.title}</h3>
          <span class="product-card__cat-label">${product.categoryName || ''}</span>
        </div>
        <p class="product-card__tagline-short">${product.tagline || ''}</p>
        <div class="product-card__meta">
          <span class="product-card__price">${formattedPrice}</span>
          <span class="product-card__badge">срок: ${product.lead_time || 'от 25 дн.'}</span>
        </div>
      </div>
    `;

    // Hover swap image
    const imgEl = card.querySelector('.product-card__img');
    card.addEventListener('mouseenter', () => {
      if (secondImg && secondImg !== mainImg) imgEl.src = secondImg;
    });
    card.addEventListener('mouseleave', () => {
      imgEl.src = mainImg;
    });

    // Click opens modal
    card.addEventListener('click', () => {
      openProductModal(product);
    });

    // Keyboard accessibility
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openProductModal(product);
      }
    });

    productsGrid.appendChild(card);
  });
}

export function initCatalogNavEvents() {
  if (desktopCatNav) {
    desktopCatNav.querySelectorAll('.cat-nav-link').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const cat = link.getAttribute('data-cat');
        if (cat) {
          switchCategory(cat);
          document.getElementById('catalog')?.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  }
}
