const CACHE_NAME = "carbon-tracking-v1.0.0";
const RUNTIME_CACHE = "carbon-tracking-runtime";

// 需要快取的靜態資源
const STATIC_CACHE_URLS = [
  "/carbon/",
  "/carbon/dashboard",
  "/carbon/visit-records",
  "/carbon/add-visit",
  "/carbon/statistics",
  "/static/manifest.json",
];

// 需要快取的 API 端點
const API_CACHE_URLS = [
  "/carbon/api/statistics-summary",
  "/carbon/api/visit-records",
  "/carbon/api/period-statistics",
  "/carbon/api/transport-distribution",
];

// 安裝 Service Worker
self.addEventListener("install", (event) => {
  console.log("[SW] Installing Service Worker...");

  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => {
        console.log("[SW] Caching static resources");
        return cache.addAll(STATIC_CACHE_URLS);
      })
      .then(() => self.skipWaiting())
  );
});

// 啟動 Service Worker
self.addEventListener("activate", (event) => {
  console.log("[SW] Activating Service Worker...");

  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
              console.log("[SW] Deleting old cache:", cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => self.clients.claim())
  );
});

// 攔截網路請求
self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // 跳過非 GET 請求
  if (request.method !== "GET") {
    return;
  }

  // 跳過 chrome-extension 和其他協議
  if (!url.protocol.startsWith("http")) {
    return;
  }

  // API 請求：網路優先，失敗時使用快取
  if (url.pathname.startsWith("/carbon/api/")) {
    event.respondWith(networkFirstStrategy(request));
    return;
  }

  // 靜態資源：快取優先，失敗時使用網路
  if (STATIC_CACHE_URLS.some((path) => url.pathname === path)) {
    event.respondWith(cacheFirstStrategy(request));
    return;
  }

  // 其他請求：網路優先
  event.respondWith(networkFirstStrategy(request));
});

// 快取優先策略
async function cacheFirstStrategy(request) {
  try {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);

    if (cachedResponse) {
      console.log("[SW] Cache hit:", request.url);
      return cachedResponse;
    }

    console.log("[SW] Cache miss, fetching:", request.url);
    const networkResponse = await fetch(request);

    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    console.error("[SW] Cache first strategy failed:", error);
    return new Response("Offline", { status: 503 });
  }
}

// 網路優先策略
async function networkFirstStrategy(request) {
  try {
    const networkResponse = await fetch(request);

    if (networkResponse.ok) {
      const cache = await caches.open(RUNTIME_CACHE);
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    console.log("[SW] Network failed, trying cache:", request.url);

    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    // 如果是 HTML 頁面，返回離線頁面
    if (request.headers.get("accept").includes("text/html")) {
      return caches.match("/carbon/");
    }

    return new Response("Offline", { status: 503 });
  }
}

// 監聽訊息
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }

  if (event.data && event.data.type === "CLEAR_CACHE") {
    event.waitUntil(
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => caches.delete(cacheName))
        );
      })
    );
  }
});

// 背景同步（如果支援）
self.addEventListener("sync", (event) => {
  if (event.tag === "sync-records") {
    event.waitUntil(syncRecords());
  }
});

async function syncRecords() {
  console.log("[SW] Syncing records...");
  // 這裡可以實作離線資料同步邏輯
}

// 推播通知（如果需要）
self.addEventListener("push", (event) => {
  const options = {
    body: event.data ? event.data.text() : "新的通知",
    icon: "/static/icons/icon-192x192.png",
    badge: "/static/icons/icon-96x96.png",
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1,
    },
  };

  event.waitUntil(
    self.registration.showNotification("碳排放追蹤系統", options)
  );
});

// 通知點擊
self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  event.waitUntil(clients.openWindow("/carbon/"));
});
