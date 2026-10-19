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
  - "Git Governance & Embedded PR Template"
verification_logic: "agent_prompt_injection"
---

# AGENTS: Операционная Конституция и Правила Работы Агента (Web Gateway & Infra)

> **ВНИМАНИЕ, ИИ-АГЕНТ!** 
> Этот документ определяет правила твоей работы в репозитории `web-gateway`. Ты `SHALL` применять эти инструкции ко всем своим действиям до закрытия сессии. Твоя задача — построить непробиваемую, кэшированную инфраструктуру доставки и ультра-быстрый веб-интерфейс без лишних зависимостей.

## 0. Git & Antigravity 2.0 Governance (Операционный регламент)

Агент в среде Google Antigravity 2.0 `SHALL` строго соблюдать следующие инварианты управления кодовой базой:

### 0.1. Git Identity (Идентификация бота)
Перед выполнением любых Git-операций агент `SHALL` применить локальные настройки авторства:
* `git config user.name "DenserBot [Web Gateway]"`
* `git config user.email "ai.denser.ru@gmail.com"`

### 0.2. Branching Constraints (Ветвление)
* **Base Branch:** Агент `SHALL` создавать рабочие ветки строго от актуальной ветки `dev`.
* **Branch Naming:** Имя ветки `SHALL` строго следовать маске: `agent/ws3-gateway/<type>-<short-description>`.
* **Prohibited Push:** Агент `SHALL NOT` пушить напрямую в ветки `main` или `dev`.

### 0.3. Pull Request Protocol (Сдача работы)
* **Target Branch:** Целевой веткой любого Pull Request (Base Branch) ВСЕГДА `SHALL` являться ветка `dev`. Агент `SHALL NOT` открывать PR в ветку `main`.
* **Self-Contained PR Form:** Агент `SHALL` генерировать описание Pull Request строго по следующей встроенной форме (без обращения к файлам за пределами своей рабочей директории):

```markdown
### 🤖 Antigravity Agent Pull Request Report

* **Workspace:** `workspace_3_web_gateway`
* **Agent Role:** `DenserBot [Web Gateway]`
* **Target Spec:** `specs/<УКАЖИ_ИМЯ_СПЕЦИФИКАЦИИ.md>`
* **Model Version:** `<УКАЖИ_МОДЕЛЬ>`

#### 🛠️ Summary of Changes
- <Кратко перечисли изменения в Docker, Nginx или JS-бутстраппере>

#### 🧪 Verification Output (Docker & Nginx Syntax)
```text
<Вставь сюда сырой вывод: docker compose config -q && echo "Docker Compose OK">
<Вставь сюда сырой вывод проверки конфигурации Nginx>
```

#### 🛡️ Invariant Compliance Checklist
- [x] Целевая ветка строго dev (не main)
- [x] Port Isolation: Игровой порт 30000 UDP и внутренний порт Websockify НЕ выставлены наружу
- [x] Single Point of Ingress: Наружу выставлен только порт 8080 (TCP)
- [x] Read-Only Mounts: Конфиги и статика смонтированы с флагом :ro
- [x] Zero-Framework Frontend: Скрипт bootstrapper.js написан на чистом Vanilla JS (без React/Vue/npm)
- [x] Wasm MIME Type: В Nginx жестко прописан заголовок application/wasm для .wasm файлов
```

### 0.4. Antigravity 2.0 Skills & Worktrees (Контекстная гигиена)
* **Worktree Isolation:** Агент `SHALL` учитывать, что сессия запущена в изолированном каталоге Git Worktree.
* **Skills on Demand:** Файлы в директории `specs/` выступают как динамические навыки (Skills). Агент `SHALL NOT` загружать все спецификации разом. При работе с Nginx загружается `03-nginx-delivery.md`, при работе с JS — `04-wasm-bootstrapper.md`.

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
5. Сформирован отчет для Pull Request по встроенной форме из Раздела 0.3 с таргетом на ветку `dev`.
