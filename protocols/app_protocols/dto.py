from dataclasses import dataclass


@dataclass
class AppStartingParams:
    app: str = "app_protocols.app:app"
    bind_host: str | None = None
    bind_port: int | None = None

    config_file: str | None = None
