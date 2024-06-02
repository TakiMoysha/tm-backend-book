from enum import Enum, unique


@unique
class SUPPORTED_GATEWAY_SERVERS(Enum):
    uvicorn = "uvicorn"
