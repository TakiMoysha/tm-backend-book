# Binance Proxy API

Сервис для обучения скальпингу.

Скачивает данные с Binance, сохраняет их в БД, и публикует в каналы. Представляет из себя небольшой bridge-сервис, который оборачивает данные через ZeroMQ для консьюмеров.
К каналам могут подключаться клиенты: конечное приложение (фронтенд) или другие сервисы.

## Domain Spec

**Tickdata** - самая маленькая единица данных:

- _Trade-tick_ - сообщение о сделке (price, quantity, timestamp, buyer/seller)
- _Quote-tick_ - сообщение об обновлении стакана (bid/ask levels)

**Backtest** - тестирование стратегии на исторических данных с симуляцией исполнения ордеров.

**Order Book** - стакан заявок (bids/asks) с глубиной рынка.

<!-- TODO: сделать через макрос -->

Candle (OHLCV) - открытие, максимум, минимум, закрытие, объем за период

Spread - разница между best ask и best bid

Depth - кол-во ордеров на каждом уровен цен

VWAP (volume-weighted average price) - средняя цена с учетом объема

Slippage - разница между ожидаемой и фактической цены исполнения

Liquidity - способность купить/продать без существенного влияния цены

Trade execution - когда ордер исполняется

## Design

just + justfile для комманда
podman + podman-compose для контейнеров
dataclass для конфигов

Следовать Explicit Architecture.


- Batch inserts для БД
- партицирование по времени (автоматически в timescaledb
- асинхронная запись
- flush buffer (DB)
- retries и backoff (jitter, exponential backoff)
- idempotency key (deduplication)
- sequence numbers (skip-check)


- NOTIFY/LISTEN (можно ли?)
- ассоциативные таблицы (можно ли?)

### Нужен ли Bridge-слой?

- единая точка для всех клиентов
- экологичная работа с api: rate-limit, упрощенное кэширование и агрегация запросов
- простой переход между провайдерами
- offline режимы для тестирования (replay по историеским данным)

**Выводы**: будет использовать, по возможности использовать composefile с локальными volumes.

### Recommendations

ZeroMQ для межсервисного общения:

- **PUB/SUB** - для рыночных данных (real-time стримы)
- **REQ/REP** - для синхронных запросов (исторические данные, метаданные)
- **ROUTER/DEALER** - для балансировки нагрузки между несколькими клиентами
- топики (и см. "Kafka - Practices / Соглашение об наименованиях"): `binance.spot.{symbol}.trades`, `binance.spot.{symbol}.orderbook`

PostgreSQL для хранения + timescaleDB:

- timescaledb - что по автоматической агрегации
- materizelized views - для предрасчитанных OHLCV на разных таймфреймах
- данные будет записываться в timescale, преобразовываться в MV (1m, 5m), сохраняться в parquet

Apache arrow (parquet) для долгосрочного хранения и чтения больших объемов (backtest).

Кеш будет redis-like (dragonfly или valkey).

ccxt для работы с биржами.

Для общения Json (optional cloudevents) + MessagePack.

## Implementation

- [x] Поднять инфраструктуру (composefile)
Пары, отслеживаемых пар будут храниться в отдельной таблице, загрузать по умолчанию пары: ETH/USDT, SOL/USDT


