from robyn import Robyn

app = Robyn(__file__)


@app.get("/")
async def h(request):
    return "Hello :)"


@app.get("/static/{static_path}")
async def static_files(request):
    print(request.path_params.get("static_path"))
    return "done"


app.start(port=8000)
