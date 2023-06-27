# anaconda base docker image
FROM continuumio/miniconda3

# Copy all files in the repo to the docker image
COPY . .

# Change the working directory to the Requirements folder
WORKDIR /Requirements

# Creating the conda enviroment in the docker image
RUN conda env create -f JTVAE.yml

# Run the new conda enviroment in the docker image
SHELL ["conda","run","-n","JTVAE","/bin/bash","-c"]


# Change the working directory to the folder with the python script
WORKDIR ../JTVAE/Paddy

# Set the entrypoint to run the python script
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "JTVAE", "python", "JTVAE.py"]

# Set default parameters
CMD ["--Vector=\"$Vector\"", "--OUTPUT=\"$OUTPUT\""]
