/**
 * Product Quick View Modal Module
 * Leads-driven: Custom size inquiries & WhatsApp triggers
 */
import { state } from './state.js';

const productModal = document.getElementById('productModal');
const modalBody = document.getElementById('modalBody');
const closeModalBtn = document.getElementById('closeModalBtn');
const modalBackdrop = document.getElementById('modalBackdrop');

export function openProductModal(product) {
  if (!productModal || !modalBody) return;
  state.activeProduct = product;
  
  const images = (product.images && product.images.length > 0) 
    ? product.images 
    : ['assets/images/hero/hero-poster.webp'];
  
  const priceDisplay = product.price_formatted_gel || `от ${product.price_from_gel || '3 900'} ₾`;
  const waPhone = (state.siteData && state.siteData.contacts && state.siteData.contacts.phoneRaw) || '995555123456';
  const waText = encodeURIComponent(`Здравствуйте! Интересует модель ${product.title}. Хочу рассчитать стоимость по моим размерам и выбрать ткань.`);
  const waUrl = `https://wa.me/${waPhone}?text=${waText}`;

  const featuresHtml = (product.features && product.features.length > 0)
    ? `<ul class="modal__features">
        ${product.features.map(f => `<li><span class="feat-bullet">✓</span> ${f}</li>`).join('')}
       </ul>`
    : '';

  const fabricsHtml = (product.popular_fabrics && product.popular_fabrics.length > 0)
    ? `<div class="modal__fabrics-tag">
        <strong>Популярные ткани:</strong> ${product.popular_fabrics.join(' • ')}
       </div>`
    : '';

  modalBody.innerHTML = `
    <div class="modal__grid">
      <div class="modal__gallery">
        <div class="modal__main-box">
          <img src="${images[0]}" alt="${product.title}" class="modal__main-img" id="modalMainImg">
          <span class="modal__badge-tag">${product.badge || 'На заказ'}</span>
        </div>
        ${images.length > 1 ? `
          <div class="modal__thumbs">
            ${images.map((img, i) => `
              <img src="${img}" alt="${product.title} ракурс ${i+1}" class="modal__thumb ${i === 0 ? 'active' : ''}" data-src="${img}">
            `).join('')}
          </div>
        ` : ''}
      </div>

      <div class="modal__details">
        <span class="modal__brand">FARFALE LIVING • GEORGIA</span>
        <h2 class="modal__title">${product.title}</h2>
        <p class="modal__tagline">${product.tagline || 'Индивидуальное изготовление под ваше пространство'}</p>

        <div class="modal__price-wrap">
          <span class="modal__price">${priceDisplay}</span>
          <span class="modal__production-time">Срок: ${product.lead_time || 'от 25 дней'}</span>
        </div>

        <p class="modal__desc">${product.description || ''}</p>

        ${featuresHtml}
        ${fabricsHtml}

        <div class="modal__specs">
          <div class="spec-item">
            <span class="spec-label">Размеры:</span>
            <span class="spec-val">${product.dimensions_standard || 'Любые под заказ'}</span>
          </div>
          <div class="spec-item">
            <span class="spec-label">Гарантия:</span>
            <span class="spec-val">5 лет на несущий каркас</span>
          </div>
          <div class="spec-item">
            <span class="spec-label">Шоурум:</span>
            <span class="spec-val">Тбилиси, Ваке, ул. Н. Бердзенишвили 2</span>
          </div>
        </div>

        <div class="modal__actions">
          <a href="${waUrl}" target="_blank" rel="noopener" class="btn btn--whatsapp btn--full">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
            </svg>
            Рассчитать в WhatsApp
          </a>
          <button class="btn btn--outline btn--full" id="modalOpenConsultBtn">
            Записаться на примерку в шоурум
          </button>
        </div>
      </div>
    </div>
  `;

  // Thumbs event
  modalBody.querySelectorAll('.modal__thumb').forEach(thumb => {
    thumb.addEventListener('click', (e) => {
      modalBody.querySelectorAll('.modal__thumb').forEach(t => t.classList.remove('active'));
      e.target.classList.add('active');
      const mainImg = document.getElementById('modalMainImg');
      if (mainImg) mainImg.src = e.target.dataset.src;
    });
  });

  // Consult button in modal scrolls to consultation form
  const consultBtn = document.getElementById('modalOpenConsultBtn');
  if (consultBtn) {
    consultBtn.addEventListener('click', () => {
      closeProductModal();
      const consultSection = document.getElementById('consultation');
      if (consultSection) {
        consultSection.scrollIntoView({ behavior: 'smooth' });
        const nameInput = consultSection.querySelector('input[name="name"]');
        if (nameInput) setTimeout(() => nameInput.focus(), 600);
      }
    });
  }

  productModal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

export function closeProductModal() {
  if (!productModal) return;
  productModal.classList.remove('open');
  document.body.style.overflow = '';
}

export function initModalEvents() {
  if (closeModalBtn) closeModalBtn.addEventListener('click', closeProductModal);
  if (modalBackdrop) modalBackdrop.addEventListener('click', closeProductModal);
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && productModal && productModal.classList.contains('open')) {
      closeProductModal();
    }
  });
}
