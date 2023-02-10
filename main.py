import sys
import uvicorn


def should_reload() -> bool:
    reload = False

    if len(sys.argv) >= 2:
        reload_flag = sys.argv[1]
        if reload_flag == "--reload":
            reload = True

    return reload


def main():
    (host, port,) = ("0.0.0.0", 8000,)
    with_reloading = should_reload()
    if with_reloading:
        print("Initializing app with hot reloading! perfect for debugging/development... cause: --reload flag")

    uvicorn.run("src.app:app", host=host, port=port, reload=with_reloading)


if __name__ == "__main__":
    main()
