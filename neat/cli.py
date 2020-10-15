import click
import yaml

from neat.embeddings import make_embeddings


def parse_yaml(file: str) -> object:
    with open(file, 'r') as stream:
        return yaml.safe_load(stream)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--config", required=True, default="config.yaml", type=click.Path(exists=True))
def run(config: str) -> None:
    """Run a NEAT pipeline using the given YAML file [neat.yaml]
    \f

    Args:
        config: Specify the YAML file containing a list of datasets to download.

    Returns:
        None.

    """
    neat_config = parse_yaml(config)

    # generate embeddings if config has 'embeddings' block
    if 'embeddings' in neat_config:
        make_embeddings(neat_config['embeddings'])
    return None

