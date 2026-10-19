---
id: "ws0-agent-rules"
status: "locked"
depends_on:
  - "ws0-project-context"
provides_context: 
  - "Agent Operational Rules"
  - "Red Lines (Taboos)"
  - "Contract Validation Tooling"
  - "Definition of Done (DoD)"
  - "Git Governance & PR Template"
verification_logic: "agent_prompt_injection"
---

# AGENTS: Операционная Конституция и Правила Работы Агента (Shared Contracts)

> **ВНИМАНИЕ, ИИ-АГЕНТ!** 
> Этот документ определяет правила твоей работы в репозитории `shared_contracts`. Ты `SHALL` применять эти инструкции ко всем своим действиям до закрытия сессии. Любое нарушение "Красных Линий" (Red Lines) приведет к глобальному каскадному сбою во всей экосистеме.

## 0. Git & Antigravity 2.0 Governance (Операционный регламент)

Агент в среде Google Antigravity 2.0 `SHALL` строго соблюдать следующие инварианты управления кодовой базой:

### 0.1. Git Identity (Идентификация бота)
Перед выполнением любых Git-операций агент `SHALL` применить локальные настройки авторства:
* `git config user.name "DenserBot [Contracts Architect]"`
* `git config user.email "ai.denser.ru@gmail.com"`

### 0.2. Branching Constraints (Ветвление)
* **Base Branch:** Агент `SHALL` создавать рабочие ветки строго от актуальной ветки `dev`.
* **Branch Naming:** Имя ветки `SHALL` строго следовать маске: `agent/ws0-contracts/<type>-<short-description>`.
* **Prohibited Push:** Агент `SHALL NOT` пушить напрямую в ветки `main` или `dev`.

### 0.3. Pull Request Protocol (Сдача работы)
* **Target Branch:** Целевой веткой любого Pull Request (Base Branch) ВСЕГДА `SHALL` являться ветка `dev`. Агент `SHALL NOT` открывать PR в ветку `main`.
* **Self-Contained PR Form:** Агент `SHALL` генерировать описание Pull Request строго по следующей встроенной форме (без обращения к внешним файлам):

```markdown
### 🤖 Antigravity Agent Pull Request Report

* **Workspace:** `workspace_0_shared_contracts`
* **Agent Role:** `DenserBot [Contracts Architect]`
* **Model Version:** `<УКАЖИ МОДЕЛЬ>`

#### 🛠️ Summary of Contract Changes
- <Кратко перечисли изменения в схемах/спецификациях>

#### 🛡️ Invariant Compliance Checklist
- [x] Целевая ветка строго dev (не main)
- [x] Отсутствуют деструктивные изменения (сохранена обратная совместимость)
- [x] Типы существующих полей в JSON-схемах не изменялись
- [x] Новые поля добавлены строго как аддитивные/опциональные
- [x] Исполняемый код отсутствует (только Markdown и JSON-схемы)
```

## 1. Environment & Tech Stack (Рабочая Среда)

* **Домен:** Системная Архитектура и Проектирование API.
* **Допустимые форматы файлов:** Исключительно Markdown (`.md`) и JSON Schema (`.json`).
* **Языковой агностицизм:** В этом рабочем пространстве `SHALL NOT` присутствовать исполняемый код ни на одном языке программирования (Python, Lua, JS, C++). 
* **Нотация спецификаций:** Агент `SHALL` использовать стандарт EARS (`Ubiquitous`, `Event-driven`, `State-driven`, `Unwanted`) и ключевые слова `SHALL` / `SHALL NOT` (RFC 2119) для описания требований.

## 2. Red Lines (Красные Линии и Табу)

При работе с сетевыми контрактами и схемами, агент `SHALL` соблюдать жесткие правила обратной совместимости (Backward Compatibility).

* **Запрет на деструктивные изменения:** Агент `SHALL NOT` удалять или переименовывать существующие ключи в JSON-схемах (например, `plot_id`, `status`, `events`).
* **Запрет на изменение типов:** Агент `SHALL NOT` изменять типы данных существующих полей (например, менять `integer` на `string`).
* **Правило расширения (Additive Changes Only):** ЕСЛИ требуется внедрить новый функционал, агент `SHALL` использовать исключительно аддитивный подход (добавление новых опциональных полей) ИЛИ создание новой мажорной версии протокола.
* **Семантическое разделение:** Агент `SHALL NOT` внедрять передачу человекочитаемого текста (сообщений об ошибках) в протокол. Все тексты `SHALL` передаваться строго в виде машинных кодов-констант (например, `OUT_OF_BOUNDS`).

## 3. Validation Tooling (Инструменты проверки)

Перед тем как отметить задачу как выполненную, агент `SHALL` проверить консистентность контрактов с использованием стандартных инструментов валидации.

* **Линтинг Markdown:** Проверка связности ссылок (Broken Links) и структуры `[Reference Implementation: markdownlint-cli]`.
* **Валидация JSON:** ЕСЛИ в спецификации обновляются структуры JSON, агент `SHALL` извлечь их и проверить на синтаксическую корректность (`[Reference Implementation: jq '.' или ajv compile]`).
* **Проверка пересечений:** Агент `SHALL` убедиться, что ни один код ошибки из `[[03-commands-registry]]` не дублирует другой.

## 4. Definition of Done (Критерии Готовности)

Любая модификация в данном рабочем пространстве считается завершенной (Done), ТОЛЬКО ЕСЛИ:
1. Изменения не нарушают "Red Lines" (Раздел 2).
2. Обновлены все связанные документы (например, при добавлении новой команды в `03-commands-registry.md` обновлен глоссарий в `PROJECT.md`, если необходимо).
3. Документ содержит актуальный блок `YAML Front Matter` с корректными `depends_on`.
4. Сформирован отчет для Pull Request по форме из Раздела 0.3 с таргетом на ветку `dev`.
