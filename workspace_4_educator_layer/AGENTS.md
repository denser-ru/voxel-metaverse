---
id: "ws4-agent-rules"
status: "locked"
depends_on:
  - "ws4-project-context"
provides_context: 
  - "Educator Operational Rules"
  - "Content i18n Taboos"
  - "Code Zoning Verification"
  - "Definition of Done (DoD)"
  - "Git Governance & Embedded PR Template"
verification_logic: "agent_prompt_injection"
---

# AGENTS: Операционная Конституция и Правила Работы Агента (Educator Layer)

> **ВНИМАНИЕ, ИИ-АГЕНТ!** 
> Этот документ определяет правила твоей работы в репозитории `educator-layer`. Ты `SHALL` применять эти инструкции ко всем своим действиям. Твоя задача — создавать надежные, дидактически правильные шаблоны уроков, которые невозможно случайно сломать, и которые идеально переведены на разные языки без поломки синтаксиса.

## 0. Git & Antigravity 2.0 Governance (Операционный регламент)

Агент в среде Google Antigravity 2.0 `SHALL` строго соблюдать следующие инварианты управления кодовой базой:

### 0.1. Git Identity (Идентификация бота)
Перед выполнением любых Git-операций агент `SHALL` применить локальные настройки авторства:
* `git config user.name "DenserBot [Educator]"`
* `git config user.email "ai.denser.ru@gmail.com"`

### 0.2. Branching Constraints (Ветвление)
* **Base Branch:** Агент `SHALL` создавать рабочие ветки строго от актуальной ветки `dev`.
* **Branch Naming:** Имя ветки `SHALL` строго следовать маске: `agent/ws4-tasks/<type>-<short-description>`.
* **Prohibited Push:** Агент `SHALL NOT` пушить напрямую в ветки `main` или `dev`.

### 0.3. Pull Request Protocol (Сдача работы)
* **Target Branch:** Целевой веткой любого Pull Request (Base Branch) ВСЕГДА `SHALL` являться ветка `dev`. Агент `SHALL NOT` открывать PR в ветку `main`.
* **Self-Contained PR Form:** Агент `SHALL` генерировать описание Pull Request строго по следующей встроенной форме (без обращения к файлам за пределами своей рабочей директории):

```markdown
### 🤖 Antigravity Agent Pull Request Report

* **Workspace:** `workspace_4_educator_layer`
* **Agent Role:** `DenserBot [Educator]`
* **Target Spec:** `specs/<УКАЖИ_ИМЯ_СПЕЦИФИКАЦИИ.md>`
* **Model Version:** `<УКАЖИ_МОДЕЛЬ>`

#### 🛠️ Summary of Changes
- <Кратко перечисли созданные или обновленные файлы уроков>

#### 🧪 Verification Output (Syntax & Zoning Checks)
```text
<Вставь сюда сырой вывод компиляции: python -m py_compile content/<lang>/<task_file>.py>
```

#### 🛡️ Invariant Compliance Checklist
- [x] Целевая ветка строго dev (не main)
- [x] Code Zoning: В файле присутствуют точные строковые маркеры # --- НАЧАЛО КОДА УЧЕНИКА --- и # --- КОНЕЦ КОДА УЧЕНИКА ---
- [x] SDK Immutability: Исходный код библиотеки voxel_turtle не модифицировался
- [x] Content i18n Taboo: Синтаксис Python, методы SDK и алиасы материалов (например, "stone") оставлены на английском
- [x] Нагрузка скрыта: Вызовы AdminBuilder / bulk_set_nodes изолированы в Setup Zone до кода ученика
- [x] Простота языка: В комментариях-подсказках (TODO) отсутствует сложная академическая терминология
```

### 0.4. Antigravity 2.0 Skills & Worktrees (Контекстная гигиена)
* **Worktree Isolation:** Агент `SHALL` учитывать, что сессия запущена в изолированном каталоге Git Worktree.
* **Skills on Demand:** Файлы в директории `specs/` выступают как динамические навыки (Skills). Агент `SHALL NOT` загружать все спецификации разом. При работе над шаблоном урока загружается `01-task-template-contract.md`, при переводе на другие языки — `04-content-i18n.md`.

## 1. Environment & Tech Stack (Рабочая Среда)

* **Runtime:** Python 3.10+ (для валидации учебных скриптов).
* **Dependencies:** Доступен только готовый (Read-Only) пакет `voxel_turtle` из `[[Python SDK]]`.
* **Content Structure:** Файлы уроков `SHALL` располагаться строго в директориях локалей (`content/ru/`, `content/en/`).

## 2. Red Lines (Красные Линии и Табу)

### 2.1. Code Integrity (Неприкосновенность SDK)
* Агент `SHALL NOT` модифицировать, патчить или переопределять исходный код библиотеки `voxel_turtle`.
* Любые учебные скрипты `SHALL` использовать исключительно утвержденный публичный API SDK.

### 2.2. Content Localization Taboos (Запреты при переводе)
* КОГДА агент генерирует версию урока для новой локали (например, копирует `en/task_01.py` в `ru/task_01.py`), он `SHALL NOT` переводить синтаксис языка Python, имена классов, имена методов или аргументы протокола.
* Алиасы материалов `SHALL` оставаться неизменными (`[Reference Implementation: bot.color("stone") ЗАПРЕЩЕНО переводить как bot.color("камень")]`).
* Переводу `SHALL` подлежать ИСКЛЮЧИТЕЛЬНО текстовые комментарии (`# ...`) и строковые литералы внутри функций `print()`.

### 2.3. Complexity Ceiling (Потолок сложности)
* В комментариях-подсказках (TODO) агент `SHALL NOT` использовать сложную инженерную терминологию (например, "идемпотентность", "инстанцирование").
* Подсказки `SHALL` формулироваться в формате прямых действий (например, "Используй цикл, чтобы повторить это 5 раз").

## 3. Zoning & Validation Tooling (Инструменты проверки)

Перед сохранением любого файла урока, агент `SHALL` валидировать его архитектуру:

* **Zoning Check (Проверка зон):** Агент `SHALL` убедиться (через regex или AST парсинг), что файл содержит точные строковые маркеры `# --- НАЧАЛО КОДА УЧЕНИКА ---` и `# --- КОНЕЦ КОДА УЧЕНИКА ---`.
* **Dry-Run Test (Холостой прогон):** Агент `SHALL` иметь эталонное решение (Reference Solution) для каждой задачи. Эталонное решение `SHALL` подставляться в Зону Ученика, после чего скрипт `SHALL` успешно исполняться (на мок-сервере) без синтаксических или логических ошибок.

## 4. Definition of Done (Критерии Готовности)

Задача в этом рабочем пространстве считается выполненной (Done), ТОЛЬКО ЕСЛИ:
1. Создан файл урока, который успешно проходит синтаксический анализ (`python -m py_compile`).
2. В файле жестко разделены Setup Zone, Student Zone и Validation Zone.
3. Локализация применена ТОЛЬКО к человекочитаемому тексту.
4. Использование `AdminBuilder` скрыто в Setup Zone (до маркера начала кода ученика).
5. Сформирован отчет для Pull Request по встроенной форме из Раздела 0.3 с таргетом на ветку `dev`.
