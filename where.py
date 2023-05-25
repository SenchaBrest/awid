import click

@click.command()
@click.option('--where', '-w')
def main(where):
    print(where)

if __name__ == "__main__":
    main()