import torch
import argparse
import docker
import numpy as np

parser = argparse.ArgumentParser()

random_numbers = np.random.uniform(-1, 1, size=56).round(2).tolist()
random_vector = ", ".join(str(num) for num in random_numbers)
print(random_vector)

# Accept three command line arguments: lower bound, upper bound, and number of steps
parser.add_argument('--Vector', type=str, default=str(random_vector))

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