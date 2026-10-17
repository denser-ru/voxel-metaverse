---
id: "03-commands-registry"
status: "locked"
depends_on: 
  - "01-network-transport"
  - "02-geometry-and-physics"
provides_context: 
  - "Material Mapping"
  - "Command Payloads"
  - "Error Codes (i18n basis)"
verification_logic: "schema_validation, protocol_fuzzing"
---

# 03-commands-registry: Реестр Команд и Машинных Кодов

> **ABSTRACT:** Спецификация определяет точные JSON-схемы полезной нагрузки (`params` и `data`) для всех сетевых команд между `[[Client Node]]` и `[[Server Node]]`. Также документ задает машинные коды ошибок, обеспечивающие семантическое разделение (Semantic Separation) для мультиязычности.

## 1. Material Mapping (Словарь Материалов)

Для абстрагирования пользователя от технических идентификаторов движка, протокол `SHALL` использовать короткие строковые алиасы для материалов. 
`[[Server Node]]` `SHALL` маппить (преобразовывать) эти алиасы во внутренние типы блоков движка.

* **"air"**: Пустота (удаление блока).
* **"stone"**: Основной строительный блок (камень/булыжник).
* **"brick"**: Кирпичная кладка.
* **"wood"**: Древесина/доски.
* **"glass"**: Прозрачное стекло.
* **"goal"**: Интерактивный целевой блок для испытаний (финиш лабиринта).
* **"red", "green", "blue", "yellow", "white", "black"**: Цветные маркеры (шерсть/бетон).

## 2. Command Payloads (Схемы Команд)

Внимание: все координаты, передаваемые в `params`, `SHALL` находиться строго в Network Space `[0..31]` (согласно `[[02-geometry-and-physics]]`).

### 2.1. Инициализация и Сессия
* **`init_bot`**
  * *Назначение:* Привязка TCP-соединения к Участку и спавн виртуальной сущности.
  * *Params:* `{"x": int, "y": int, "z": int, "heading": int}` (где heading: 0=+X, 1=+Z, 2=-X, 3=-Z).
  * *Data:* `{"plot_size": {"x": 32, "y": 64, "z": 32}}`

### 2.2. Атомарные Действия
* **`step`**
  * *Назначение:* Шаг Черепашки с опциональной установкой блока на предыдущей позиции.
  * *Params:* `{"x": int, "y": int, "z": int, "heading": int, "pen_down": bool, "material": string}`
  * *Data:* `{"local_pos": {"x": int, "y": int, "z": int}, "heading": int}`
* **`set_node`**
  * *Назначение:* Точечная установка блока.
  * *Params:* `{"x": int, "y": int, "z": int, "material": string}`
  * *Data:* `{"success": true}`
* **`get_node`**
  * *Назначение:* Сенсор (проверка препятствия).
  * *Params:* `{"x": int, "y": int, "z": int}`
  * *Data:* `{"material": string, "is_solid": bool, "is_goal": bool}`

### 2.3. Запись и Офлайн-Витрина (Record & Replay)
* **`start_recording`**
  * *Назначение:* Инициализация пустой "пленки" в памяти сервера для данного участка.
  * *Params:* `{}`
  * *Data:* `{"recording": true}`
* **`save_tape`**
  * *Назначение:* Фиксация "пленки" в постоянном хранилище для запуска Гостями (без запущенного Python-скрипта).
  * *Params:* `{}`
  * *Data:* `{"saved_steps": int}`

### 2.4. Инфраструктурные команды
* **`wipe`**
  * *Назначение:* Полная очистка Участка (заполнение `air`).
  * *Params:* `{}`
  * *Data:* `{"cleared": true}`
* **`bulk_set_nodes`**
  * *Назначение:* Оружие массовой застройки для ИИ-Архитектора.
  * *Params:* `{"nodes": [{"x": int, "y": int, "z": int, "material": string}]}`
  * *Data:* `{"success": true, "blocks_queued": int}` (Сервер `SHALL` возвращать статус до фактической отрисовки всех чанков).

## 3. Error Codes Contract (i18n Basis)

КОГДА запрос не может быть выполнен, `[[Server Node]]` `SHALL` вернуть ответ со `status: "error"` и объектом `error`. 
Поле `error.code` `SHALL` содержать один из машинных кодов ниже. `[[Client Node]]` `SHALL` использовать эти коды для выброса локализованных (переведенных на язык пользователя) исключений.

| `error.code` | Server Condition | Client Node Reaction (Fail-Fast) |
| :--- | :--- | :--- |
| `OUT_OF_BOUNDS` | Координаты выходят за пределы `[0..31, 0..63, 0..31]`. | `SHALL` выбросить фатальное исключение границы (BoundaryError). |
| `OBSTACLE_DETECTED` | При попытке `step` бот уперся в твердый блок. | `SHALL` выбросить исключение препятствия (CrashError). |
| `INVALID_PIN` | Переданный `pin_hash` не совпадает с владельцем Участка. | `SHALL` выбросить исключение доступа (AccessDeniedError). |
| `RATE_LIMIT_EXCEEDED`| Превышен лимит команд (100 шт / сек). | `SHALL` инициировать ожидание (Backoff) ИЛИ выбросить исключение. |
| `UNKNOWN_COMMAND` | Запрошен `action`, отсутствующий в реестре. | `SHALL` выбросить исключение протокола. |
| `NOT_RECORDING` | Вызван `save_tape`, но запись не была начата. | `SHALL` вывести предупреждение (Warning). |
