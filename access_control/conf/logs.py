LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(levelname)s \t %(name)s \t %(asctime)s \t pid:%(process)s \t %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": """
                asctime: %(asctime)s
                filename: %(filename)s
                funcName: %(funcName)s
                levelname: %(levelname)s
                lineno: %(lineno)d
                message: %(message)s
                module: %(module)s
                name: %(name)s
                process: %(process)s
            """,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": { "console": {"formatter": "default", "level": "DEBUG", "class": "logging.StreamHandler"}},
    "loggers": { "": {"level": "INFO", "propagate": False, "handlers": ["console"]} },
}
