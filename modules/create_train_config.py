import pathlib
import questionary

def start(project_path=None, train_config_path=None, train_type=None):
    # if project_path is not specified, ask user where to create the project
    if project_path == None:
        project_path = questionary.text(
            "Where is the project?",
            default=str(pathlib.Path.home()) + "/project"
        ).ask()

    # if config_path is not specified, ask user where to store the config file
    if train_config_path == None:
        train_config_path = questionary.text(
            "Where do you want to store the config file?",
            default=str(pathlib.Path.home()) + "/project/train_config.json"
        ).ask()
    
    # if train_type is not specified, ask user to choose a train type
    if train_type == None:
        train_type = questionary.select(
            "Which type of training project do you want to create?",
            choices=[
                "[1] [GPU]dreambooth-lora",
                "[2] [GPU]dreambooth",
                "[3] [GPU]text-to-image",
                "[4] [TPU]dreambooth",
                "[5] [TPU]text-to-image"
            ]
        ).ask()
    
    # create the config file
    # if train_type == "[1] [GPU]dreambooth-lora":
    # user configs/dreambooth-lora-config's start(project_path)
    if train_type == "[1] [GPU]dreambooth-lora":
        from configs.dreambooth_lora_config import start
        start(train_config_path)
    elif train_type == "[5] [TPU]text-to-image":
        from configs.text_to_image_tpu_config import start
        start(train_config_path)
    
    return train_config_path

if __name__ == "__main__":
    start()
