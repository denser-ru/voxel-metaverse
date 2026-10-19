---
id: "ws2-agent-rules"
status: "locked"
depends_on:
  - "ws2-project-context"
provides_context: 
  - "Agent Operational Rules"
  - "Red Lines (Taboos)"
  - "Fault Tolerance (pcall)"
  - "Definition of Done (DoD)"
  - "Git Governance & Embedded PR Template"
verification_logic: "agent_prompt_injection"
---

# AGENTS: Операционная Конституция и Правила Работы Агента (Luanti Server Mod)

> **ВНИМАНИЕ, ИИ-АГЕНТ!** 
> Этот документ определяет правила твоей работы в репозитории `luanti-mod`. Ты `SHALL` применять эти инструкции ко всем своим действиям до закрытия сессии. Твоя задача — написать сверхнадежный серверный код, который невозможно "положить" некорректными сетевыми пакетами или DDoS-атаками.

## 0. Git & Antigravity 2.0 Governance (Операционный регламент)

Агент в среде Google Antigravity 2.0 `SHALL` строго соблюдать следующие инварианты управления кодовой базой:

### 0.1. Git Identity (Идентификация бота)
Перед выполнением любых Git-операций агент `SHALL` применить локальные настройки авторства:
* `git config user.name "DenserBot [Luanti Mod]"`
* `git config user.email "ai.denser.ru@gmail.com"`

### 0.2. Branching Constraints (Ветвление)
* **Base Branch:** Агент `SHALL` создавать рабочие ветки строго от актуальной ветки `dev`.
* **Branch Naming:** Имя ветки `SHALL` строго следовать маске: `agent/ws2-mod/<type>-<short-description>`.
* **Prohibited Push:** Агент `SHALL NOT` пушить напрямую в ветки `main` или `dev`.

### 0.3. Pull Request Protocol (Сдача работы)
* **Target Branch:** Целевой веткой любого Pull Request (Base Branch) ВСЕГДА `SHALL` являться ветка `dev`. Агент `SHALL NOT` открывать PR в ветку `main`.
* **Self-Contained PR Form:** Агент `SHALL` генерировать описание Pull Request строго по следующей встроенной форме (без обращения к файлам за пределами своей рабочей директории):

```markdown
### 🤖 Antigravity Agent Pull Request Report

* **Workspace:** `workspace_2_luanti_mod`
* **Agent Role:** `DenserBot [Luanti Mod]`
* **Target Spec:** `specs/<УКАЖИ_ИМЯ_СПЕЦИФИКАЦИИ.md>`
* **Model Version:** `<УКАЖИ_МОДЕЛЬ>`

#### 🛠️ Summary of Changes
- <Кратко перечисли изменения в серверном моде>

#### 🧪 Verification Output (luacheck)
```text
<Вставь сюда сырой вывод выполнения: luacheck src/ --globals minetest voxel_bot>
```

#### 🛡️ Invariant Compliance Checklist
- [x] Целевая ветка строго dev (не main)
- [x] Zero-Lag Policy: Все сокеты переведены в неблокирующий режим через settimeout(0)
- [x] Fault Tolerance: Все вызовы minetest.parse_json обернуты в pcall
- [x] Scope Isolation: Отсутствуют случайные глобальные переменные (только local и _G.voxel_bot)
- [x] Изменения затронули только файлы внутри workspace_2_luanti_mod
- [x] Нет синхронных дисковых операций (io.open / create_schematic) внутри тика globalstep
```

### 0.4. Antigravity 2.0 Skills & Worktrees (Контекстная гигиена)
* **Worktree Isolation:** Агент `SHALL` учитывать, что сессия запущена в изолированном каталоге Git Worktree.
* **Skills on Demand:** Файлы в директории `specs/` выступают как динамические навыки (Skills). Агент `SHALL NOT` загружать все спецификации разом. При работе с сокетами загружается `02-network-ingress.md`, при работе с очередями — `05-safety-guardrails.md`.

## 1. Environment & Tech Stack (Рабочая Среда)

* **Runtime:** Движок Luanti 5.8+ (интерпретатор Lua 5.1 / LuaJIT).
* **API:** Стандартный `Luanti Server API`.
* **Scope Isolation:** Агент `SHALL` использовать строго локальные переменные и функции (`local`). Загрязнение глобальной области видимости `SHALL NOT` допускаться. Допускается экспорт только одной глобальной таблицы-пространства имен (`[Reference Implementation: _G.voxel_bot = {}]`).

## 2. Red Lines (Красные Линии и Табу)

* **Zero-Lag Invariant (Запрет на блокирующий I/O):** Агент `SHALL NOT` использовать блокирующие сетевые вызовы в основном потоке. Все TCP-сокеты (слушающие и клиентские) `SHALL` быть принудительно переведены в неблокирующий режим (`[Reference Implementation: socket:settimeout(0)]`).
* **Fault Tolerance (Защита от крашей):** Любой парсинг входящих сетевых данных (JSON) `SHALL` считаться недоверенным (Untrusted). Вызов десериализатора `SHALL` быть обернут в защищенный вызов (`[Reference Implementation: pcall(minetest.parse_json, raw_data)]`). Падение мода из-за некорректного JSON от клиента `SHALL NOT` допускаться.
* **No Disk I/O in Main Loop (Запрет на синхронную работу с диском):** Агент `SHALL NOT` использовать `io.open`, `minetest.create_schematic` с сохранением в файл или запись в `Mod Storage` внутри высокочастотных циклов (например, при каждом шаге бота). Персистентные сохранения `SHALL` выполняться только по явным триггерам (например, `save_tape` или `shutdown`).
* **Time Slicing (Ограничение цикла):** Агент `SHALL NOT` использовать тяжелые циклы `for`/`while`, способные занять более 10 миллисекунд. Любые массовые операции с блоками `SHALL` быть разбиты на чанки и разнесены по тикам `globalstep`.

## 3. Testing & Linting Tooling (Инструменты проверки)

Ввиду динамической типизации Lua, агент `SHALL` применять строгий статический анализ кода.

* **Linter:** Весь генерируемый код `SHALL` проходить проверку линтером `luacheck`.
* **Command:** Запуск проверки `SHALL` производиться командой:
  `luacheck src/ --globals minetest voxel_bot`
* Код `SHALL NOT` содержать предупреждений (Warnings) о неиспользуемых переменных, теневом копировании (shadowing) или доступе к неопределенным глобальным переменным.

## 4. Definition of Done (Критерии Готовности)

Задача в этом рабочем пространстве считается выполненной (Done), ТОЛЬКО ЕСЛИ:
1. Линтер `luacheck` завершается с кодом возврата `0` (нет ошибок и предупреждений).
2. Все вызовы `minetest.parse_json` защищены через `pcall`.
3. Все сокеты инициализируются с `settimeout(0)`.
4. В коде отсутствуют глобальные переменные, кроме таблицы мода.
5. Сформирован отчет для Pull Request по встроенной форме из Раздела 0.3 с таргетом на ветку `dev`.
