import logging_config
import logging
import questionary
import os
import pathlib
import distro
import subprocess

# config logging
logging_config.configure_logging()

# install cuda, torch or jax depends on backend
# @param backend: the backend to install
# @param pip_exccutable: the pip executable to use
# @return: None
def install_backend(pip_executable, backend):
    if backend == "[1] CUDA 12.1 + PyTorch Nightly":
        # pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
        result = subprocess.run([pip_executable, "install", "--pre", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/nightly/cu121"])
    elif backend == "[2] CUDA 11.8 + PyTorch 2.0.1":
        # pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        result = subprocess.run([pip_executable, "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu118"])
    elif backend == "[3] CUDA 11.7 + PyTorch 2.0.1":
        # pip3 install torch torchvision torchaudio
        result = subprocess.run([pip_executable, "install", "torch", "torchvision", "torchaudio"])
    elif backend == "[4] CUDA 11.7 + PyTorch 1.13.1":
        # pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
        result = subprocess.run([pip_executable, "install", "torch==1.13.1+cu117", "torchvision==0.14.1+cu117", "torchaudio==0.13.1", "--extra-index-url", "https://download.pytorch.org/whl/cu117"])
    elif backend == "[5] CUDA 11.6 + PyTorch 1.13.1":
        # pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu116
        result = subprocess.run([pip_executable, "install", "torch==1.13.1+cu116", "torchvision==0.14.1+cu116", "torchaudio==0.13.1", "--extra-index-url", "https://download.pytorch.org/whl/cu116"])
    elif backend == "[6] CUDA 11.6 + PyTorch 1.12.1":
        # pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu116
        result = subprocess.run([pip_executable, "install", "torch==1.12.1+cu116", "torchvision==0.13.1+cu116", "torchaudio==0.12.1", "--extra-index-url", "https://download.pytorch.org/whl/cu116"])
    elif backend == "[7] TPU (must be v3)":
        result = subprocess.run([pip_executable, "install", "jax[tpu]", "-f", "https://storage.googleapis.com/jax-releases/libtpu_releases.html"])
    
    if result.returncode != 0:
        logging.error("Failed to install backend")
        exit(1)



# create virtual environment
# @param train_env_path: the path to create the training environment
# @return: None
def create_virtual_env(train_env_path):
    # if system is ubuntu or debian, we can use apt-get
    # install python3-venv
    distro_name = distro.linux_distribution()[0].toLowerCase()
    if distro_name == "ubuntu" or distro_name == "debian":
        subprocess.run(["sudo", "apt-get", "update"])
        subprocess.run(["sudo", "apt-get", "install","-y", "python3-venv"])
    
    # create virtual environment
    subprocess.run(["python3", "-m", "venv", train_env_path])

# main function
def start(train_env_path=None, train_type=None):
    # get home path
    home_path = str(pathlib.Path.home())

    # ask user where to create the training environment
    # default path is user home dir + training_env
    if train_env_path == None:
        train_env_path = questionary.text(
            "Where do you want to create the training environment?",
            default=home_path + "/training_env",
            validate=lambda text: pathlib.Path(text).is_dir() and len(list(pathlib.Path(text).iterdir())) == 0,
            message={
                "invalid": "The path must be empty"
            }
        ).ask()
    else:
        # check if train_env_path is empty
        if len(list(pathlib.Path(train_env_path).iterdir())) != 0:
            logging.error("The training env path must be empty")
            exit()
    
    # ask the train type if not specified
    if train_type == None:
        train_type = questionary.select(
            "which type of training project do you want to create?",
            choices=[
                "[1] [GPU]dreambooth-lora",
                "[2] [GPU]dreambooth",
                "[3] [GPU]text-to-image",
                "[4] [TPU]dreambooth",
                "[5] [TPU]text-to-image"
            ]
        ).ask()
    
    # ask user to choose a training backend
    # [1] CUDA 12.1 + PyTorch 2.0.1
    # [2] CUDA 11.8 + PyTorch 2.0.1
    # [3] CUDA 11.7 + PyTorch 2.0.1
    # [4] CUDA 11.7 + PyTorch 1.13.1
    # [5] CUDA 11.6 + PyTorch 1.13.1
    # [6] CUDA 11.6 + PyTorch 1.12.1
    # [7] TPU (must be v3)

    training_backend = questionary.select(
        "Which training backend do you want to use?",
        choices=[
            "[1] CUDA 12.1 + PyTorch Nightly",
            "[2] CUDA 11.8 + PyTorch 2.0.1",
            "[3] CUDA 11.7 + PyTorch 2.0.1",
            "[4] CUDA 11.7 + PyTorch 1.13.1",
            "[5] CUDA 11.6 + PyTorch 1.13.1",
            "[6] CUDA 11.6 + PyTorch 1.12.1",
            "[7] TPU (must be v3)"
        ]
    ).ask()

    # create the virtual environment
    create_virtual_env(train_env_path)

    pip_executable = train_env_path + "/bin/pip"

    # install the backend
    install_backend(pip_executable, training_backend)

    # install other dependencies

    # install acccelerate if not "[7] TPU (must be v3)"
    if training_backend != "[7] TPU (must be v3)":
        result = subprocess.run([pip_executable, "install", "accelerate"])
        if result.returncode != 0:
            logging.error("Failed to install accelerate")
            exit(1)
    
    # install diffusers from source
    result = subprocess.run([pip_executable, "install", "git+https://github.com/huggingface/diffusers"])
    if result.returncode != 0:
        logging.error("Failed to install diffusers")
        exit(1)

    # install other dependencies according to train_type
    if train_type == "[1] [GPU]dreambooth-lora" or train_type == "[2] [GPU]dreambooth":
        # https://github.com/huggingface/diffusers/raw/main/examples/dreambooth/requirements.txt
        result = subprocess.run([pip_executable, "install", "-r", "https://github.com/huggingface/diffusers/raw/main/examples/dreambooth/requirements.txt"])
        if result.returncode != 0:
            logging.error("Failed to install dreambooth-lora dependencies")
            exit(1)
    elif train_type == "[3] [GPU]text-to-image":
        # https://github.com/huggingface/diffusers/raw/main/examples/text_to_image/requirements.txt
        result = subprocess.run([pip_executable, "install", "-r", "https://github.com/huggingface/diffusers/raw/main/examples/text_to_image/requirements.txt"])
        if result.returncode != 0:
            logging.error("Failed to install text-to-image dependencies")
            exit(1)
    elif train_type == "[4] [TPU]dreambooth":
        # https://github.com/huggingface/diffusers/raw/main/examples/dreambooth/requirements_flax.txt
        result = subprocess.run([pip_executable, "install", "-r", "https://github.com/huggingface/diffusers/raw/main/examples/dreambooth/requirements_flax.txt"])
        if result.returncode != 0:
            logging.error("Failed to install dreambooth-lora dependencies")
            exit(1)
    elif train_type == "[5] [TPU]text-to-image":
        # https://github.com/huggingface/diffusers/raw/main/examples/text_to_image/requirements_flax.txt
        result = subprocess.run([pip_executable, "install", "-r", "https://github.com/huggingface/diffusers/raw/main/examples/text_to_image/requirements_flax.txt"])
        if result.returncode != 0:
            logging.error("Failed to install text-to-image dependencies")
            exit(1)
    
    logging.info("Training environment created successfully")


if __name__ == '__main__':
    start()