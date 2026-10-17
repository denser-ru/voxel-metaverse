---
id: "ws3-03-nginx-delivery"
status: "approved"
depends_on:
  - "ws3-00-domain-vision"
  - "ws3-01-docker-topology"
  - "ws3-02-websockify-bridge"
provides_context:
  - "WebSocket Reverse Proxy"
  - "Wasm MIME Types Enforcement"
  - "Aggressive Caching Strategy"
  - "Compression (Gzip/Brotli)"
verification_logic: "nginx_config_test, mime_type_curl_check, websocket_upgrade_test"
---

# ws3-03-nginx-delivery: Доставка Статики и Обратное Проксирование (Nginx)

> **ABSTRACT:** Документ описывает контракты для компонента `nginx_gateway`. Спецификация устанавливает жесткие правила маршрутизации WebSocket-трафика, требования к MIME-типам для бинарных WebAssembly файлов и стратегии агрессивного кэширования для оптимизации загрузки Zero-Install витрины в браузере.

## 1. WebSocket Reverse Proxy (Обратное проксирование)

Веб-сервер `SHALL` выступать в роли единой точки входа (Port 8080 согласно `[[ws3-01-docker-topology]]`) и маршрутизировать динамический трафик.

* КОГДА клиент запрашивает специальный URI-префикс (`[Reference Implementation: /ws/]`), Nginx `SHALL` проксировать этот запрос во внутренний контейнер `[[ws3-02-websockify-bridge]]`.
* Прокси-блок `SHALL` быть сконфигурирован для поддержки длительных соединений смены протокола (Protocol Upgrade).
  * Сервер `SHALL` передавать заголовки `Upgrade` и `Connection` от клиента к backend-сервису (`[Reference Implementation: proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection "Upgrade";]`).
* Таймауты чтения и записи для прокси-локации `SHALL` быть увеличены (`[Reference Implementation: proxy_read_timeout 3600s]`), чтобы предотвратить обрыв долгих игровых сессий Гостей по вине балансировщика.

## 2. Wasm MIME Types Enforcement (Типизация Wasm)

WebAssembly модули не исполняются современными браузерами, если они отдаются с неверным MIME-типом. Nginx `SHALL` строго специфицировать типы файлов движка.

* Для файлов с расширением `.wasm` сервер `SHALL` возвращать заголовок `Content-Type: application/wasm`.
* Для бинарных файлов виртуальной файловой системы (VFS) движка с расширением `.data` сервер `SHALL` возвращать заголовок `Content-Type: application/octet-stream`.
* ЕСЛИ эти MIME-типы не включены в стандартный файл `mime.types` базового образа Docker, ИИ-агент `SHALL` явно добавить их в конфигурацию.

## 3. Aggressive Caching Strategy (Стратегия кэширования)

Для обеспечения мгновенной загрузки при повторных посещениях, сервер `SHALL` реализовать агрессивную политику кэширования статики. Файлы движка Luanti весят десятки мегабайт, их повторная загрузка `SHALL NOT` допускаться.

* **Heavy Assets (Тяжелые неизменяемые файлы):**
  * Для файлов `.wasm`, `.data` и ассетов из папки `wasm_build/`, Nginx `SHALL` возвращать HTTP-заголовок `Cache-Control: public, max-age=31536000, immutable`.
* **Dynamic / Mutable Assets (Изменяемые файлы):**
  * Для `index.html`, `bootstrapper.js` и конфигурационных JSON файлов, сервер `SHALL` возвращать заголовок `Cache-Control: no-cache, must-revalidate`. 
  * Это гарантирует, что браузер всегда запросит у сервера свежую версию логики входа, даже если Wasm-движок берется из локального кэша.

## 4. Compression Contract (Сжатие трафика)

Для ускорения первой (холодной) загрузки, Nginx `SHALL` сжимать текстовые и бинарные ресурсы "на лету" перед отправкой в сеть.

* Nginx `SHALL` включить компрессию (Gzip ИЛИ Brotli).
* Список типов для сжатия (MIME types) `SHALL` обязательно включать:
  * `text/html`
  * `application/javascript`
  * `application/wasm` (`[CRITICAL]` - Wasm файлы отлично поддаются сжатию, их объем уменьшается до 50%).
  * `application/json`
