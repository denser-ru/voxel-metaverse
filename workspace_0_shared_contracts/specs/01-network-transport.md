---
id: "01-network-transport"
status: "locked"
depends_on: []
provides_context: 
  - "TCP Transport Configuration"
  - "NDJSON Framing Rules"
  - "Session Lifecycle"
  - "Base Request Schema"
  - "Base Response Schema"
verification_logic: "schema_validation, tcp_framing_tests"
---

# 01-network-transport: Core Networking & Framing Contract

> **ABSTRACT:** Данная спецификация является фундаментальным контрактом взаимодействия между `[[Client Node]]` (SDK) и `[[Server Node]]` (Симуляция). Контракт полностью абстрагирован от языков программирования и описывает исключительно транспортный уровень, управление сессиями и базовые структуры сообщений (JSON Schemas).

## 1. Transport & Framing Protocol

Для обеспечения надежной передачи команд система `SHALL` реализовывать следующий механизм фрейминга:

* **Protocol & Port:** TCP, выделенный порт `4711`.
* **Encoding:** Строго `UTF-8`.
* **Framing Format (NDJSON):** Обмен данными `SHALL` происходить исключительно в формате **JSON Lines (NDJSON)**. Каждое сообщение (Запрос или Ответ) `SHALL` представлять собой валидный цельный JSON-объект, сериализованный строго в одну строку без внутренних переносов.
* **Delimiter:** Концом каждого фрейма (сообщения) `SHALL` выступать ровно один байт перевода строки `\n` (`0x0A`).
* **Interaction Mode (Request-Response):** 
  * `[[Client Node]]` `SHALL` отправлять один запрос и ожидать получения ответа перед отправкой следующего запроса.
  * `[[Server Node]]` `SHALL` обрабатывать сообщения асинхронно, отвечая на валидные фреймы по мере их исполнения.

## 2. Session Lifecycle (Жизненный цикл сессии)

Состояние выполнения алгоритма жестко привязано к жизненному циклу TCP-соединения.

* КОГДА `[[Client Node]]` устанавливает TCP-соединение, `[[Server Node]]` `SHALL` инициализировать новую сессию, очистив все предыдущие незавершенные очереди команд для указанного участка.
* КОГДА TCP-соединение обрывается (закрытие сокета, потеря Keepalive, тайм-аут), `[[Server Node]]` `SHALL` немедленно остановить исполнение текущего алгоритма и сбросить очередь команд (защита от "Zombie Connections").

## 3. Base Request Schema (Client -> Server)

Каждый пакет, отправляемый от клиента к серверу, `SHALL` строго соответствовать следующей JSON-схеме:

```json
{
  "req_id": "integer",
  "meta": {
    "plot_id": "integer",
    "pin_hash": "string",
    "role": "string",
    "host_id": "string",
    "locale": "string"
  },
  "command": {
    "action": "string",
    "params": "object"
  }
}
```

### 3.1. Request Fields Validation:
* `req_id`: Монотонно возрастающий идентификатор запроса в рамках сессии.
* `meta`: Блок авторизации и маршрутизации. 
  * `plot_id`: Идентификатор целевого участка (`1..N`).
  * `pin_hash`: Хэш 4-значного PIN-кода для авторизации доступа к участку.
  * `role`: Задел под Web3/Майнинг (Extension Hook). Для MVP `SHALL` передаваться значение `"owner"`. В будущем поддерживает `"worker"`.
  * `host_id`: Идентификатор клиентского устройства (Telemetry Hook).
  * `locale`: ISO 639-1 код языка клиента (например, `"ru"`, `"en"`). Используется для i18n-закладок.
* `command.action`: Строгое имя команды (определяется в `[[03-commands-registry]]`).
* `command.params`: Объект с аргументами, специфичными для команды.

## 4. Base Response Schema (Server -> Client)

На каждый валидный фрейм запроса сервер `SHALL` ответить ровно одной строкой, соответствующей следующей JSON-схеме:

```json
{
  "req_id": "integer",
  "status": "string",
  "data": "object | null",
  "events": ["string"],
  "quota": {
    "cost": "number",
    "reward": "number"
  },
  "error": "object | null"
}
```

### 4.1. Response Fields Validation:
* `req_id`: Точное эхо идентификатора из запроса.
* `status`: `SHALL` принимать только два значения: `"ok"` или `"error"`.
* `events`: Массив строковых констант произошедших событий (например, `["GOAL_REACHED"]`). ЕСЛИ событий нет, `SHALL` возвращаться пустой массив `[]`.
* `quota`: Блок экономики (Extension Hook). `cost` отражает затраты (топливо), `reward` отражает заработок (майнинг). Для MVP сервер `SHALL` всегда возвращать `{"cost": 0, "reward": 0}`.
* **Mutual Exclusivity Constraint:**
  * ЕСЛИ `status == "ok"`, ТОГДА поле `error` `SHALL` быть `null`, а поле `data` `SHALL` содержать объект ответа.
  * ЕСЛИ `status == "error"`, ТОГДА поле `data` `SHALL` быть `null`, а поле `error` `SHALL` содержать объект с машинным кодом ошибки.
