// FUT Master offline: guarda cada arquivo do jogo quando ele carrega com internet
// e usa a cópia guardada quando estiver sem internet (rede primeiro, cópia depois).
const CACHE = "fut-master";
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(CACHE).then(c => c.addAll(["./", "./index.html"]).catch(() => {}))); });
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;
  const chave = url.origin + url.pathname; // sem o ?v= — a versão nova substitui a antiga
  e.respondWith(fetch(req).then(r => {
    if (r.ok && r.status === 200) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(chave, cp)); }
    return r;
  }).catch(() => caches.open(CACHE).then(c => c.match(chave).then(m => m || c.match(url.origin + url.pathname.replace(/[^/]*$/, "index.html"))))));
});
