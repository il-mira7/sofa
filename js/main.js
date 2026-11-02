/**
 * Farfale Living Georgia — Application Entry Point
 * Cool & Comfy • Vake, Tbilisi
 */
import { state } from './modules/state.js';
import { showToast } from './modules/toast.js';
import { initModalEvents } from './modules/modal.js';
import { renderCategoryTabs, renderProducts, initCatalogNavEvents } from './modules/catalog.js';
import { renderShowrooms } from './modules/showrooms.js';
import { renderPortfolio } from './modules/portfolio.js';
import { initMenuEvents } from './modules/menu.js';
import { applySiteContent } from './modules/siteContent.js';

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const [prodRes, showRes, portRes, siteRes] = await Promise.all([
      fetch('data/products.json').then(r => r.json()).catch(() => ({})),
      fetch('data/showrooms.json').then(r => r.json()).catch(() => ({})),
      fetch('data/portfolio.json').then(r => r.json()).catch(() => ({})),
      fetch('data/site.json').then(r => r.json()).catch(() => null)
    ]);

    state.productsData = prodRes;
    state.showroomsData = showRes;
    state.portfolioData = portRes;
    state.siteData = siteRes;

    // Apply texts from data/site.json
    if (state.siteData) {
      applySiteContent(state.siteData);
    }

    // Initialize UI
    renderCategoryTabs();
    renderProducts(state.currentCategory);
    renderPortfolio();
    renderShowrooms();

    // Event listeners
    initModalEvents();
    initCatalogNavEvents();
    initMenuEvents();

    // Consultation form submission handler
    const consultForm = document.getElementById('consultForm');
    if (consultForm) {
      consultForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(consultForm);
        const name = formData.get('name') || '';
        const phone = formData.get('phone') || '';
        const message = formData.get('message') || '';

        const waPhone = (state.siteData && state.siteData.contacts && state.siteData.contacts.phoneRaw) || '995555123456';
        const waText = encodeURIComponent(`Здравствуйте! Меня зовут ${name}. Мой телефон: ${phone}. Вопрос / размеры: ${message || 'хочу получить консультацию по диванам'}`);
        
        showToast('Спасибо за заявку! Открываем WhatsApp для связи...');
        setTimeout(() => {
          window.open(`https://wa.me/${waPhone}?text=${waText}`, '_blank');
          consultForm.reset();
        }, 800);
      });
    }

  } catch (err) {
    console.error('Initialization error:', err);
    showToast('Ошибка загрузки данных сайта');
  }
});
