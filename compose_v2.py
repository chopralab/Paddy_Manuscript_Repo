import subprocess
import os
# Set the environment variables
env_vars = {
    "VECTOR_INPUT": "[1.0, -0.5, 0.3, 0.1, -0.1, -0.6, 1.0, 0.2, -0.2, -0.8, -0.3, -0.3, -0.3, -0.2, -1.0, -0.9, -0.9, -0.5, 0.1, 0.9, 0.6, 0.6, -0.7, 0.5, -0.3, -0.4, -0.7, -0.1, 0.0, 0.6, 0.8, -0.1, 0.1, 0.3, -0.7, 0.4, 0.2, 0.4, 0.7, -0.2, 0.5, 0.6, -0.5, -0.2, 0.3, 0.2, -0.9, -0.5, -0.7, -0.9, 0.1, 0.9, 0.9, -0.8, -0.1, -0.1]",
    "OUTPUT_PATH": "JTVAE_test.txt"
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

# Remove the .env file
os.remove(".env")