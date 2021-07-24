import logging
from enum import Enum

from flask import request
from logstash import LogstashHandler


def extend_enum(inherited_enum):
    def wrapper(added_enum):
        joined = {}
        for item in inherited_enum:
            joined[item.name] = item.value
        for item in added_enum:
            joined[item.name] = item.value
        return Enum(added_enum.__name__, joined)

    return wrapper


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get("X-Request-Id")
        return True


def add_logstash_handler(app, settings):
    logstash_handler = LogstashHandler(
        settings.logstash_host,
        int(settings.logstash_port),
        version=1,
    )
    logstash_handler.setLevel(logging.INFO)
    logstash_handler.addFilter(RequestIdFilter())
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(logstash_handler)
    return app
