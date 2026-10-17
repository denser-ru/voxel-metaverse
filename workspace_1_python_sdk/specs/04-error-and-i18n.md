---
id: "ws1-04-error-and-i18n"
status: "approved"
depends_on:
  - "03-commands-registry"
  - "ws1-01-network-client"
provides_context:
  - "Fail-Fast Policy"
  - "Exception Hierarchy"
  - "i18n Localization Dictionaries"
verification_logic: "exception_raising_tests, localization_mock_tests"
---

# ws1-04-error-and-i18n: Обработка Ошибок и Локализация (i18n)

> **ABSTRACT:** Документ задает строгие правила обработки нештатных ситуаций в `[[Client Node]]`. Спецификация обязывает применять политику Fail-Fast для защиты от рассинхронизации состояния (State Desync) и определяет механизм локализации сообщений об ошибках на основе машинных кодов.

## 1. Fail-Fast Policy (Политика мгновенного отказа)

Для предотвращения ситуации «Слепой Черепахи» (когда скрипт продолжает выполняться, хотя бот уперся в стену в виртуальном мире), SDK `SHALL` использовать политику Fail-Fast.

* КОГДА транспортный слой получает от `[[Server Node]]` пакет, в котором `status == "error"`, SDK `SHALL NOT` игнорировать его или возвращать `False`.
* SDK `SHALL` немедленно прервать выполнение текущего метода (например, `_single_step()`) и выбросить (raise) типизированное исключение.
* Дальнейшее выполнение скрипта ученика `SHALL` быть остановлено, если только ученик явно не обернул вызов в блок `try/except`.

## 2. Exception Hierarchy (Иерархия Исключений)

SDK `SHALL` определять собственную иерархию исключений, наследуемую от базового класса `VoxelTurtleError`.
Модуль `i18n.py` (или аналогичный компонент) `SHALL` маппить (проецировать) машинные коды `error.code` из `[[03-commands-registry]]` в конкретные классы исключений:

| Машинный код (`error.code`) | Класс исключения SDK |
| :--- | :--- |
| `OUT_OF_BOUNDS` | `PlotBoundaryError(VoxelTurtleError)` |
| `OBSTACLE_DETECTED` | `ObstacleCrashError(VoxelTurtleError)` |
| `INVALID_PIN` | `AccessDeniedError(VoxelTurtleError)` |
| `UNKNOWN_COMMAND`, `PROTOCOL_ERROR` | `ProtocolError(VoxelTurtleError)` |

*(Примечание: Сетевые ошибки `VoxelTimeoutError` и `VoxelConnectionError` генерируются локально транспортным слоем согласно `[[ws1-01-network-client]]`, минуя маппинг машинных кодов).*

## 3. i18n Localization Dictionaries (Локализация сообщений)

SDK `SHALL` быть спроектирован с учетом поддержки нескольких языков (i18n). 

* **Инициализация локали:** Класс `Turtle` `SHALL` принимать опциональный строковый параметр `lang` (по умолчанию `"ru"`).
* **Словари:** SDK `SHALL` хранить локализованные человекочитаемые сообщения во внутренних структурах данных (`[Reference Implementation: вложенный Python dict]`), без использования внешних библиотек (Zero-Dependency).
* **Разрешение текста (Text Resolution):**
  * КОГДА SDK выбрасывает исключение, он `SHALL` извлечь текст ошибки из словаря по ключу `[lang][error.code]`.
  * ЕСЛИ указанный язык или код отсутствует в словаре, SDK `SHALL` использовать фоллбэк (Fallback) на базовый язык (`"en"`) и возвращать сырой машинный код.

### 3.1. Требуемый минимальный словарь (Reference)

Модуль локализации `SHALL` содержать минимум две языковые ветки (`ru` и `en`) со следующими семантическими переводами:

* **`OUT_OF_BOUNDS`**
  * `ru`: *"Черепашка попыталась выйти за пределы разрешенного участка!"*
  * `en`: *"The turtle attempted to move outside the plot boundaries!"*
* **`OBSTACLE_DETECTED`**
  * `ru`: *"Авария! Черепашка врезалась в твердый блок."*
  * `en`: *"Crash! The turtle hit a solid block."*
* **`INVALID_PIN`**
  * `ru`: *"Отказано в доступе. Неверный PIN-код участка."*
  * `en`: *"Access denied. Invalid plot PIN code."*
