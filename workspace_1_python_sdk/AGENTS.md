---
id: "ws1-agent-rules"
status: "locked"
depends_on:
  - "ws1-project-context"
provides_context: 
  - "Agent Operational Rules"
  - "Red Lines (Taboos)"
  - "Testing & Mocking Harness"
  - "Definition of Done (DoD)"
  - "Git Governance & Embedded PR Template"
verification_logic: "agent_prompt_injection"
---

# AGENTS: Операционная Конституция и Правила Работы Агента (Python SDK)

> **ВНИМАНИЕ, ИИ-АГЕНТ!** 
> Этот документ определяет правила твоей работы в репозитории `python-sdk`. Ты `SHALL` применять эти инструкции ко всем своим действиям до закрытия сессии. Твоя задача — написать идеальный, пуленепробиваемый клиент для детей 11–14 лет, который запускается из коробки без сторонних библиотек.

## 0. Git & Antigravity 2.0 Governance (Операционный регламент)

Агент в среде Google Antigravity 2.0 `SHALL` строго соблюдать следующие инварианты управления кодовой базой:

### 0.1. Git Identity (Идентификация бота)
Перед выполнением любых Git-операций агент `SHALL` применить локальные настройки авторства:
* `git config user.name "DenserBot [Python SDK]"`
* `git config user.email "ai.denser.ru@gmail.com"`

### 0.2. Branching Constraints (Ветвление)
* **Base Branch:** Агент `SHALL` создавать рабочие ветки строго от актуальной ветки `dev`.
* **Branch Naming:** Имя ветки `SHALL` строго следовать маске: `agent/ws1-sdk/<type>-<short-description>`.
* **Prohibited Push:** Агент `SHALL NOT` пушить напрямую в ветки `main` или `dev`.

### 0.3. Pull Request Protocol (Сдача работы)
* **Target Branch:** Целевой веткой любого Pull Request (Base Branch) ВСЕГДА `SHALL` являться ветка `dev`. Агент `SHALL NOT` открывать PR в ветку `main`.
* **Self-Contained PR Form:** Агент `SHALL` генерировать описание Pull Request строго по следующей встроенной форме (без обращения к файлам за пределами своей рабочей директории):

```markdown
### 🤖 Antigravity Agent Pull Request Report

* **Workspace:** `workspace_1_python_sdk`
* **Agent Role:** `DenserBot [Python SDK]`
* **Target Spec:** `specs/<УКАЖИ_ИМЯ_СПЕЦИФИКАЦИИ.md>`
* **Model Version:** `<УКАЖИ_МОДЕЛЬ>`

#### 🛠️ Summary of Changes
- <Кратко перечисли реализованные методы или фиксы>

#### 🧪 Verification Output (unittest)
```text
<Вставь сюда сырой вывод выполнения: python -m unittest discover tests>
```

#### 🛡️ Invariant Compliance Checklist
- [x] Целевая ветка строго dev (не main)
- [x] Zero-Dependency: Сторонние библиотеки не используются (только stdlib Python 3.10+)
- [x] Файл requirements.txt отсутствует
- [x] Изменения затронули только файлы внутри workspace_1_python_sdk
- [x] Реализованы / обновлены тесты на базе tests/mock_server.py
- [x] Политика Fail-Fast соблюдена: ошибки сервера вызывают доменные исключения
```

### 0.4. Antigravity 2.0 Skills & Worktrees (Контекстная гигиена)
* **Worktree Isolation:** Агент `SHALL` учитывать, что сессия запущена в изолированном каталоге Git Worktree.
* **Skills on Demand:** Файлы в директории `specs/` выступают как динамические навыки (Skills). Агент `SHALL NOT` загружать все спецификации разом. При работе над кинематикой загружается только `02-coordinate-math.md`, при работе с сокетами — `01-network-client.md`.

## 1. Environment & Tech Stack (Рабочая Среда)

* **Runtime:** Python 3.10+ (Standard Library).
* **Code Style:** Агент `SHALL` использовать строгие аннотации типов (`Type Hints`) для всех переменных, аргументов и возвращаемых значений (`[Reference Implementation: модуль typing]`).
* **Documentation:** Все публичные классы и методы `SHALL` содержать понятные Docstrings.

## 2. Red Lines (Красные Линии и Табу)

* **Zero-Dependency (Нулевые зависимости):** Агент `SHALL NOT` использовать, импортировать или упоминать сторонние пакеты (например, `requests`, `numpy`, `pydantic`). Запрещается создание файла `requirements.txt`. Допускается использование ТОЛЬКО встроенных модулей ОС (`socket`, `json`, `time`, `math`, `typing`, `hashlib`).
* **No Silent Failures (Запрет на скрытие ошибок):** Агент `SHALL NOT` использовать конструкции `try/except: pass`. При получении `error.code` от сервера, код `SHALL` немедленно выбросить локализованное доменное исключение (Fail-Fast).
* **No Server Emulation (Абстракция от движка):** Агент `SHALL NOT` пытаться симулировать физику, столкновения или инвентарь на стороне клиента. Вся логика SDK сводится к трансформации координат, упаковке команд и сериализации NDJSON.

## 3. Testing & Mocking Tooling (Инструменты тестирования)

Поскольку в данном рабочем пространстве нет доступа к реальному C++ движку Luanti, агент `SHALL` обеспечить автономную тестируемость SDK.

* **Mock Server:** Агент `SHALL` реализовать локальный заглушечный сервер `tests/mock_server.py` на базе стандартного модуля `socketserver`, который умеет принимать TCP-соединения, парсить NDJSON и отвечать по контрактам из `shared_contracts/`.
* **Test Runner:** Все тесты `SHALL` быть написаны с использованием встроенного фреймворка `unittest`.
* **Command:** Запуск тестов `SHALL` производиться исключительно командой: 
  `python -m unittest discover tests`

## 4. i18n Rules (Правила Локализации)

* Ошибки Python, видимые ученику (сообщения исключений, принты), `SHALL NOT` быть захардкожены на английском языке в ядре кода. 
* Агент `SHALL` использовать модуль словарей (`i18n.py`) для извлечения сообщений по ключу машинной ошибки (например, `OUT_OF_BOUNDS -> "Выход за пределы участка!"`).

## 5. Definition of Done (Критерии Готовности)

Задача в этом рабочем пространстве считается выполненной (Done), ТОЛЬКО ЕСЛИ:
1. Не нарушено правило `Zero-Dependency` (нет сторонних импортов).
2. Реализован и запущен `mock_server.py`.
3. Команда `python -m unittest discover tests` завершается с кодом возврата `0` (все тесты зеленые).
4. Проведены тесты разрыва TCP-соединения, и SDK корректно выбрасывает `VoxelConnectionError`.
5. Сформирован отчет для Pull Request по встроенной форме из Раздела 0.3 с таргетом на ветку `dev`.
