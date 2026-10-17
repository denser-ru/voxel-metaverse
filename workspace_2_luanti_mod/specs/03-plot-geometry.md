---
id: "ws2-03-plot-geometry"
status: "approved"
depends_on:
  - "ws2-00-domain-vision"
  - "02-geometry-and-physics" (Shared)
provides_context:
  - "Grid Math & Plot Origin"
  - "Coordinate Transformation"
  - "Invisible Barrier Node Registration"
  - "Plot Infrastructure Generation"
verification_logic: "math_formula_tests, mapgen_boundary_check"
---

# ws2-03-plot-geometry: Математика Сетки и Физика Границ

> **ABSTRACT:** Спецификация определяет подсистему `plot_manager`. Документ задает математические формулы для распределения Участков (`plot_id`) в глобальном мире Luanti, алгоритмы валидации координат и контракт физической защиты (генерация невидимых барьеров).

## 1. Grid Math & Plot Origin (Вычисление начальной точки Участка)

Глобальный мир Luanti `SHALL` быть разделен на двумерную сетку. Подсистема `SHALL` использовать следующие константы для вычисления:
* `PLOT_SIZE = 32` (Рабочая зона).
* `ROAD_WIDTH = 6` (Ширина нейтральной полосы).
* `STEP = 38` (Общий шаг сетки: `PLOT_SIZE + ROAD_WIDTH`).
* `GRID_COLS = 10` (Количество участков в одном ряду по оси X).

КОГДА требуется вычислить глобальную точку отсчета (Origin) $X_0, Y_0, Z_0$ для заданного `plot_id` (где $plot\_id \ge 1$), подсистема `SHALL` использовать формулы:
* `col = (plot_id - 1) % GRID_COLS`
* `row = math.floor((plot_id - 1) / GRID_COLS)`
* $X_0 = col \times STEP$
* $Y_0 = 1$ (Уровень земли $Y=0$ зарезервирован под пол, рабочая зона начинается с $Y=1$).
* $Z_0 = row \times STEP$

## 2. Coordinate Transformation (Валидация и Трансляция)

КОГДА сетевой шлюз получает команду, содержащую координаты `(x, y, z)` из Network Space, подсистема `plot_manager` `SHALL` выполнить их валидацию и перевод в Global Space.

* **Bounds Check (Проверка границ):** 
  Подсистема `SHALL` убедиться, что $x \in [0..31]$, $z \in [0..31]$, $y \in [0..63]$. 
  ЕСЛИ условие нарушено, команда `SHALL` быть отклонена с ошибкой `error.code = "OUT_OF_BOUNDS"`.
* **Translation (Перевод):**
  Глобальные координаты блока в мире Luanti `SHALL` вычисляться как:
  * $X_{global} = X_0 + x$
  * $Y_{global} = Y_0 + y$
  * $Z_{global} = Z_0 + z$

## 3. Invisible Barrier Node Registration (Защитный барьер)

Для реализации инварианта "Изоляция состояний" из `[[ws2-00-domain-vision]]`, мод `SHALL` зарегистрировать кастомный узел (node) `voxel_bot:barrier`.

* **Физические свойства барьера:** Узел `SHALL` быть спроектирован так, чтобы блокировать физические объекты и жидкости, но оставаться невидимым для игроков.
* `[Reference Implementation: minetest.register_node("voxel_bot:barrier", { ... })]`:
  * `drawtype = "airlike"` (Полностью прозрачный).
  * `pointable = false` (Игроки не могут выделить его курсором).
  * `walkable = true` (Блокирует движение игроков и мобов).
  * `buildable_to = false` (Нельзя заменить другим блоком).
  * `sunlight_propagates = true` (Не создает теней).
  * *Liquid Protection:* Узел физически преграждает путь растекающимся узлам (`liquidtype = "none"`), таким как вода и лава.

## 4. Plot Infrastructure Generation (Генерация инфраструктуры)

КОГДА Участок (`plot_id`) инициализируется впервые, подсистема `SHALL` автоматически сгенерировать его физическое обустройство вокруг расчётной зоны $X_0, Z_0$.

1. **Бордюр:** На высоте $Y=0$ по внешнему периметру участка (координаты $X_0-1$ до $X_0+32$ и $Z_0-1$ до $Z_0+32$) `SHALL` быть установлен контрастный блок (например, `default:stonebrick`).
2. **Защитный купол (Щит):** Подсистема `SHALL` возвести стены из блока `voxel_bot:barrier` по внешнему периметру бордюра от высоты $Y=1$ до $Y=63$.
3. **Зона гостя:** На координате $(X_0 + 15, Y_0, Z_0 - 2)$ (на нейтральной дорожке перед участком) `SHALL` быть установлен пьедестал с кнопкой `voxel_bot:demo_button` (интерактивный триггер для зрителей).
