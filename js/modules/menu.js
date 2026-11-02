/**
 * Navigation, Mega Menu & Drawers Module
 */
import { switchCategory } from './catalog.js';
import { closeProductModal } from './modal.js';
import { closeCartDrawer } from './cart.js';
import { showToast } from './toast.js';

const openMegaMenuBtn = document.getElementById('openMegaMenuBtn');
const megaMenu = document.getElementById('megaMenu');
const closeMegaMenuBtn = document.getElementById('closeMegaMenuBtn');
const megaMenuBackdrop = document.getElementById('megaMenuBackdrop');

const sideDrawerBtn = document.getElementById('sideDrawerBtn');
const sideDrawer = document.getElementById('sideDrawer');
const closeSideDrawerBtn = document.getElementById('closeSideDrawerBtn');
const sideDrawerBackdrop = document.getElementById('sideDrawerBackdrop');

const consultForm = document.getElementById('consultForm');

export function openMegaMenu() {
  if (!megaMenu) return;
  megaMenu.classList.add('open');
  document.body.style.overflow = 'hidden';
}

export function closeMegaMenu() {
  if (!megaMenu) return;
  megaMenu.classList.remove('open');
  document.body.style.overflow = '';
}

export function openSideDrawer() {
  if (!sideDrawer) return;
  sideDrawer.classList.add('open');
  document.body.style.overflow = 'hidden';
}

export function closeSideDrawer() {
  if (!sideDrawer) return;
  sideDrawer.classList.remove('open');
  document.body.style.overflow = '';
}

export function initMenuEvents() {
  if (openMegaMenuBtn) openMegaMenuBtn.addEventListener('click', openMegaMenu);
  if (closeMegaMenuBtn) closeMegaMenuBtn.addEventListener('click', closeMegaMenu);
  if (megaMenuBackdrop) megaMenuBackdrop.addEventListener('click', closeMegaMenu);

  if (megaMenu) {
    megaMenu.querySelectorAll('.mega-card').forEach(card => {
      card.addEventListener('click', () => {
        const cat = card.dataset.cat;
        if (cat) {
          switchCategory(cat);
          closeMegaMenu();
        }
      });
    });
  }

  if (sideDrawerBtn) sideDrawerBtn.addEventListener('click', openSideDrawer);
  if (closeSideDrawerBtn) closeSideDrawerBtn.addEventListener('click', closeSideDrawer);
  if (sideDrawerBackdrop) sideDrawerBackdrop.addEventListener('click', closeSideDrawer);

  document.querySelectorAll('[data-close-drawer]').forEach(el => {
    el.addEventListener('click', closeSideDrawer);
  });

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

  // Global ESC key handler
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeProductModal();
      closeCartDrawer();
      closeMegaMenu();
      closeSideDrawer();
    }
  });
}
