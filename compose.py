# #Runs the image, but doesn't have input
# import subprocess

# # Specify the command to run Docker Compose
# command = ["docker-compose", "up"]

# # Execute the command
# process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# # Capture the output and error
# stdout, stderr = process.communicate()

# # Check if the command was successful
# if process.returncode == 0:
#     print("Docker Compose started successfully")
#     print(stdout.decode())
# else:
#     print("Failed to start Docker Compose")
#     print(stderr.decode())
# ##############
import subprocess
import random
vector = [round(random.uniform(-1, 1), 1) for _ in range(56)]
print(vector)

# Specify the full path to docker-compose
docker_compose_path = "/usr/local/bin/docker-compose"

#command = ["docker-compose", "-f", "/path/to/your/docker-compose.yml", "up"]
# Specify the command to run Docker Compose
command = [docker_compose_path, "up"]

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

