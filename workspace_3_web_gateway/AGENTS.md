---
id: "ws3-agent-rules"
status: "locked"
depends_on:
  - "ws3-project-context"
provides_context: 
  - "DevOps Operational Rules"
  - "Network Security Taboos"
  - "Frontend Constraints"
  - "Definition of Done (DoD)"
verification_logic: "agent_prompt_injection"
---

# AGENTS: Операционная Конституция и Правила Работы Агента (Web Gateway & Infra)

> **ВНИМАНИЕ, ИИ-АГЕНТ!** 
> Этот документ определяет правила твоей работы в репозитории `web-gateway`. Ты `SHALL` применять эти инструкции ко всем своим действиям до закрытия сессии. Твоя задача — построить непробиваемую, кэшированную инфраструктуру доставки и ультра-быстрый веб-интерфейс без лишних зависимостей.

## 1. Environment & Tech Stack (Рабочая Среда)

* **Infrastructure:** Docker, Docker Compose (спецификация v3+).
* **Reverse Proxy & Delivery:** Nginx (alpine-based).
* **Frontend:** Строго Vanilla JavaScript (ES6+), HTML5, CSS3.
* **Bridge:** Websockify (или аналогичный TCP-to-UDP прокси).

## 2. Red Lines (Красные Линии и Табу)

### 2.1. Network & Security Constraints (Сетевая безопасность)
* **Port Isolation:** Агент `SHALL NOT` экспонировать (publish) внутренние порты микросервисов (`30000 UDP` сервера Luanti или внутренний `TCP` порт Websockify) на публичный интерфейс хост-машины.
* **Single Point of Ingress:** Наружу `SHALL` торчать ИСКЛЮЧИТЕЛЬНО порт веб-сервера Nginx (`[Reference Implementation: 8080 TCP]`). Весь остальной трафик `SHALL` ходить внутри изолированной Docker-сети.
* **Read-Only Mounts:** Агент `SHALL NOT` монтировать конфигурационные файлы или HTML-статику с правом на запись (`rw`). Тома `SHALL` монтироваться строго как `:ro` (Read-Only).

### 2.2. Frontend Constraints (Запреты Фронтенда)
* **No Frameworks:** Агент `SHALL NOT` использовать тяжелые фронтенд-фреймворки (React, Vue, Angular) или сборщики (Webpack, Vite) для страницы-бутстраппера. Код `SHALL` быть написан на чистом Vanilla JS (Zero-Dependency), чтобы минимизировать размер бандла.
* **Strict MIME Types:** Агент `SHALL` гарантировать, что Nginx отдает файлы `.wasm` строго с MIME-типом `application/wasm`. Несоблюдение этого правила приведет к фатальной ошибке загрузки движка в браузере.

## 3. Testing & Linting Tooling (Инструменты проверки)

Перед тем как отметить задачу как выполненную, агент `SHALL` валидировать инфраструктурные файлы стандартными инструментами:

* **Docker Compose Validation:** Агент `SHALL` проверить синтаксис манифеста командой:
  `docker compose config -q`
* **Nginx Config Check:** Агент `SHALL` проверить корректность конфигурации Nginx командой:
  `docker run --rm -v $(pwd)/nginx/nginx.conf:/etc/nginx/nginx.conf:ro nginx:alpine nginx -t`
* **HTML/JS Linting:** Фронтенд-код `SHALL` быть валидным согласно базовым правилам ESLint (без предупреждений о необъявленных переменных).

## 4. Definition of Done (Критерии Готовности)

Задача в этом рабочем пространстве считается выполненной (Done), ТОЛЬКО ЕСЛИ:
1. `docker compose config` не возвращает ошибок.
2. Проверка `nginx -t` успешно пройдена.
3. В `docker-compose.yml` нет директивы `ports:` для UDP-трафика (только для Nginx).
4. `bootstrapper.js` не содержит `import` из внешних npm-пакетов.
