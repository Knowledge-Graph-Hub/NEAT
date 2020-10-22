import os
import click
import yaml

from neat.embeddings import make_embeddings, make_classifier


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
        if not os.path.exists(neat_config['embeddings']['embedding_file_name']):
            make_embeddings(neat_config['embeddings'])

    if 'classifier' in neat_config:
        for classifier in neat_config['classifier']:
            model = make_classifier(classifier)
            embedding_model, method, train_data, validation_data = make_data(neat_config)  # this generates pos/neg train/validation data
            model_fit(model, train_data, validation_data, neat_config['classifier'])
    return None


