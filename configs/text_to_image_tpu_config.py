import yaml
import questionary
import pathlib

# keys:
# --pretrained_model_name_or_path required

# Default value: None
# Value type: str
# --revision

# Default value: None
# Value type: str
# --dataset_name required

# Default value: None
# Value type: str
# --dataset_config_name

# Default value: None
# Value type: str
# --train_data_dir

# Default value: None
# Value type: str
# --image_column

# Default value: "image"
# Value type: str
# --caption_column

# Default value: "text"
# Value type: str
# --max_train_samples

# Default value: None
# Value type: int
# --output_dir required

# Default value: "sd-model-finetuned"
# Value type: str
# --cache_dir

# Default value: None
# Value type: str
# --seed

# Default value: 0
# Value type: int
# --resolution required

# Default value: 512
# Value type: int
# --center_crop

# Default value: False
# Value type: bool
# --random_flip

# Default value: False
# Value type: bool
# --train_batch_size required

# Default value: 16
# Value type: int
# --num_train_epochs required

# Default value: 100
# Value type: int
# --max_train_steps

# Default value: None
# Value type: int
# --learning_rate required

# Default value: 1e-4
# Value type: float
# --scale_lr

# Default value: False
# Value type: bool
# --lr_scheduler required

# Default value: "constant"
# Value type: str
# --adam_beta1

# Default value: 0.9
# Value type: float
# --adam_beta2

# Default value: 0.999
# Value type: float
# --adam_weight_decay

# Default value: 1e-2
# Value type: float
# --adam_epsilon

# Default value: 1e-08
# Value type: float
# --max_grad_norm

# Default value: 1.0
# Value type: float
# --push_to_hub

# Default value: False
# Value type: bool
# --hub_token

# Default value: None
# Value type: str
# --hub_model_id

# Default value: None
# Value type: str
# --logging_dir

# Default value: "logs"
# Value type: str
# --report_to

# Default value: "tensorboard"
# Value type: str
# --mixed_precision required

# Default value: "no"
# Value type: str
# --local_rank

# Default value: -1
# Value type: int

# main function
def start(project_path=None, train_config_path=None):

    if project_path is None:
        # ask where is the project path, check if exists
        # defualt is home path + project
        project_path = questionary.path(
            "project_path",
            default=str(pathlib.Path.home()) + "/project",
            validate=lambda text: pathlib.Path(text).exists()
        ).ask()

    if train_config_path is None:
        # default train_config_path is project path + train_config.yaml
        train_config_path = questionary.text(
            "train_config_path",
            default=project_path + "/train_config.yaml"
        ).ask()

    # ask user required keys

    pretrained_model_name_or_path = questionary.text(
        "pretrained_model_name_or_path",
        default="",
        validate=lambda text: text.isalnum() or text.isascii(),
    ).ask()

    dataset_name = questionary.text(
        "dataset_name",
        default="",
        validate=lambda text: text.isalnum() or text.isascii(),
    ).ask()

    output_dir = questionary.text(
        "output_dir",
        default=project_path + "/output",
        validate=lambda text: text.isalnum() or text.isascii(),
    ).ask()

    resolution = questionary.text(
        "resolution",
        default="512",
        validate=lambda text: text.isalnum() or text.isascii(),
    ).ask()

    train_batch_size = questionary.text(
        "train_batch_size",
        default="16",
        validate=lambda text: text.isalnum() or text.isascii(),
    ).ask()

    num_train_epochs = questionary.text(
        "num_train_epochs",
        default="100",
        validate=lambda text: text.isalnum() or text.isascii(),
    ).ask()

    learning_rate = questionary.text(
        "learning_rate",
        default="1e-4",
        validate=lambda text: text.isalnum() or text.isascii(),
    ).ask()

    lr_scheduler = questionary.select(
        "lr_scheduler",
        choices=["constant", "linear", "cosine", "cosine_with_restarts", "polynomial", "polynomial_with_restarts", "constant_with_warmup"],
        default="constant",
    ).ask()

    mixed_precision = questionary.select(
        "mixed_precision",
        choices=["no", "fp16", "bf16"],
        default="no",
    ).ask()


    # create a dict
    config_dict = {
        "pretrained_model_name_or_path": pretrained_model_name_or_path,
        "revision": None,
        "dataset_name": dataset_name,
        "dataset_config_name": None,
        "train_data_dir": None,
        "image_column": None,
        "caption_column": None,
        "max_train_samples": None,
        "output_dir": output_dir,
        "cache_dir": None,
        "seed": None,
        "resolution": resolution,
        "center_crop": None,
        "random_flip": None,
        "train_batch_size": train_batch_size,
        "num_train_epochs": num_train_epochs,
        "max_train_steps": None,
        "learning_rate": learning_rate,
        "scale_lr": None,
        "lr_scheduler": lr_scheduler,
        "adam_beta1": None,
        "adam_beta2": None,
        "adam_weight_decay": None,
        "adam_epsilon": None,
        "max_grad_norm": None,
        "push_to_hub": None,
        "hub_token": None,
        "hub_model_id": None,
        "logging_dir": None,
        "report_to": None,
        "mixed_precision": mixed_precision,
        "local_rank": None,
    }

    # save the dict to yaml file, to the train_config_path
    with open(train_config_path, 'w') as file:
        documents = yaml.dump(config_dict, file)

    # print success message
    print("Train config file created successfully!")


if __name__ == "__main__":
    start()
