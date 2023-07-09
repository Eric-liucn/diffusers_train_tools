from pathlib import Path
import questionary
import logging_config

# config logging
logging_config.configure_logging()

# main function
def start():
    # get user home dir
    home_path = str(Path.home())

    # ask user the train type
    # [1] [GPU]dreambooth-lora
    # [2] [GPU]dreambooth
    # [3] [GPU]text-to-image
    # [4] [TPU]dreambooth
    # [5] [TPU]text-to-image
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

    # ask user the project name, should not contain space and special characters
    project_name = questionary.text(
        "What is the project name?",
        default="my_project",
        validate=lambda text: text.isalnum() or text.isascii(),
        instruction="The project name should not contain space and special characters"
    ).ask()

    # ask user where to create the project
    # the path must be empty
    # default path is user home dir + project name
    project_path = questionary.text(
        "Where do you want to create the project?",
        default=home_path + "/" + project_name,
        validate=lambda text: Path(text).is_dir() and len(list(Path(text).iterdir())) == 0,
        instruction="The path must be empty"
    ).ask()

    # if project path not exist, create the folder, if parent dir not exists, create them too
    Path(project_path).mkdir(parents=True, exist_ok=True)
    logging_config.logging.info("Project path created: " + project_path)

    # create data folder, should be project_path/data
    Path(project_path + "/data").mkdir(parents=True, exist_ok=True)
    logging_config.logging.info("Data folder created: " + project_path + "/data")

    # create regulation data folder, should be project_path/data/reg_data
    Path(project_path + "/data/reg_data").mkdir(parents=True, exist_ok=True)
    logging_config.logging.info("Regulation data folder created: " + project_path + "/data/reg_data")

    # create base_model folder, should be project_path/base_model
    Path(project_path + "/base_model").mkdir(parents=True, exist_ok=True)
    logging_config.logging.info("Base model folder created: " + project_path + "/base_model")

    # create output folder, should be project_path/output
    Path(project_path + "/output").mkdir(parents=True, exist_ok=True)
    logging_config.logging.info("Output folder created: " + project_path + "/output")

    # ask if user want to set up training environment now?
    # if yes, run setup_scripts/create_training_env.py and pass project_path as argument
    # if no, exit
    setup_training_env = questionary.confirm(
        "Do you want to set up training environment now?"
    ).ask()
    
    train_env_path = None

    if setup_training_env:
        # ask where to create the training environment
        # default path is project_path + /training_env
        # the path must be empty or not exist
        train_env_path = questionary.text(
            "Where do you want to create the training environment?",
            default=project_path + "/training_env",
            validate=lambda text: not Path(text).exists() or (Path(text).is_dir() and len(list(Path(text).iterdir())) == 0),
            instruction="The path must be empty or not exist"
        ).ask()

        import modules.create_training_env as create_training_env
        # pass project path + train_env, and train type
        create_training_env.start(train_env_path, train_type)
    
    # ask if user want to create a train config now?
    create_train_config = questionary.confirm(
        "Do you want to create a train config now?"
    ).ask()

    train_config_path = None

    if create_train_config:
        # ask where to create the train config
        # default path is project_path + /train_config.yaml
        # the path must be not exist
        train_config_path = questionary.text(
            "Where do you want to create the train config?",
            default=project_path + "/train_config.yaml",
            validate=lambda text: not Path(text).exists(),
            instruction="The path must be not exist"
        ).ask()

        import modules.create_train_config as create_train_config
        train_config_path = create_train_config.start(project_path, train_config_path, train_type)


    # ask if user want to start training now?
    start_training = questionary.confirm(
        "Do you want to start training now?"
    ).ask()

    if start_training:
        import modules.start_training as start_training
        start_training.start(project_path, train_env_path, train_config_path, train_type)
    

if __name__ == '__main__':
    start()