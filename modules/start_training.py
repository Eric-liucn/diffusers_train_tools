
import pathlib
import questionary
import logging
import logging_config
import yaml
import requests
import subprocess

# get train script from url according to train_type
# @param project_path: str
# @param train_type: str
# @return train_script_path: str
def get_train_script(project_path, train_type):
    
    train_script_path = project_path + "/train.py"
    if train_type == "[1] [GPU]dreambooth-lora":
        train_script_url = "https://github.com/huggingface/diffusers/raw/main/examples/dreambooth/train_dreambooth_lora.py"
        # download train script
        response = requests.get(train_script_url)
        if response.status_code != 200:
            logging.error("Failed to download train script")
            exit(1)
        with open(train_script_path, "wb") as f:
            f.write(response.content)
    elif train_type == "[2] [GPU]dreambooth":
        train_script_url = "https://github.com/huggingface/diffusers/raw/main/examples/dreambooth/train_dreambooth.py"
        # download train script
        response = requests.get(train_script_url)
        if response.status_code != 200:
            logging.error("Failed to download train script")
            exit(1)
        with open(train_script_path, "wb") as f:
            f.write(response.content)
    elif train_type == "[3] [GPU]text-to-image":
        train_script_url = "https://github.com/huggingface/diffusers/raw/main/examples/text_to_image/train_text_to_image.py"
        # download train script
        response = requests.get(train_script_url)
        if response.status_code != 200:
            logging.error("Failed to download train script")
            exit(1)
        with open(train_script_path, "wb") as f:
            f.write(response.content)
    elif train_type == "[4] [TPU]dreambooth":
        train_script_url = "https://github.com/huggingface/diffusers/raw/main/examples/dreambooth/train_dreambooth_flax.py"
        # download train script
        response = requests.get(train_script_url)
        if response.status_code != 200:
            logging.error("Failed to download train script")
            exit(1)
        with open(train_script_path, "wb") as f:
            f.write(response.content)
    elif train_type == "[5] [TPU]text-to-image":
        train_script_url = "https://github.com/huggingface/diffusers/raw/main/examples/text_to_image/train_text_to_image_flax.py"
        # download train script
        response = requests.get(train_script_url)
        if response.status_code != 200:
            logging.error("Failed to download train script")
            exit(1)
        with open(train_script_path, "wb") as f:
            f.write(response.content)
    else:
        logging.error("Invalid train_type, exiting...")
        exit(1)

    return train_script_path


# parse train_config.yaml to args
def parse_train_config(train_config_path):

    # check if train_config_path exists
    if not pathlib.Path(train_config_path).exists():
        logging.error("train_config_path does not exist, exiting...")
        return None
    
    # for every entry in train_config.yaml
    # if the value type is str or int or float, append arg like --key=value
    # if the value type is boolean, append arg like --key
    # if the value is None, skip
    # if the value type is list, append arg like --key=value1,value2,value3
    args = []
    with open(train_config_path, "r") as f:
        train_config = yaml.load(f, Loader=yaml.FullLoader)
        for key, value in train_config.items():
            if value is None:
                continue
            elif type(value) == str or type(value) == int or type(value) == float:
                args.append("--" + key + "=" + str(value))
            elif type(value) == bool:
                args.append("--" + key)
            elif type(value) == list:
                args.append("--" + key + "=" + ",".join(value))
            else:
                logging.error("Unknown type for value: " + str(type(value)))
        
    return args

# main function
def start(project_path=None, train_env_path=None, train_config_path=None, train_type=None):

    if project_path is None:
        # ask where is the project path, check if exists
        # defualt is home path + project
        project_path = questionary.path(
            "Where is the project?",
            default=str(pathlib.Path.home()) + "/project",
            validate=lambda text: pathlib.Path(text).exists()
        ).ask()

    if train_env_path is None:
        # default train_env_path is project path + train_env.yaml
        train_env_path = questionary.path(
            "Where is the train env folder?",
            default=project_path + "/train_env",
        ).ask()

    if train_config_path is None:
        # default train_config_path is project path + train_config.yaml
        train_config_path = questionary.text(
            "Where is the train config file?",
            default=project_path + "/train_config.yaml"
        ).ask()
    
    if train_type is None:
        # default train_type is project path + train_config.yaml
        train_type = questionary.select(
            "Which type of training do you want to start?",
            choices=[
                "[1] [GPU]dreambooth-lora",
                "[2] [GPU]dreambooth",
                "[3] [GPU]text-to-image",
                "[4] [TPU]dreambooth",
                "[5] [TPU]text-to-image"
            ]
        ).ask()
    
    # construct commands
    accelerate_exec = train_env_path + "/bin" + "/accelerate"
    python_exec = train_env_path + "/bin" + "/python"

    # parse train_config.yaml to args
    args = parse_train_config(train_config_path)

    # get train script path
    train_script_path = get_train_script(project_path, train_type)

    # if train_type is 
    # [1] [GPU]dreambooth-lora
    # [2] [GPU]dreambooth
    # [3] [GPU]text-to-image
    # we use accelerate to start training
    if train_type == "[1] [GPU]dreambooth-lora" or train_type == "[2] [GPU]dreambooth" or train_type == "[3] [GPU]text-to-image":
        # construct command
        command = accelerate_exec + " " + train_script_path + " ".join(args)
    # if train_type is
    # [4] [TPU]dreambooth
    # [5] [TPU]text-to-image
    # we use python to start training
    elif train_type == "[4] [TPU]dreambooth" or train_type == "[5] [TPU]text-to-image":
        # construct command
        command = python_exec + " " + train_script_path + " " + " ".join(args)
    else:
        logging.error("Invalid train_type, exiting...")
        exit(1)

    # preview command
    print("Command: " + command.replace(" ", "\n    "))
    # ask if user want to start training
    if questionary.confirm("Do you want to start training?").ask():
        # start training, create a screen session named with project name + _train and run command
        project_name = pathlib.Path(project_path).name
        subprocess.run(["screen", "-dmS", project_name + "_train", command])
        print("Training started, you can use `screen -r " + project_name + "_train` to attach to the screen session")
        
    

    
    
    
    
