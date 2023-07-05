import docker

# Define client and volume name
client = docker.from_env()
volume_name = 'my_volume'
container_image = '<image_name>'

# Run a temporary container with the volume mounted
temp_container = client.containers.run(
    container_image,
    volumes={volume_name: {'bind': '/vol', 'mode': 'rw'}},
    detach=True,
    command='ls /vol/data'  # Command to list the contents of the 'data' folder
)

# Wait for the container to finish running
temp_container.wait()

# Retrieve the container's logs to see the output
output = temp_container.logs().decode()
print(output)

# Remove the temporary container
temp_container.remove()
