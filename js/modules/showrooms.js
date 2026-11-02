/**
 * Showrooms Module — Farfale Living Vake, Tbilisi
 */
import { state } from './state.js';

const showroomsContainer = document.getElementById('showroomsContainer');

export function renderShowrooms() {
  if (!showroomsContainer) return;
  showroomsContainer.innerHTML = '';

  const data = state.showroomsData;
  if (!data || !data.showrooms || data.showrooms.length === 0) return;

  const room = data.showrooms[0];
  const photos = room.photos || [];

  const card = document.createElement('div');
  card.className = 'showroom-flagship';

  card.innerHTML = `
    <div class="showroom-flagship__grid">
      <div class="showroom-flagship__gallery">
        <div class="showroom-main-photo">
          <img src="${photos[0] || 'assets/images/showroom/showroom-street.webp'}" alt="${room.title}" id="showroomMainPhoto" class="showroom-img-active">
        </div>
        ${photos.length > 1 ? `
          <div class="showroom-thumbs">
            ${photos.map((p, i) => `
              <div class="showroom-thumb-box ${i === 0 ? 'active' : ''}" data-src="${p}">
                <img src="${p}" alt="Шоурум Farfale ракурс ${i+1}" loading="lazy">
              </div>
            `).join('')}
          </div>
        ` : ''}
      </div>

      <div class="showroom-flagship__info">
        <span class="showroom-badge">Флагманский шоурум • Ваке</span>
        <h2 class="showroom-title">${room.title}</h2>
        <div class="showroom-address-box">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
          <div>
            <strong>${room.address}</strong>
            <div class="showroom-ge-addr">${room.addressGe || 'ნ. ბერძენიშვილის ქუჩა 2, ვაკე, თბილისი'}</div>
          </div>
        </div>

        <p class="showroom-desc">${room.description}</p>

        <div class="showroom-details-list">
          <div class="detail-row">
            <span class="detail-icon">🕒</span>
            <div><strong>График работы:</strong> ${room.hours}</div>
          </div>
          <div class="detail-row">
            <span class="detail-icon">🚗</span>
            <div><strong>Парковка:</strong> ${room.parking}</div>
          </div>
          <div class="detail-row">
            <span class="detail-icon">🚇</span>
            <div><strong>Метро / Локация:</strong> ${room.metro}</div>
          </div>
        </div>

        <div class="showroom-actions">
          <a href="${room.whatsapp}" target="_blank" rel="noopener" class="btn btn--whatsapp">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
            </svg>
            Записаться на примерку в WhatsApp
          </a>
          <a href="https://maps.google.com/?q=N.+Berdzenishvili+2+Tbilisi" target="_blank" rel="noopener" class="btn btn--outline">
            Открыть на Google Maps
          </a>
        </div>
      </div>
    </div>
  `;

  // Thumbs switch
  card.querySelectorAll('.showroom-thumb-box').forEach(thumb => {
    thumb.addEventListener('click', () => {
      card.querySelectorAll('.showroom-thumb-box').forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
      const main = card.querySelector('#showroomMainPhoto');
      if (main) main.src = thumb.dataset.src;
    });
  });

  showroomsContainer.appendChild(card);
}

export function initShowroomsEvents() {
  // Static single-city flagship setup
}
