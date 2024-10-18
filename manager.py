from typer import Typer

app = Typer()

@app.command()
def run():
    import uvicorn
    print("Hello")
    uvicorn.run("src.main:app", port=8000, reload=True)

@app.command()
def test():
    ...


if __name__ == "__main__":
    app()
