/**
 * Dynamic Content Updater Module
 * Populates text, links, and contacts from data/site.json
 */
export function applySiteContent(siteData) {
  if (!siteData) return;

  // Update elements by specific data attributes
  if (siteData.contacts) {
    if (siteData.contacts.phone) {
      document.querySelectorAll('[data-site-phone]').forEach(el => {
        el.textContent = siteData.contacts.phone;
        if (el.tagName === 'A') {
          el.href = `tel:${siteData.contacts.phoneRaw || siteData.contacts.phone.replace(/[^0-9+]/g, '')}`;
        }
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

  // Generic data-site-text="path.to.value" resolver
  document.querySelectorAll('[data-site-text]').forEach(el => {
    const path = el.getAttribute('data-site-text').split('.');
    let val = siteData;
    for (const key of path) {
      if (val && typeof val === 'object' && key in val) {
        val = val[key];
      } else {
        val = null;
        break;
      }
    }
    if (val && typeof val === 'string') {
      el.textContent = val;
    }
  });
}
