def create_asgi():
    from fastapi import FastAPI

    # from fastapi.middleware import Middleware
    # from fastapi.middleware.cors import CORSMiddleware
    from app.__about__ import __version__
    from app.config import get_config
    from app.server import server_lifespan

    config = get_config()
    app = FastAPI(
        title="BackendBook-FastApi-Events",
        version=__version__,
        debug=config.server.debug,
        lifespan=server_lifespan,
        middleware=(
            # Middleware(
            #     CorsMiddleware,
            #     allow_credentials=True,
            #     allow_origins=config.server.cors_origins,
            #     allow_methods=["*"],
            #     allow_headers=["*"],
            # )

        ),
    )
    return app


app = create_asgi()
