from robyn import Robyn, Config
from .handlers import router

config = Config()

app = Robyn(__file__, config=config)
app.include_router(router)

def run_app():
    app.start(port=8000)
