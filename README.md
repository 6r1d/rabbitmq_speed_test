# RabbitMQ test (2022)

A tiny informal experiment I did to check how many requests I could send through RabbitMQ synchronously,
without much effort.

Delay is set in `generator/main.py`.

| Delay, seconds | Requests per second |
|----------------|---------------------|
| `0.01`         | `95/s`              |
| `0.0005`       | `1,341/s`           |
| `0.0001`       | `3,252/s`           |
| `0.00001`      | `5,270/s`           |
| `0.0    `      | `11,000/s`          |

## Usage

It is just a personal experiment to see how many "sentences" could pass through RabbitMQ with default settings and library.
The random sentences are currently being generated using the Hunspell dictionary in `generator`'s [`main.py`](./generator/main.py) file.

You can configure both receiver and generator starting delays in [`docker-compose.yml`](./docker-compose.yml) by changing both `START_WAIT_S` parameters in `environment` service parameter.

The `generator` service has a parameter that defines the delay between sending messages.
It can be zero and is called `MSG_DELAY_S`.

To check current performance, run `docker-compose up` and have a look at the [RabbitMQ management panel](http://127.0.0.1:15672/).
`Publish` and `Deliver` message rates tell about the current performance.

### Notes

#### Network issues

I hit some weird network issue when both generator and receiver instances were unable to connect.
In my case, I needed to restart Docker with `doas sv restart docker`.
For `systemd`-based distros, it may be something like `sudo systemctl restart docker`.

## Links

* [Pika](https://pika.readthedocs.io/en/stable/index.html) - a library I tested here
* [aio-Pika](https://aio-pika.readthedocs.io/) - a library to test later to understand AIO performance differences
* X-TEAM: [How to set up RabbitMQ with Docker compose](https://x-team.com/blog/set-up-rabbitmq-with-docker-compose/) - a detailed tutorial on Compose and RabbitMQ