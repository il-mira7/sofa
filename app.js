/**
 * BOCA ROOM Georgia — Main Application Script
 * Ultra-fast, zero-dependency, modular modern JavaScript
 */

document.addEventListener('DOMContentLoaded', async () => {
  // State
  let state = {
    productsData: {},
    showroomsData: [],
    blogData: [],
    siteData: null,
    currentCategory: 'sofas',
    currentShowroomCity: 'Тбилиси',
    cart: JSON.parse(localStorage.getItem('boca_cart') || '[]'),
    activeProduct: null
  };

  // DOM Elements
  const categoriesTabs = document.getElementById('categoriesTabs');
  const productsGrid = document.getElementById('productsGrid');
  const currentCategoryTitle = document.getElementById('currentCategoryTitle');
  const currentCategoryCount = document.getElementById('currentCategoryCount');
  const footerCatLinks = document.getElementById('footerCatLinks');
  
  const showroomsContainer = document.getElementById('showroomsContainer');
  const showroomCityTabs = document.getElementById('showroomCityTabs');
  
  const blogGrid = document.getElementById('blogGrid');
  
  const productModal = document.getElementById('productModal');
  const modalBody = document.getElementById('modalBody');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const modalBackdrop = document.getElementById('modalBackdrop');
  
  const cartDrawer = document.getElementById('cartDrawer');
  const cartBtn = document.getElementById('cartBtn');
  const closeCartBtn = document.getElementById('closeCartBtn');
  const cartBackdrop = document.getElementById('cartBackdrop');
  const cartItemsList = document.getElementById('cartItemsList');
  const cartTotalSum = document.getElementById('cartTotalSum');
  const cartCount = document.getElementById('cartCount');
  const checkoutBtn = document.getElementById('checkoutBtn');
  
  // Mega Menu & Side Drawer Elements
  const openMegaMenuBtn = document.getElementById('openMegaMenuBtn');
  const megaMenu = document.getElementById('megaMenu');
  const closeMegaMenuBtn = document.getElementById('closeMegaMenuBtn');
  const megaMenuBackdrop = document.getElementById('megaMenuBackdrop');
  
  const sideDrawerBtn = document.getElementById('sideDrawerBtn');
  const sideDrawer = document.getElementById('sideDrawer');
  const closeSideDrawerBtn = document.getElementById('closeSideDrawerBtn');
  const sideDrawerBackdrop = document.getElementById('sideDrawerBackdrop');

  const desktopCatNav = document.getElementById('desktopCatNav');
  const consultForm = document.getElementById('consultForm');
  const toast = document.getElementById('toast');

  // Load Data
  try {
    const [prodRes, showRes, blogRes, siteRes] = await Promise.all([
      fetch('data/products.json').then(r => r.json()).catch(() => ({})),
      fetch('data/showrooms.json').then(r => r.json()).catch(() => []),
      fetch('data/blog.json').then(r => r.json()).catch(() => []),
      fetch('data/site.json').then(r => r.json()).catch(() => null)
    ]);

    state.productsData = prodRes;
    state.showroomsData = showRes;
    state.blogData = blogRes;
    state.siteData = siteRes;

    if (siteRes) {
      applySiteContent(siteRes);
    }

    initApp();
  } catch (err) {
    console.error('Error loading data:', err);
    showToast('Ошибка загрузки данных каталога');
  }

  function applySiteContent(siteData) {
    if (!siteData) return;
    if (siteData.contacts) {
      if (siteData.contacts.phone) {
        document.querySelectorAll('[data-site-phone]').forEach(el => {
          el.textContent = siteData.contacts.phone;
          if (el.tagName === 'A') el.href = `tel:${siteData.contacts.phoneRaw || siteData.contacts.phone.replace(/[^0-9+]/g, '')}`;
        });
      }
      if (siteData.contacts.whatsapp) {
        document.querySelectorAll('[data-site-whatsapp]').forEach(el => {
          if (el.tagName === 'A') el.href = siteData.contacts.whatsapp;
        });
      }
      if (siteData.contacts.telegram) {
        document.querySelectorAll('[data-site-telegram]').forEach(el => {
          if (el.tagName === 'A') el.href = siteData.contacts.telegram;
        });
      }
      if (siteData.contacts.address) {
        document.querySelectorAll('[data-site-address]').forEach(el => {
          el.textContent = siteData.contacts.address;
        });
      }
    }
    if (siteData.announcement && siteData.announcement.topBar) {
      document.querySelectorAll('[data-site-topbar]').forEach(el => {
        el.textContent = siteData.announcement.topBar;
      });
    }
  }

  function initApp() {
    renderCategoryTabs();
    renderProducts(state.currentCategory);
    renderShowrooms(state.currentShowroomCity);
    renderBlog();
    updateCartUI();
    setupEventListeners();
  }

  // ==========================================
  // Categories & Products
  // ==========================================
  function renderCategoryTabs() {
    if (categoriesTabs) categoriesTabs.innerHTML = '';
    if (footerCatLinks) footerCatLinks.innerHTML = '';

    const categories = Object.keys(state.productsData);

    categories.forEach((catKey) => {
      const cat = state.productsData[catKey];
      
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
        footLink.addEventListener('click', () => switchCategory(catKey));
        footLi.appendChild(footLink);
        footerCatLinks.appendChild(footLi);
      }
    });
  }

  function switchCategory(catKey) {
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

  function renderProducts(catKey) {
    const category = state.productsData[catKey];
    if (!category) return;

    if (currentCategoryTitle) currentCategoryTitle.textContent = category.name;
    if (currentCategoryCount) currentCategoryCount.textContent = `${category.total} моделей`;

    if (!productsGrid) return;
    productsGrid.innerHTML = '';

    category.products.forEach(product => {
      // Create product link pointing to its individual page (e.g. cosmo.html)
      const productUrl = product.url || 'cosmo.html';
      const card = document.createElement('a');
      card.className = 'product-card';
      card.href = productUrl;
      
      const mainImg = product.images[0] || 'https://via.placeholder.com/600x600?text=BOCA+ROOM';
      const secondImg = product.images[1] || mainImg;
      const formattedPrice = product.price_formatted_gel || product.price_formatted;

      card.innerHTML = `
        <div class="product-card__img-box">
          <img src="${mainImg}" alt="${product.title}" class="product-card__img" loading="lazy" data-hover="${secondImg}">
          <button class="product-card__quick-btn" aria-label="Быстрый просмотр">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
            Быстрый просмотр
          </button>
        </div>
        <div class="product-card__info">
          <h3 class="product-card__title">${product.title}</h3>
          <div class="product-card__meta">
            <span class="product-card__price">от ${formattedPrice}</span>
            <span class="product-card__badge">на заказ 45 дн.</span>
          </div>
        </div>
      `;

      // Hover secondary image effect if available
      const imgEl = card.querySelector('.product-card__img');
      if (product.images.length > 1) {
        card.addEventListener('mouseenter', () => {
          imgEl.src = secondImg;
        });
        card.addEventListener('mouseleave', () => {
          imgEl.src = mainImg;
        });
      }

      // Quick view button opens modal without opening link
      const quickBtn = card.querySelector('.product-card__quick-btn');
      if (quickBtn) {
        quickBtn.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          openProductModal(product);
        });
      }

      productsGrid.appendChild(card);
    });
  }

  // ==========================================
  // Product Modal (Quick View)
  // ==========================================
  function openProductModal(product) {
    if (!productModal || !modalBody) return;
    state.activeProduct = product;
    const images = product.images.length > 0 ? product.images : ['https://via.placeholder.com/600x600?text=BOCA+ROOM'];
    const priceDisplay = product.price_formatted_gel || product.price_formatted;
    const productUrl = product.url || 'cosmo.html';

    modalBody.innerHTML = `
      <div class="modal__grid">
        <div class="modal__gallery">
          <img src="${images[0]}" alt="${product.title}" class="modal__main-img" id="modalMainImg">
          ${images.length > 1 ? `
            <div class="modal__thumbs">
              ${images.map((img, i) => `
                <img src="${img}" alt="${product.title} ${i+1}" class="modal__thumb ${i === 0 ? 'active' : ''}" data-src="${img}">
              `).join('')}
            </div>
          ` : ''}
        </div>
        <div class="modal__details">
          <span class="modal__brand">BOCA ROOM GEORGIA</span>
          <h2 class="modal__title">${product.title}</h2>
          <div class="modal__price-wrap">
            <span class="modal__price">от ${priceDisplay}</span>
            <span class="modal__production-time">Срок изготовления ~45 дней</span>
          </div>
          <p class="modal__desc">
            Премиальный модульный диван от BOCA ROOM. Доступно более 50 вариантов высококачественных тканей и фактур (букле, рогожка, шенилл, кожа). Индивидуальные размеры под ваш интерьер.
          </p>
          <div class="modal__specs">
            <div class="spec-item">
              <span class="spec-label">Гарантия:</span>
              <span class="spec-val">5 лет</span>
            </div>
            <div class="spec-item">
              <span class="spec-label">Доставка:</span>
              <span class="spec-val">Тбилиси, Батуми и вся Грузия</span>
            </div>
          </div>
          <div class="modal__actions">
            <button class="btn btn--primary btn--full" id="modalAddToCartBtn">Добавить в корзину</button>
            <a href="${productUrl}" class="btn btn--outline btn--full" style="text-align: center; display: block; margin-top: 10px;">Перейти на страницу модели →</a>
          </div>
        </div>
      </div>
    `;

    // Thumbnails click handling
    modalBody.querySelectorAll('.modal__thumb').forEach(thumb => {
      thumb.addEventListener('click', (e) => {
        modalBody.querySelectorAll('.modal__thumb').forEach(t => t.classList.remove('active'));
        e.target.classList.add('active');
        document.getElementById('modalMainImg').src = e.target.dataset.src;
      });
    });

    // Add to cart in modal
    const addBtn = document.getElementById('modalAddToCartBtn');
    if (addBtn) {
      addBtn.addEventListener('click', () => {
        addToCart(product);
        closeProductModal();
        openCartDrawer();
      });
    }

    productModal.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeProductModal() {
    if (!productModal) return;
    productModal.classList.remove('open');
    document.body.style.overflow = '';
  }

  // ==========================================
  // Showrooms
  // ==========================================
  function renderShowrooms(cityName) {
    if (!showroomsContainer) return;
    showroomsContainer.innerHTML = '';
    const filtered = state.showroomsData.filter(s => s.city.toLowerCase() === cityName.toLowerCase());

    if (filtered.length === 0) {
      showroomsContainer.innerHTML = `<p class="empty-state">Нет данных о шоуруме в выбранном городе.</p>`;
      return;
    }

    filtered.forEach(room => {
      const roomCard = document.createElement('div');
      roomCard.className = 'showroom-card';
      const mainPhoto = room.photos && room.photos.length > 0 ? room.photos[0] : 'https://static.tildacdn.com/tild3637-3539-4633-b931-323938643830/holodilnyi_5.jpg';

      roomCard.innerHTML = `
        <div class="showroom-card__media">
          <img src="${mainPhoto}" alt="${room.city}, ${room.address}" class="showroom-card__img" loading="lazy">
        </div>
        <div class="showroom-card__info">
          <span class="showroom-card__city-badge">${room.country} • ${room.city}</span>
          <h3 class="showroom-card__address">${room.address}</h3>
          ${room.metro ? `<p class="showroom-card__metro">${room.metro}</p>` : ''}
          <div class="showroom-card__schedule">
            <div><strong>Будни:</strong> ${room.weekdays}</div>
            <div><strong>Выходные:</strong> ${room.weekend}</div>
          </div>
          <div class="showroom-card__contacts">
            <a href="tel:${room.phone.replace(/[^0-9+]/g, '')}" class="showroom-phone">${room.phone}</a>
            <a href="https://wa.me/995322123456" target="_blank" rel="noopener" class="btn btn--outline btn--sm">WhatsApp</a>
          </div>
        </div>
      `;

      showroomsContainer.appendChild(roomCard);
    });
  }

  // ==========================================
  // Blog / Events
  // ==========================================
  function renderBlog() {
    if (!blogGrid) return;
    blogGrid.innerHTML = '';
    state.blogData.forEach(item => {
      const article = document.createElement('article');
      article.className = 'blog-card';
      article.innerHTML = `
        <div class="blog-card__media">
          <img src="${item.img}" alt="${item.title}" class="blog-card__img" loading="lazy">
          <span class="blog-card__tag">${item.tag}</span>
        </div>
        <div class="blog-card__body">
          <time class="blog-card__date">${item.date}</time>
          <h3 class="blog-card__title">${item.title}</h3>
          <p class="blog-card__desc">${item.desc}</p>
        </div>
      `;
      blogGrid.appendChild(article);
    });
  }

  // ==========================================
  // Cart Logic
  // ==========================================
  function addToCart(product) {
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

  function removeFromCart(uid) {
    state.cart = state.cart.filter(i => i.uid !== uid);
    saveCart();
    updateCartUI();
  }

  function changeCartQty(uid, delta) {
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

  function saveCart() {
    localStorage.setItem('boca_cart', JSON.stringify(state.cart));
  }

  function updateCartUI() {
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

  function openCartDrawer() {
    if (!cartDrawer) return;
    cartDrawer.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeCartDrawer() {
    if (!cartDrawer) return;
    cartDrawer.classList.remove('open');
    document.body.style.overflow = '';
  }

  // ==========================================
  // Mega Menu & Side Drawer Handlers
  // ==========================================
  function openMegaMenu() {
    if (!megaMenu) return;
    megaMenu.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeMegaMenu() {
    if (!megaMenu) return;
    megaMenu.classList.remove('open');
    document.body.style.overflow = '';
  }

  function openSideDrawer() {
    if (!sideDrawer) return;
    sideDrawer.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeSideDrawer() {
    if (!sideDrawer) return;
    sideDrawer.classList.remove('open');
    document.body.style.overflow = '';
  }

  // ==========================================
  // Toast Notification
  // ==========================================
  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3200);
  }

  // ==========================================
  // Event Listeners
  // ==========================================
  function setupEventListeners() {
    // Showroom city tabs
    if (showroomCityTabs) {
      showroomCityTabs.querySelectorAll('.city-tab').forEach(btn => {
        btn.addEventListener('click', (e) => {
          showroomCityTabs.querySelectorAll('.city-tab').forEach(b => b.classList.remove('active'));
          e.target.classList.add('active');
          renderShowrooms(e.target.dataset.city);
        });
      });
    }

    // Mega Menu triggers
    if (openMegaMenuBtn) openMegaMenuBtn.addEventListener('click', openMegaMenu);
    if (closeMegaMenuBtn) closeMegaMenuBtn.addEventListener('click', closeMegaMenu);
    if (megaMenuBackdrop) megaMenuBackdrop.addEventListener('click', closeMegaMenu);

    if (megaMenu) {
      megaMenu.querySelectorAll('.mega-card').forEach(card => {
        card.addEventListener('click', (e) => {
          const cat = card.dataset.cat;
          if (cat) {
            switchCategory(cat);
            closeMegaMenu();
          }
        });
      });
    }

    // Level 2 Desktop Category Nav
    if (desktopCatNav) {
      desktopCatNav.querySelectorAll('.cat-nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
          const cat = link.dataset.cat;
          if (cat) {
            e.preventDefault();
            switchCategory(cat);
            const catalogSec = document.getElementById('catalog');
            if (catalogSec) catalogSec.scrollIntoView({ behavior: 'smooth' });
          }
        });
      });
    }

    // Side Drawer triggers
    if (sideDrawerBtn) sideDrawerBtn.addEventListener('click', openSideDrawer);
    if (closeSideDrawerBtn) closeSideDrawerBtn.addEventListener('click', closeSideDrawer);
    if (sideDrawerBackdrop) sideDrawerBackdrop.addEventListener('click', closeSideDrawer);

    document.querySelectorAll('[data-close-drawer]').forEach(el => {
      el.addEventListener('click', closeSideDrawer);
    });

    // Cart Drawer triggers
    if (cartBtn) cartBtn.addEventListener('click', openCartDrawer);
    if (closeCartBtn) closeCartBtn.addEventListener('click', closeCartDrawer);
    if (cartBackdrop) cartBackdrop.addEventListener('click', closeCartDrawer);

    // Modal triggers
    if (closeModalBtn) closeModalBtn.addEventListener('click', closeProductModal);
    if (modalBackdrop) modalBackdrop.addEventListener('click', closeProductModal);

    // Checkout button
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

    // Consultation Form
    if (consultForm) {
      consultForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const fd = new FormData(consultForm);
        const name = fd.get('name');
        const phone = fd.get('phone');
        
        showToast(`Спасибо, ${name}! Мы свяжемся с вами по номеру ${phone} в течение 15 минут.`);
        consultForm.reset();
      });
    }

    // ESC key closes any open dialog
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeProductModal();
        closeCartDrawer();
        closeMegaMenu();
        closeSideDrawer();
      }
    });
  }
});
