---
id: "ws1-02-coordinate-math"
status: "approved"
depends_on:
  - "02-geometry-and-physics"
  - "ws1-00-domain-vision"
provides_context:
  - "Virtual Origin Shift"
  - "Heading State Machine"
  - "Kinematics & Motion Deltas"
verification_logic: "pure_function_unit_tests"
---

# ws1-02-coordinate-math: Математический Движок и Преобразование Координат

> **ABSTRACT:** Данная спецификация описывает алгоритмы пространственной навигации (Кинематику) и трансляцию систем координат. Модуль `math_engine.py` `SHALL` выступать как набор чистых функций (Pure Functions) без побочных эффектов, что обеспечит 100% покрытие Unit-тестами без необходимости инициализации сетевых соединений.

## 1. Virtual Origin Shift (Сдвиг начала координат)

Чтобы обеспечить ученику привычную декартову систему с нулем в центре (User Space), а `[[Server Node]]` — сырые положительные массивы (Network Space), SDK `SHALL` реализовывать двунаправленную трансляцию.

* **User Space to Network Space (Для отправки запросов):**
  * КОГДА SDK подготавливает полезную нагрузку (payload) для сетевого слоя, математический движок `SHALL` применить формулы:
    * $X_{net} = X_{user} + 15$
    * $Z_{net} = Z_{user} + 15$
    * $Y_{net} = Y_{user}$
* **Network Space to User Space (Для чтения ответов):**
  * КОГДА SDK получает актуальные координаты от сервера в блоке `data.local_pos`, он `SHALL` инвертировать сдвиг перед тем, как обновить внутреннее состояние и вернуть значения ученику:
    * $X_{user} = X_{net} - 15$
    * $Z_{user} = Z_{net} - 15$
    * $Y_{user} = Y_{net}$

## 2. Heading State Machine (Управление направлением)

Черепашка оперирует 4-позиционным компасом (Heading).
Значения компаса строго ограничены: `0` (Восток / +X), `1` (Север / +Z), `2` (Запад / -X), `3` (Юг / -Z).

* **Rotation (Повороты):** Ученик передает углы в градусах (например, `90`, `180`, `-90`). SDK `SHALL` преобразовывать их в новые значения компаса:
  * **Turn Left (Налево / Против часовой стрелки):**
    Формула: `new_heading = (current_heading + (angle // 90)) % 4`
  * **Turn Right (Направо / По часовой стрелке):**
    Формула: `new_heading = (current_heading - (angle // 90)) % 4`
* *Примечание:* Если переданы углы, не кратные 90 (например, `45`), SDK `SHALL` использовать целочисленное деление `// 90`, чтобы избежать некорректных состояний компаса в воксельной сетке.

## 3. Kinematics & Motion Deltas (Смещение позиций)

КОГДА ученик вызывает команды движения (`forward(distance)`, `backward(distance)`), SDK `SHALL` вычислить целевую позицию (Target Position) в User Space перед отправкой пакета.

* **Горизонтальное движение (в зависимости от `heading`):**
  * ЕСЛИ `heading == 0`, ТОГДА `dx = distance, dz = 0`
  * ЕСЛИ `heading == 1`, ТОГДА `dx = 0, dz = distance`
  * ЕСЛИ `heading == 2`, ТОГДА `dx = -distance, dz = 0`
  * ЕСЛИ `heading == 3`, ТОГДА `dx = 0, dz = -distance`
* **Вертикальное движение (`up`, `down`):**
  * `up(distance)`: `dy = distance`
  * `down(distance)`: `dy = -distance`
* **Target Application:** Новая позиция вычисляется как $X_{new} = X_{current} \pm dx$ (и аналогично для $Y$ и $Z$).

## 4. Bounding Box Pre-Validation (Пре-валидация границ)

Для реализации паттерна Fail-Fast (до отправки сетевого запроса), математический движок `SHALL` содержать функцию проверки границ User Space:
* Допустимые границы: $X \in [-15..15]$, $Z \in [-15..15]$, $Y \in [0..63]$.
* ЕСЛИ вычисленная целевая позиция `Target Position` нарушает эти границы, SDK `SHALL NOT` отправлять сетевой запрос, а немедленно выбросить локальное исключение границы (`BoundaryError`).
