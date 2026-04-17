const API_BASE = 'http://localhost:8000/api';
// const API_BASE = 'https://your-app.onrender.com/api'; // production

function getImageUrl(url) {
  if (!url) return '../images/placeholder.jpg';
  if (url.startsWith('http')) return url;
  return `${API_BASE.replace('/api', '')}${url}`;
}
