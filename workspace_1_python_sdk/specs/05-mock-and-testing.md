---
id: "ws1-05-mock-and-testing"
status: "approved"
depends_on:
  - "ws1-01-network-client"
  - "ws1-02-coordinate-math"
  - "ws1-03-turtle-public-api"
  - "ws1-04-error-and-i18n"
provides_context:
  - "Mock Server Implementation"
  - "Test Coverage Requirements"
  - "Integration Scenarios"
verification_logic: "pytest_execution, coverage_report"
---

# ws1-05-mock-and-testing: Стратегия Тестирования и Локальный Mock-Сервер

> **ABSTRACT:** Спецификация определяет требования к тестовому покрытию SDK. Для обеспечения независимости от реального `[[Server Node]]`, агенты `SHALL` реализовать локальный TCP Mock-сервер. Документ задает тестовые сценарии (Test Cases) для проверки правильности преобразования координат и соблюдения политики Fail-Fast.

## 1. Local Mock Server (Эмулятор Сервера)

Для проведения интеграционных тестов без внешних зависимостей, в директории `tests/` `SHALL` быть реализован скрипт эмулятора сервера (`mock_server.py`).

* **Технологический стек:** Mock-сервер `SHALL` быть написан на чистом Python, используя стандартные модули (`[Reference Implementation: socketserver, threading]`).
* **Поведение (Behavior):**
  * Сервер `SHALL` подниматься на локальном хосте (например, `127.0.0.1`) на динамически назначенном порту перед запуском тестов и корректно завершаться после них.
  * Сервер `SHALL` принимать TCP-соединения, читать NDJSON построчно (по символу `\n`) и декодировать запросы.
  * На запрос `init_bot` сервер `SHALL` возвращать мок-ответ: `{"req_id": <id>, "status": "ok", "data": {"plot_size": {"x":32,"y":64,"z":32}, "local_pos": {"x":15, "y":0, "z":15}}, "events": [], "quota": {"cost":0,"reward":0}, "error": null}`.
  * Сервер `SHALL` предоставлять метод для инжектирования ошибок (Fault Injection), чтобы в определенных тестах намеренно возвращать `status: "error"`.

## 2. Test Coverage Requirements (Требования к покрытию)

Тестовый набор `SHALL` использовать стандартные фреймворки тестирования (`[Reference Implementation: unittest или pytest]`). Тесты `SHALL` покрывать следующие критические домены:

### 2.1. Coordinate Translation Tests (Тесты геометрии)
* **Сценарий 1:** КОГДА вызывается `bot.forward(5)` при начальном состоянии (User Space `0,0,0`, `heading = 0`), ТОГДА отправленный JSON `SHALL` содержать координаты Network Space: `x=20, y=0, z=15`.
* **Сценарий 2:** КОГДА вызывается `bot.right(90)` из `heading = 0`, ТОГДА `heading` `SHALL` стать `3` (Юг), а сетевой запрос `SHALL NOT` отправляться.

### 2.2. Protocol & Framing Tests (Тесты транспорта)
* **Сценарий 3:** КОГДА Mock-сервер отправляет ответ, разбитый на два TCP-пакета (фрагментация до символа `\n`), транспортный слой SDK `SHALL` корректно склеить их в буфере и десериализовать.
* **Сценарий 4:** КОГДА Mock-сервер обрывает соединение (Close Socket), SDK `SHALL` выбросить исключение `VoxelConnectionError`.

### 2.3. Fail-Fast & i18n Tests (Тесты исключений)
* **Сценарий 5:** КОГДА Mock-сервер отвечает на команду `step` ошибкой с кодом `OUT_OF_BOUNDS`, метод `forward()` `SHALL` немедленно прерваться и выбросить исключение `PlotBoundaryError`.
* **Сценарий 6:** КОГДА локаль установлена в `"ru"`, сообщение выброшенного исключения `SHALL` содержать русскоязычный текст из словаря переводов.

## 3. Atomic Stepping Validation (Валидация декомпозиции)

Для проверки визуальной плавности, тесты `SHALL` верифицировать механику разделения шагов.

* КОГДА вызывается `bot.forward(3)`, ТОГДА Mock-сервер `SHALL` зафиксировать ровно 3 отдельных входящих запроса с `action="step"`.
* КОГДА вызывается метод `AdminBuilder.build_from_json(nodes)`, ТОГДА Mock-сервер `SHALL` зафиксировать ровно 1 запрос с `action="bulk_set_nodes"`, содержащий весь массив блоков.
