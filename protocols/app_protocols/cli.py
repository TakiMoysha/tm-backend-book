from logging import getLogger

import importlib
import uvicorn
import click

from app_protocols.dto import AppStartingParams
from app_protocols.consts import SUPPORTED_GATEWAY_SERVERS

logger = getLogger(__name__)


def init_app_params(**kwargs) -> AppStartingParams:
    app = AppStartingParams(
        app=kwargs["app"],
        bind_host=kwargs["host"],
        bind_port=kwargs["port"],
        config_file=kwargs["config"],
    )
    return app


def generate_gateway_kwargs(app_params: AppStartingParams) -> dict:
    kwargs = {
        "app": app_params.app,
        "host": app_params.bind_host,
        "port": app_params.bind_port,
        "use_colors": True,
        "lifespan": "off",
        "log_level": "warning",
        "access_log": False,
        "forwarded_allow_ips": "*",
        "reload": True,
    }
    return kwargs


@click.command("runserver", help="Run server")
@click.option("-v", "--version", is_flag=True, default=False, help="Show version")
@click.option("-H", "--host", default="127.0.0.1", help="Bind [default: 127.0.0.1]")
@click.option("-p", "--port", default=8000, help="Bind port. [default: 8000]")
@click.option("-c", "--config", default=None, help="Config file. [default: None]")
@click.option(
    "--gateway",
    type=click.Choice([v.value for v in SUPPORTED_GATEWAY_SERVERS]),
    default=SUPPORTED_GATEWAY_SERVERS.uvicorn.value,
    help="Gateaway server. [default: {}]".format(SUPPORTED_GATEWAY_SERVERS),
)
@click.option(
    "--app",
    default="app_protocols.app:app",
    help="Python ASGI app. [default: app_protocols.app:app]",
)
def runserver(**kwargs):
    if kwargs["version"]:
        from . import __version__

        print(__version__)
        exit()

    if kwargs["gateway"]:
        try:
            gateway = importlib.import_module("{}".format(kwargs["gateway"]))
        except ModuleNotFoundError as err:
            err_msg = "Gateway server {} not found: {}".format(kwargs["gateway"], err)
            logger.error(err_msg)
            exit(1)

    app_params = init_app_params(**kwargs)
    gateway_kwargs = generate_gateway_kwargs(app_params)
    logger.info(f"Running server with kwargs: {gateway_kwargs}")
    return uvicorn.run(**gateway_kwargs)
