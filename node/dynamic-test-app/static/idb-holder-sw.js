// Opens the 'rfdb' IndexedDB database and never closes the connection, so that a
// versionchange, as caused by deleting the database, stays blocked. Used to test that
// Set Storage State reports a service worker which blocks restoring the storage state.
let heldConnection;

self.addEventListener('install', () => self.skipWaiting());

// Answers whether the connection is open yet, so that tests can wait for it instead of sleeping.
self.addEventListener('message', (event) => {
    if (event.ports[0]) event.ports[0].postMessage(heldConnection ? 'open' : 'pending');
});

self.addEventListener('activate', (event) =>
    event.waitUntil(
        (async () => {
            await self.clients.claim();
            heldConnection = await new Promise((resolve, reject) => {
                const request = indexedDB.open('rfdb', 1);
                request.onupgradeneeded = () => request.result.createObjectStore('kv');
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            });
        })(),
    ),
);
