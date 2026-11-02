/**
 * Blog / News Module
 */
import { state } from './state.js';

const blogGrid = document.getElementById('blogGrid');

export function renderBlog() {
  if (!blogGrid) return;
  blogGrid.innerHTML = '';
  
  state.blogData.forEach(item => {
    const article = document.createElement('article');
    article.className = 'blog-card';
    const tag = item.tag || 'Событие';
    const desc = item.desc || item.descr || '';
    const img = item.image || item.img || '';

    article.innerHTML = `
      <div class="blog-card__media">
        <img src="${img}" alt="${item.title}" class="blog-card__img" loading="lazy">
        <span class="blog-card__tag">${tag}</span>
      </div>
      <div class="blog-card__body">
        <time class="blog-card__date">${item.date}</time>
        <h3 class="blog-card__title">${item.title}</h3>
        ${desc ? `<p class="blog-card__desc">${desc}</p>` : ''}
      </div>
    `;
    blogGrid.appendChild(article);
  });
}
