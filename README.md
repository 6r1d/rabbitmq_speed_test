# RabbitMQ test (2022)

A tiny informal experiment I did to check how many requests I could send through RabbitMQ synchronously,
without much effort.

Delay is set in `injector/main.py`.

| Delay, seconds | Requests per second |
|----------------|---------------------|
| `0.01`         | `95/s`              |
| `0.0005`       | `1,341/s`           |
| `0.0001`       | `3,252/s`           |
| `0.00001`      | `5,270/s`           |