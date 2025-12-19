# Prototype for dmr async api spec generator

Проект по генерации AsyncAPI yml файла на основе API.

На текущем этапе используется django-modern-rest для API (dmr) и генерация будет происходить с него.
Пример api в @example.py.

## Что необходимо реализовать
- [?] парсинг маршрутов, на соответствие `AsyncAPIProtocol(typing.Protocol)`
- то, что поддерживает грузит данные из маршута и получаем `SpecPlan`:
    - маппинг в asyncapi operations (send/receive)
    - конвертация `msgspec.Struct` (`pydantic.BaseModel` потом, просто держим в голове для расширения)
    - channel difinitions из url
    - message schemas на оснтве request/response моделей
    - [?] вложенные структуры и сложные типы 

- генерация asynapi.yaml, структура, метаданные, components/schemas, operations
- кастомные поля для маршрутов (исключения, exapmles, etc)
- расширения из других same-генераторов (аля AsyncApiSpecBuilder), 

- интеграция с django commands
- hot-reload для dev режима

# References

- https://www.asyncapi.com/docs/reference/specification/v3.0.0

