import typer

app = typer.Typer()


@app.command()
def tentacle(power: list[str]) -> None:
    print(f"Deleting user: {power}")


if __name__ == "__main__":
    app()
