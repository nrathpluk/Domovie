const API_BASE = 'https://domovie-backend.onrender.com/api';

function getImageUrl(url) {
  if (!url) return '../images/placeholder.jpg';
  if (url.startsWith('http')) return url;
  return `${API_BASE.replace('/api', '')}${url}`;
}
