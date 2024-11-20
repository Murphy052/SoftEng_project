from typer import Typer

app = Typer()

@app.command()
def run():
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("src.main:app", port=port, reload=True)

@app.command()
def test():
    import subprocess

    subprocess.run(['pytest', 'tests'])


if __name__ == "__main__":
    app()
