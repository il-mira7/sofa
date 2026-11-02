/**
 * Real Interiors / Portfolio Module
 */
import { state } from './state.js';

const portfolioGrid = document.getElementById('portfolioGrid');

export function renderPortfolio() {
  if (!portfolioGrid) return;
  portfolioGrid.innerHTML = '';

  const data = state.portfolioData;
  if (!data || !data.projects) return;

  data.projects.forEach(project => {
    const card = document.createElement('div');
    card.className = 'portfolio-card';

    card.innerHTML = `
      <img src="${project.image}" alt="${project.title} — ${project.model}" loading="lazy">
      <div class="portfolio-card__overlay">
        <span class="portfolio-card__tag">${project.location}</span>
        <h3 class="portfolio-card__title">${project.title}</h3>
        <p class="portfolio-card__meta">${project.model}</p>
      </div>
    `;

    portfolioGrid.appendChild(card);
  });
}
