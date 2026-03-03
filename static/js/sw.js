self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

self.addEventListener('push', (event) => {
    const data = event.data ? event.data.json() : {};
    const title = data.title || "BURGERS Fleet Update";
    const options = {
        body: data.message || "You have a new update from dispatch.",
        icon: "https://burgersgroup.com/wp-content/uploads/2025/05/logo-blue.svg",
        badge: "https://burgersgroup.com/wp-content/uploads/2025/05/logo-blue.svg",
        vibrate: [100, 50, 100],
        data: {
            url: "/driver/"
        }
    };

    event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    event.waitUntil(
        clients.matchAll({ type: 'window' }).then((clientList) => {
            for (const client of clientList) {
                if (client.url === '/' && 'focus' in client) return client.focus();
            }
            if (clients.openWindow) return clients.openWindow('/driver/');
        })
    );
});
