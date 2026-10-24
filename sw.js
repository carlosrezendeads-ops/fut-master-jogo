// FUT Master offline: guarda cada arquivo do jogo quando ele carrega com internet
// e usa a cópia guardada quando estiver sem internet (rede primeiro, cópia depois).
const CACHE = "fut-master";
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(CACHE).then(c => c.addAll(["./", "./index.html"]).catch(() => {}))); });
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;
  const chave = url.origin + url.pathname; // sem o ?v= — a versão nova substitui a antiga
  // imagem com versão (?v=): se já está guardada, usa direto sem baixar de novo (abre muito mais rápido)
  if (url.searchParams.has("v")) { e.respondWith(caches.open(CACHE).then(c => c.match(req.url).then(m => m || fetch(req).then(r => { if (r.ok && r.status === 200) { c.put(req.url, r.clone()); c.put(chave, r.clone()); c.keys().then(ks => ks.forEach(k => { const u = new URL(k.url); if (u.pathname === url.pathname && u.search && k.url !== req.url) c.delete(k); })); } return r; }).catch(() => c.match(chave))))); return; }
  e.respondWith(fetch(req).then(r => {
    if (r.ok && r.status === 200) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(chave, cp)); }
    return r;
  }).catch(() => caches.open(CACHE).then(c => c.match(chave).then(m => m || c.match(url.origin + url.pathname.replace(/[^/]*$/, "index.html"))))));
});

// avisos no celular: o push chega vazio; o texto vem do servidor (notificacoes/) e o aviso só aparece se o jogo não estiver na tela
const PUSH_URL = "";
async function hashHex(t) { const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t)); return [...new Uint8Array(d)].map(x => x.toString(16).padStart(2, "0")).join(""); }
self.addEventListener("push", e => e.waitUntil((async () => {
  const wins = await clients.matchAll({ type: "window", includeUncontrolled: true });
  if (wins.some(c => c.visibilityState === "visible" && c.focused)) return;
  let m = { t: "FUT Master", c: "Tem novidade no jogo. Toque para abrir." };
  try { const sub = await self.registration.pushManager.getSubscription(); if (sub && PUSH_URL) { const r = await fetch(PUSH_URL + "/msg?e=" + await hashHex(sub.endpoint)); if (r.ok) m = await r.json(); } } catch (_) {}
  await self.registration.showNotification(m.t || "FUT Master", { body: m.c, icon: "app/icon-192.png", badge: "app/icon-192.png", tag: m.k || "fut" });
})()));
self.addEventListener("notificationclick", e => { e.notification.close(); e.waitUntil(clients.matchAll({ type: "window", includeUncontrolled: true }).then(w => { const c = w.find(x => x.url.startsWith(self.registration.scope)); return c ? c.focus() : clients.openWindow(self.registration.scope); })); });
