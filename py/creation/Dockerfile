# Use an official base image with micromamba pre-installed
FROM mambaorg/micromamba:latest

# Set the working directory
WORKDIR /app

# Copy source folders
COPY src/ /app/src/
COPY shared/ /app/shared/

# Copy the environment file
COPY environment.yml /app/environment.yml

# Create the environment from environment.yml
RUN micromamba env create -f /app/environment.yml && \
    micromamba clean --all --yes

# Activate the environment by default in micromamba containers
ENV MAMBA_DOCKERFILE_ACTIVATE=1
ENV CONDA_DEFAULT_ENV=creation_env
ENV PATH=/opt/conda/envs/creation_env/bin:$PATH

# Expose ports
EXPOSE 8080

# Set the command to run your Python script when the container starts
CMD ["micromamba", "run", "-n", "creation_env", "python", "-m", "src.main"]
