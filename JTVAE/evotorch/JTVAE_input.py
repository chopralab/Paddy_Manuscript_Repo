from evotorch import Problem
from evotorch.algorithms import SNES
from evotorch.logging import StdOutLogger
import torch
import argparse
import docker

# Argument parsing
parser = argparse.ArgumentParser()
# Accept a command line argument: Vector
parser.add_argument('--Vector', type=str, required=True)
args = parser.parse_args()

# Convert Vector string to a torch.Tensor of size 56
Vector = torch.tensor(list(map(float, args.Vector.split(','))))

# Define client, pathing, and volume
client = docker.from_env()
volume_name = 'myvolume'
client.volumes.create(name=volume_name)
volume_config = {volume_name: {'bind': '/vol', 'mode': 'rw'}}
output_path = '/vol/JTVAE_output.txt'

# Variable to keep track of the best evaluation
best_eval = float('inf')
best_x = None

# Global variable to store all evaluation values
evaluations = []

# Define a function to minimize
def jtvae_fitness(x: torch.Tensor) -> torch.Tensor:
    # Convert the torch.Tensor to a comma-separated string
    x_str = ','.join(map(str, x.tolist()))

    # Run the JTVAE container
    client.containers.run(
        "JTVAE",
        volumes=volume_config,
        environment={"Vector": x_str, "OUTPUT": output_path},
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
    evaluation = float(output.decode())
    evaluations.append(evaluation)
    print(f"Current Evaluation: {evaluation}")
    return torch.tensor(evaluation)

# Define a Problem instance wrapping the function
# Solutions have length 56
problem = Problem("min", jtvae_fitness, solution_length=56, initial_bounds=(-1, 1))

# Instantiate a searcher
searcher = SNES(problem, stdev_init=0.5)

# Create a logger
logger = StdOutLogger(searcher)

# After Evolve!
searcher.run(1)

# Find the best evaluation
best_eval = min(evaluations)

# Write the best evaluation to a file in the volume
best_eval_file = '/vol/best_evaluation.txt'

# Run a lightweight Docker container with the volume attached to write the best evaluation
write_command = f"echo '{best_eval}' > {best_eval_file}"
client.containers.run(
    'alpine:latest',
    command=f'/bin/sh -c "{write_command}"',
    volumes=volume_config,
    remove=True
)

print(f"Best Evaluation: {best_eval} has been written to {best_eval_file}")
