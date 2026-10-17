---
id: "ws3-02-websockify-bridge"
status: "approved"
depends_on:
  - "ws3-00-domain-vision"
  - "ws3-01-docker-topology"
provides_context:
  - "Protocol Translation (WS to UDP)"
  - "Bridge Execution Environment"
  - "Connection Lifecycle & Keepalive"
verification_logic: "websocket_handshake_tests, udp_forwarding_telemetry"
---

# ws3-02-websockify-bridge: Мост Трансляции Протоколов (WebSocket <-> UDP)

> **ABSTRACT:** Спецификация определяет контракты для внутреннего микросервиса `websockify_bridge`. Документ регламентирует правила прозрачной трансляции двунаправленного сетевого трафика между веб-клиентами (браузерами), использующими протокол WebSocket (TCP), и игровым сервером, оперирующим сырыми датаграммами (UDP).

## 1. Protocol Translation Contract (Трансляция Протоколов)

Микросервис `websockify_bridge` `SHALL` выступать в роли "глупого" прокси-транслятора (Layer 4/Layer 7 Proxy). Он не анализирует полезную нагрузку игрового протокола.

* **Ingress (Входящий трафик от браузера):**
  * Сервис `SHALL` принимать входящие TCP-соединения с запросом на Upgrade до протокола WebSocket на внутреннем порту (`[Reference Implementation: TCP 8081]`).
  * КОГДА фрейм WebSocket (Binary Frame) получен, сервис `SHALL` извлечь из него сырую бинарную нагрузку (Payload).
  * Сервис `SHALL` отправить эту нагрузку в виде UDP-датаграммы на внутренний DNS-адрес и порт игрового сервера (`[Reference Target: luanti_server:30000]`).
* **Egress (Исходящий трафик от сервера):**
  * КОГДА UDP-датаграмма получена от `luanti_server`, сервис `SHALL` обернуть её в бинарный фрейм WebSocket.
  * Сервис `SHALL` маршрутизировать этот фрейм обратно в TCP-сокет соответствующего клиента.

## 2. Execution Environment (Среда выполнения)

ИИ-агент `SHALL` подготовить спецификацию сборки (`[Reference Implementation: Dockerfile]`) для данного сервиса.

* Сервис `SHALL` запускаться как изолированный легковесный процесс.
* Агент `SHALL` использовать готовое решение с поддержкой UDP-режима (`[Reference Implementation: novnc/websockify с флагом --udp или эквивалент на Go/Rust]`).
* Процесс `SHALL NOT` запускаться от имени пользователя `root` (контейнер `SHALL` использовать `USER nobody` или аналог для снижения радиуса поражения при компрометации).

## 3. Connection Lifecycle & Keepalive (Жизненный цикл)

Управление ресурсами `SHALL` строго следовать жизненному циклу WebSocket-соединений.

* КОГДА WebSocket-соединение устанавливается, мост `SHALL` аллоцировать виртуальный локальный UDP-порт для общения с сервером.
* КОГДА браузер закрывает вкладку (инициируется штатное закрытие сокета: TCP FIN или WebSocket Close Frame) ИЛИ происходит обрыв соединения по таймауту (TCP Keepalive fail), мост `SHALL`:
  1. Немедленно прекратить отправку датаграмм на `luanti_server:30000` для данной сессии.
  2. Освободить аллоцированный локальный UDP-порт и уничтожить состояние сессии в памяти.
* Мост `SHALL NOT` поддерживать "зомби-сессии" (zombie states). Любая неактивность WebSocket-канала сверх заданного таймаута (например, 60 секунд) `SHALL` приводить к принудительному сбросу сессии.

## 4. Security & Isolation (Изоляция)

В соответствии с `[[ws3-01-docker-topology]]`:
* Сервис `websockify_bridge` `SHALL NOT` экспонировать свой слушающий TCP-порт наружу хост-машины.
* Сервис `SHALL` принимать TCP-подключения ИСКЛЮЧИТЕЛЬНО от контейнера `nginx_gateway` (в рамках внутренней сети `voxel_net`). Проверки SSL/TLS сертификатов (TLS Termination) на уровне моста `SHALL NOT` выполняться, так как эта ответственность делегируется Nginx.
