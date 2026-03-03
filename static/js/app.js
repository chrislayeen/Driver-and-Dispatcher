/* BURGERS Fleet App — Shared JavaScript */

// Lightbox utility
function openLightbox(url) {
    const lb = document.getElementById('lb');
    if (lb) {
        document.getElementById('lbImg').src = url;
        lb.style.display = 'flex';
    }
}

function closeLightbox() {
    const lb = document.getElementById('lb');
    if (lb) lb.style.display = 'none';
}

// CSRF token helper for AJAX
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrfToken = getCookie('csrftoken');

// Generic photo preview helper
function addPhotoPreview(file, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const url = URL.createObjectURL(file);
    const div = document.createElement('div');
    div.className = 'relative w-16 h-16 rounded-lg overflow-hidden border border-slate-200 shadow-sm';
    div.innerHTML = `<img src="${url}" class="w-full h-full object-cover cursor-pointer" onclick="openLightbox('${url}')">
        <button type="button" onclick="this.parentElement.remove()" class="absolute top-0 right-0 bg-red-500 text-white p-0.5 rounded-bl-lg shadow-md">
            <span class="material-symbols-outlined text-xs">close</span></button>`;
    container.appendChild(div);
}

console.log('BURGERS Fleet App JS loaded.');
