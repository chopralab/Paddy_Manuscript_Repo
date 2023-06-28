import os
import subprocess
import warnings
import docker


# Define client, pathing, and volume
client = docker.from_env()
volume_name = 'myvolume'
client.volumes.create(name=volume_name)
volume_config = {volume_name: {'bind': '/vol', 'mode': 'rw'}}
output_path = '/vol/output.txt'

# Get the Vector input from the user
vector_input_path = raw_input("Enter the path to the Vector input file: ")

# Read the Vector input file
with open(vector_input_path, "r") as f:
    vector_input = f.read().strip()

# Set the environment variables
env_vars = {
    "VECTOR_INPUT": vector_input,
    "OUTPUT_PATH": output_path
}

# Write the environment variables to a .env file
with open(".env", "w") as f:
    for key, value in env_vars.items():
        f.write("{}={}\n".format(key, value))

# Specify the command to run Docker Compose
command = ["docker-compose", "up"]

# Execute the command
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Capture the output and error
stdout, stderr = process.communicate()

# Check if the command was successful
if process.returncode == 0:
    print("Docker Compose started successfully")
    print(stdout.decode())
else:
    print("Failed to start Docker Compose")
    print(stderr.decode())

container = client.containers.run(
    'alpine:latest',
    command=f'cat {output_path}',
    volumes=volume_config,
    detach=True
)

# Remove the .env file
os.remove(".env")

# Remove the Docker container
subprocess.call(["docker-compose", "down"])


