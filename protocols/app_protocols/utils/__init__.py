from dataclasses import dataclass


@dataclass
class WebProtocolsStartingParams:
    bind_host: str | None = None
    bind_port: int | None = None

    config_file: str | None = None
