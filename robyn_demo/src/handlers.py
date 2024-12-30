from robyn import router


@router.get("/")
async def h(request):
    return "Hello :)"


@router.get("/static/{static_path}")
async def static_files(request):
    print(request.path_params.get("static_path"))
    return "done"
