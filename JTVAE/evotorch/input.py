import torch
import argparse
import docker

parser = argparse.ArgumentParser()
# Accept three command line arguments: lower bound, upper bound, and number of steps
parser.add_argument('--Vector', type=str, default='0.4, 0.1, -0.8, -0.2, 0.9, -0.6, -0.5, -0.4, 0.9, -0.2, 0.5, -0.1, 0.3, -0.9, 0.7, 0.8, -0.1, -0.0, 1.0, 0.5, -0.3, -0.3, 0.4, 1.0, 0.7, 0.6, -0.2, 0.3, -0.2, -0.8, -0.2, 0.3, 0.1, -0.8, 0.9, 0.3, -0.4, -1.0, 0.1, -0.6, 0.5, 0.4, -0.2, -0.6, -1.0, -0.5, -0.4, 0.6, -0.2, -0.7, -0.7, -0.5, -0.7, 0.9')

vector = parser.parse_args().Vector

# Define client, pathing, and volume
client = docker.from_env()
volume_name = 'myvolume'
client.volumes.create(name=volume_name)
volume_config = {volume_name: {'bind': '/vol', 'mode': 'rw'}}
output_path = '/vol/output.txt'

# Global variable to store all evaluation values
evaluations = []
# Define a function to minimize
def JTVAE(x: torch.Tensor) -> torch.Tensor:
    print(str(x.tolist()))

    # Run the container that corresponds to the fitness function you want to use
    client.containers.run(
        "jtvae",
        volumes=volume_config,
        environment={"Vector": str(x.tolist()), "OUTPUT": output_path},
        remove=True,
    )

    # Run another container with the same volume attached and read the file
    # This container outputs the contents of the file to stdout
    container = client.containers.run(
        'alpine:latest',
        command=f'cat {output_path}',
        volumes=volume_config,
        detach=True
    )

    # Wait for the container to finish and get its output
    response = container.wait()
    output = container.logs()

    # Decode the output, add it to evaluations and return as a torch tensor
    evaluation = output
    evaluations.append(evaluation)
    print(f"Current Evaluation: {evaluation}")
    return evaluation