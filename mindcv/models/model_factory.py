from typing import List

from .helpers import load_model_checkpoint
from .registry import is_model, model_entrypoint

__all__ = ["create_model"]


def create_model(
    model_name: str,
    num_classes: int = 1000,
    pretrained: bool = False,
    in_channels: int = 3,
    checkpoint_path: str = "",
    ema: bool = False,
    **kwargs,
):
    r"""Creates model by name.

    Args:
        model_name (str):  The name of model.
        num_classes (int): The number of classes. Default: 1000.
        pretrained (bool): Whether to load the pretrained model. Default: False.
        in_channels (int): The input channels. Default: 3.
        checkpoint_path (str): The path of checkpoint files. Default: "".
        ema (bool): Whether use ema method. Default: False.
    """

    if checkpoint_path != "" and pretrained:
        raise ValueError("checkpoint_path is mutually exclusive with pretrained")

    model_args = dict(num_classes=num_classes, pretrained=pretrained, in_channels=in_channels)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    if not is_model(model_name):
        raise RuntimeError(f"Unknown model {model_name}")

    create_fn = model_entrypoint(model_name)
    model = create_fn(**model_args, **kwargs)

    if checkpoint_path:
        load_model_checkpoint(model, checkpoint_path, ema)

    return model
