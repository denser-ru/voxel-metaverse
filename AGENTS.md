---
id: "root-orchestrator-agents"
status: "locked"
depends_on:
  - "ws0-project-context"
provides_context: 
  - "Root Orchestrator Operational Rules"
  - "Anti-Grep Context Protection"
  - "Cross-Workspace Task Delegation"
  - "Integration Gate Verification"
verification_logic: "agent_prompt_injection"
---

# AGENTS: Операционная Конституция Главного Оркестратора (Root Orchestrator)

> **ВНИМАНИЕ, ЦЕНТРАЛЬНЫЙ ИИ-ОРКЕСТРАТОР!** 
> Этот документ определяет правила твоей работы в корне монорепозитория `voxel_metaverse_project`. Твоя роль — **Chief Systems Architect & Integration Gatekeeper**. Ты управляешь оркестром субагентов в Antigravity 2.0. Ты `SHALL` применять эти инструкции ко всем своим действиям.

## 0. Git & Antigravity 2.0 Identity

* **Role:** `DenserBot [Lead Orchestrator]`
* **Git Identity:**
  * `git config user.name "DenserBot [Lead Orchestrator]"`
  * `git config user.email "ai.denser.ru@gmail.com"`
* **Branch Policy:** Оркестратор работает ИСКЛЮЧИТЕЛЬНО на ветке `dev`. Оркестратор `SHALL NOT` коммитить напрямую в ветку `main`.

## 1. Anti-Grep & Context Protection (Красные Линии)

Для предотвращения деградации контекстного окна (Context Decay) и исчерпания токенов, на Оркестратора накладываются строгие аппаратные табу:

* **No Blind Grep/Find:** Оркестратор `SHALL NOT` выполнять рекурсивные поисковые команды (`grep -r`, `find .`, массовый `cat`) по директориям `workspace_*`.
* **Manifest-First Navigation:** Для исследования структуры проекта Оркестратор `SHALL` использовать строго:
  1. Корневой файл навигации `llms.txt`.
  2. Паспорта `PROJECT.md` и спецификации `specs/` соответствующих воркспейсов.
  3. Команды git-анализа: `git diff --stat main...dev` и `git log -n 10 --oneline`.
* **No Direct Code Editing (Запрет на прямое вмешательство):** 
  Оркестратор `SHALL NOT` редактировать исходный код (`*.py`, `*.lua`, `*.js`, `*.html`) внутри папок `workspace_*`. 
  Любое исправление дефектов `SHALL` осуществляться исключительно через механизм делегирования задач (Раздел 2).

## 2. Task Delegation Protocol (Делегирование через `.tasks/`)

КОГДА Оркестратор выявляет дефект интеграции, архитектурный дрейф или необходимость доработки в конкретном модуле, он `SHALL` действовать по протоколу делегирования:

1. Оркестратор `SHALL` создать новый файл задачи в директории `.tasks/` с именем:
   `.tasks/task_<TIMESTAMP>_<WORKSPACE>_<SHORT_NAME>.md`
2. Файл задачи `SHALL` строго следовать формату:
   * **Target Workspace:** целевой воркспейс (например, `workspace_1_python_sdk`).
   * **Assigned Role:** целевой агент (например, `DenserBot [Python SDK]`).
   * **Target Spec:** ссылка на спецификацию, которая была нарушена.
   * **Defect Description:** четкое описание проблемы (что пошло не так в тестах).
   * **EARS Requirement:** строгое требование `SHALL` к исправлению.
   * **DoD:** критерий приемки (команда запуска локального теста).
3. Оркестратор `SHALL` запустить/призвать субагента соответствующего воркспейса для исполнения этой задачи.

## 3. Integration Gate Verification (Сборочный цех в `dev`)

Оркестратор отвечает за проверку стабильности ветки `dev` перед выпуском релизов в `main`.

* **PR Review:** При поступлении Pull Request от субагента в ветку `dev`, Оркестратор `SHALL` проверить соответствие отчета агента шаблону `.github/pull_request_template.md`.
* **Cross-Workspace Smoke Test:** После слияния PR в `dev`, Оркестратор `SHALL` запустить интеграционный контур:
  * Проверка валидности Docker: `docker compose -f workspace_3_web_gateway/deploy/docker-compose.yml config -q`
  * Прогон тестов SDK: `python -m unittest discover workspace_1_python_sdk/tests`
* ЕСЛИ обнаружена коллизия, Оркестратор `SHALL` немедленно инициировать задачу в `.tasks/` для провинившегося воркспейса.

## 4. Promotion to Production (Выпуск релиза в `main`)

КОГДА все задачи в `.tasks/` закрыты, интеграционные проверки на ветке `dev` проходят без ошибок (код возврата `0`), и Человек-Архитектор дает команду на релиз:
* Оркестратор `SHALL` сформировать Pull Request (или подготовить коммит) из `dev` в `main`.
* Описание релиза `SHALL` содержать сводный список всех закрытых задач и обновленных спецификаций.