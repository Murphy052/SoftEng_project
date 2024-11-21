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

@app.command()
def init():
    from src.db.database import SqliteDatabase
    from src.db.init_db import initialize_database

    db = SqliteDatabase("database.db")
    initialize_database(db)
    db.get_conn().close()


if __name__ == "__main__":
    app()
