import yaml
import questionary
import pathlib

# keys:
# name, value_type, default_value
# --pretrained_model_name_or_path str None required
# --revision str None
# --tokenizer_name str None
# --instance_data_dir str None required
# --class_data_dir str None required
# --instance_prompt str None required
# --class_prompt str None required
# --validation_prompt str None
# --num_validation_images int 4
# --validation_epochs int 50
# --with_prior_preservation bool False required
# --prior_loss_weight float 1.0 required
# --num_class_images int 100
# --output_dir str lora-dreambooth-model required
# --seed int None
# --resolution int 512 required
# --center_crop bool False
# --train_text_encoder bool False required
# --train_batch_size int 4 required
# --sample_batch_size int 4
# --num_train_epochs int 1 required
# --max_train_steps int None
# --checkpointing_steps int 500
# --checkpoints_total_limit int None
# --resume_from_checkpoint str None
# --gradient_accumulation_steps int 1
# --gradient_checkpointing bool False required
# --learning_rate float 5e-4 required
# --scale_lr bool False
# --lr_scheduler str constant required
# --lr_warmup_steps int 500
# --lr_num_cycles int 1
# --lr_power float 1.0
# --dataloader_num_workers int 0
# --use_8bit_adam bool False required
# --adam_beta1 float 0.9
# --adam_beta2 float 0.999
# --adam_weight_decay float 1e-2
# --adam_epsilon float 1e-08
# --max_grad_norm float 1.0
# --push_to_hub bool False
# --hub_token str None
# --hub_model_id str None
# --logging_dir str logs
# --allow_tf32 bool False
# --report_to str tensorboard
# --mixed_precision str None required
# --prior_generation_precision str None
# --local_rank int -1
# --enable_xformers_memory_efficient_attention bool False required
# --pre_compute_text_embeddings bool False
# --tokenizer_max_length int None
# --text_encoder_use_attention_mask bool False
# --validation_images list None
# --class_labels_conditioning str None

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
        default="None",
        validate=lambda text: text.isalnum() or text.isascii(),
    ).ask()

    instance_data_dir = questionary.text(
        "instance_data_dir",
        default=project_path + "/data"
    ).ask()

    class_data_dir = questionary.text(
        "class_data_dir",
        default=project_path + "/reg_data"
    ).ask()

    instance_prompt = questionary.text(
        "instance_prompt",
        default="A photo of a person"
    ).ask()

    class_prompt = questionary.text(
        "class_prompt",
        default="A photo of a person"
    ).ask()

    with_prior_preservation = questionary.confirm(
        "with_prior_preservation",
        default=True
    ).ask()

    if with_prior_preservation:
        prior_loss_weight = questionary.text(
            "prior_loss_weight",
            default="1.0"
        ).ask()
    else:
        prior_loss_weight = None

    num_class_images = questionary.text(
        "num_class_images",
        default="100",
        validate=lambda text: text.isnumeric(),
    ).ask()

    output_dir = questionary.text(
        "output_dir",
        default=project_path + "/output"
    ).ask()

    resolution = questionary.text(
        "resolution",
        default="512"
    ).ask()

    train_text_encoder = questionary.confirm(
        "train_text_encoder",
        default=True
    ).ask()

    train_batch_size = questionary.text(
        "train_batch_size",
        default=4,
        validate=lambda text: text.isnumeric(),
    ).ask()

    num_train_epochs = questionary.text(
        "num_train_epochs",
        default=100,
        validate=lambda text: text.isnumeric(),
    ).ask()

    gradient_checkpointing = questionary.confirm(
        "gradient_checkpointing",
        default=True
    ).ask()

    if gradient_checkpointing:
        gradient_accumulation_steps = questionary.text(
            "gradient_accumulation_steps",
            default=1,
            validate=lambda text: text.isnumeric(),
        ).ask()
    else:
        gradient_accumulation_steps = None
    
    learning_rate = questionary.text(
        "learning_rate",
        default="5e-4"
    ).ask()

    lr_scheduler = questionary.select(
        "lr_scheduler",
        choices=["constant", "linear", "cosine", "cosine_with_restarts", "polynomial", "polynomial_with_restarts", "cosine_with_hard_restarts"],
        default="constant"
    ).ask()

    use_8bit_adam = questionary.confirm(
        "use_8bit_adam",
        default=False
    ).ask()

    if use_8bit_adam:
        adam_beta1 = questionary.text(
            "adam_beta1",
            default=0.9
        ).ask()
        adam_beta2 = questionary.text(
            "adam_beta2",
            default=0.999
        ).ask()
        adam_weight_decay = questionary.text(
            "adam_weight_decay",
            default="1e-2"
        ).ask()
        adam_epsilon = questionary.text(
            "adam_epsilon",
            default="1e-8"
        ).ask()
    else:
        adam_beta1 = None
        adam_beta2 = None
        adam_weight_decay = None
        adam_epsilon = None

    mixed_precision = questionary.select(
        "mixed_precision",
        choices=["no", "fp16", "bf16"],
        default="no"
    ).ask()

    enable_xformers_memory_efficient_attention = questionary.confirm(
        "enable_xformers_memory_efficient_attention",
        default=False
    ).ask()


    # create a dict
    config_dict = {
        "pretrained_model_name_or_path": pretrained_model_name_or_path,
        "revision": None,
        "tokenizer_name": None,
        "instance_data_dir": instance_data_dir,
        "class_data_dir": class_data_dir,
        "instance_prompt": instance_prompt,
        "class_prompt": class_prompt,
        "validation_prompt": None,
        "num_validation_images": None,
        "validation_epochs": None,
        "with_prior_preservation": with_prior_preservation,
        "prior_loss_weight": prior_loss_weight,
        "num_class_images": num_class_images,
        "output_dir": output_dir,
        "seed": None,
        "resolution": resolution,
        "center_crop": None,
        "train_text_encoder": train_text_encoder,
        "train_batch_size": train_batch_size,
        "sample_batch_size": None,
        "num_train_epochs": num_train_epochs,
        "max_train_steps": None,
        "checkpointing_steps": None,
        "checkpoints_total_limit": None,
        "resume_from_checkpoint": None,
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "gradient_checkpointing": gradient_checkpointing,
        "learning_rate": learning_rate,
        "scale_lr": None,
        "lr_scheduler": lr_scheduler,
        "lr_warmup_steps": None,
        "lr_num_cycles": None,
        "lr_power": None,
        "dataloader_num_workers": None,
        "use_8bit_adam": use_8bit_adam,
        "adam_beta1": adam_beta1,
        "adam_beta2": adam_beta2,
        "adam_weight_decay": adam_weight_decay,
        "adam_epsilon": adam_epsilon,
        "max_grad_norm": None,
        "push_to_hub": None,
        "hub_token": None,
        "hub_model_id": None,
        "logging_dir": None,
        "allow_tf32": None,
        "report_to": None,
        "mixed_precision": mixed_precision,
        "prior_generation_precision": None,
        "local_rank": None,
        "enable_xformers_memory_efficient_attention": enable_xformers_memory_efficient_attention,
        "pre_compute_text_embeddings": None,
        "tokenizer_max_length": None,
        "text_encoder_max_length": None,
    }

    # save the dict to yaml file, to the train_config_path
    with open(train_config_path, 'w') as file:
        documents = yaml.dump(config_dict, file)

    # print success message
    print("Train config file created: train_config.yaml")


if __name__ == "__main__":
    start()