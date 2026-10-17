---
id: "ws2-04-entity-and-physics"
status: "approved"
depends_on:
  - "ws2-00-domain-vision"
  - "ws2-03-plot-geometry"
  - "03-commands-registry" (Shared)
provides_context:
  - "Turtle Entity Registration"
  - "Movement Kinematics & Yaw"
  - "Trailing Block Placement"
  - "Collision Detection (Sensors)"
verification_logic: "entity_spawn_tests, collision_mock_tests"
---

# ws2-04-entity-and-physics: Сущность Робота и Взаимодействие с Физикой

> **ABSTRACT:** Документ определяет визуализацию и кинематику виртуального робота (Черепашки) в мире Luanti. Для обеспечения независимости от гравитации и предотвращения застревания в блоках, робот реализуется как динамическая Lua-сущность (Entity), а не как статический блок (Node).

## 1. Turtle Entity Registration (Регистрация Сущности)

Мод `SHALL` зарегистрировать кастомную сущность `voxel_bot:turtle` (`[Reference Implementation: minetest.register_entity]`).

* **Физические свойства (Physical Properties):**
  * `physical = false`: Сущность `SHALL NOT` подчиняться встроенному физическому движку Luanti (гравитации, инерции). Координаты управляются исключительно алгоритмически из подсистемы очередей.
  * `pointable = false`: Игроки `SHALL NOT` иметь возможности ударить, сдвинуть или взаимодействовать с сущностью вручную.
* **Визуальные свойства:**
  * Сущность `SHALL` иметь 3D-модель (`visual = "mesh"`) и текстуру.
* **Жизненный цикл:**
  * КОГДА сервер обрабатывает команду `init_bot` для `plot_id`, он `SHALL` проверить, существует ли уже сущность робота для данного Участка. ЕСЛИ существует — телепортировать её в новую стартовую точку. ЕСЛИ нет — заспавнить новую сущность (Spawn).

## 2. Movement Kinematics & Yaw (Кинематика и Повороты)

В мире Luanti вращение сущности задается параметром Yaw в радианах. Подсистема `SHALL` транслировать дискретный параметр `heading` (из Network Space) в радианы вращения (Yaw).

* Маппинг направлений `SHALL` выполняться по следующему контракту:
  * `heading == 0` (+X): `yaw = math.pi / 2`
  * `heading == 1` (+Z): `yaw = 0`
  * `heading == 2` (-X): `yaw = -math.pi / 2` (или `3 * math.pi / 2`)
  * `heading == 3` (-Z): `yaw = math.pi`
* КОГДА сущность выполняет команду `step`, она `SHALL` обновить свою глобальную позицию `(X, Y, Z)` и свой угол поворота `yaw` (`[Reference Implementation: entity:set_pos(pos) и entity:set_yaw(yaw)]`).

## 3. Trailing Block Placement (Установка блоков "позади")

Для предотвращения ситуации, когда робот устанавливает блок и оказывается замурованным внутри него, применяется логика "Trailing Placement" (Установка позади).

* КОГДА выполняется команда `step` с параметром `pen_down == true`:
  1. Подсистема `SHALL` запомнить *текущие* (старые) глобальные координаты сущности.
  2. Подсистема `SHALL` переместить сущность на *новые* глобальные координаты (Target Position).
  3. Подсистема `SHALL` установить блок с материалом `material` на *старых* координатах (`[Reference Implementation: minetest.set_node]`).
* Выбор материала `SHALL` строго соответствовать таблице алиасов `Material Mapping` из `[[03-commands-registry]]`.

## 4. Collision Detection (Детектирование столкновений)

Сервер `SHALL` аппаратно (на уровне Lua) проверять физику коллизий до совершения движения (Pre-Step Validation).

* КОГДА обрабатывается команда `step`, сервер `SHALL` запросить свойства блока на целевой позиции (Target Position) через `minetest.get_node`.
* **Obstacle Check:**
  * ЕСЛИ блок является проходимым (`walkable == false` в свойствах ноды, например, `air` или `water`), движение разрешается.
  * ЕСЛИ блок является твердым препятствием (`walkable == true`):
    * Движение `SHALL` быть отменено.
    * Сервер `SHALL` вернуть ответ с ошибкой `error.code = "OBSTACLE_DETECTED"`.
* **Goal Node Check:**
  * ЕСЛИ целевой блок имеет имя `"voxel_bot:goal_node"`, сервер `SHALL` разрешить движение и ОБЯЗАТЕЛЬНО добавить строку `"GOAL_REACHED"` в массив `events` ответа.
