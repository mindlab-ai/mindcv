# ConViT
> [ConViT: Improving Vision Transformers with Soft Convolutional Inductive Biases](https://arxiv.org/abs/2103.10697)

## Introduction

ConViT combines the strengths of convolutional architectures and Vision Transformers (ViTs). ConViT introduces gated positional self-attention (GPSA), a form of positional self-attention that can be equipped with a “soft” convolutional inductive bias. ConViT initializes the GPSA layers to mimic the locality of convolutional layers, then gives each attention head the freedom to escape locality by adjusting a gating parameter regulating the attention paid to position versus content information. ConViT, outperforms the DeiT (Touvron et al., 2020) on ImageNet, while offering a much improved sample efficiency.

<p align="center">
  <img src="https://github.com/mindspore-lab/mindcv/blob/main/configs/convit/convit.png" width=400 />  
</p>
<p align="center">
  <em>Figure 1. Architecture of ConViT</em>
</p>


## Results

<div align="center">

| Model            | Context   |  Top-1 (%)  | Top-5 (%)  |  Params (M)    |                                                 Recipe                                                 |                                       Download                                       | 
|------------------|-----------|-------------|------------|----------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| convit_tiny      | D910x8-G  | 73.66       | 91.72      | 5.71           | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/convit/convit_tiny_ascend.yaml)       | [weights](https://download.mindspore.cn/toolkits/mindcv/convit/convit_tiny.ckpt)       |
| convit_tiny_plus | D910x8-G  | 77.00       | 93.60      | 9.97           | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/convit/convit_tiny_plus_ascend.yaml)  | [weights](https://download.mindspore.cn/toolkits/mindcv/convit/convit_tiny_plus.ckpt)  |
| convit_small     | D910x8-G  | 81.63       | 95.59      | 27.78          | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/convit/convit_small_ascend.yaml)      | [weights](https://download.mindspore.cn/toolkits/mindcv/convit/convit_small.ckpt)      |
| convit_small_plus| D910x8-G  | 81.80       | 95.42      | 48.98          | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/convit/convit_small_plus_ascend.yaml) | [weights](https://download.mindspore.cn/toolkits/mindcv/convit/convit_small_plus.ckpt) |
| convit_base      | D910x8-G  | 82.10       | 95.52      | 86.54          | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/convit/convit_base_ascend.yaml)       | [weights](https://download.mindspore.cn/toolkits/mindcv/convit/convit_base.ckpt)       |
| convit_base_plus | D910x8-G  | 81.96       | 95.04      | 153.13         | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/convit/convit_base_plus_ascend.yaml)  | [weights](https://download.mindspore.cn/toolkits/mindcv/convit/convit_base_plus.ckpt)  |

</div>

#### Notes

- Context: Training context denoted as {device}x{pieces}-{MS mode}, where mindspore mode can be G - graph mode or F - pynative mode with ms function. For example, D910x8-G is for training on 8 pieces of Ascend 910 NPU using graph mode. 
- Top-1 and Top-5: Accuracy reported on the validation set of ImageNet-1K.  

## Quick Start

### Preparation

#### Installation
Please refer to the [installation instruction](https://github.com/mindspore-ecosystem/mindcv#installation) in MindCV.

#### Dataset Preparation
Please download the [ImageNet-1K](https://www.image-net.org/challenges/LSVRC/2012/index.php) dataset for model training and validation.

### Training

* Distributed Training

It is easy to reproduce the reported results with the pre-defined training recipe. For distributed training on multiple Ascend 910 devices, please run

```shell
# distrubted training on multiple GPU/Ascend devices
mpirun -n 8 python train.py --config configs/convit/convit_tiny_ascend.yaml --data_dir /path/to/imagenet
```
  
Similarly, you can train the model on multiple GPU devices with the above `mpirun` command.

For detailed illustration of all hyper-parameters, please refer to [config.py](https://github.com/mindspore-lab/mindcv/blob/main/config.py).

**Note:**  As the global batch size  (batch_size x num_devices) is an important hyper-parameter, it is recommended to keep the global batch size unchanged for reproduction or adjust the learning rate linearly to a new global batch size.

* Standalone Training

If you want to train or finetune the model on a smaller dataset without distributed training, please run:

```shell
# standalone training on a CPU/GPU/Ascend device
python train.py --config configs/convit/convit_tiny_ascend.yaml --data_dir /path/to/dataset --distribute False
```

### Validation

To validate the accuracy of the trained model, you can use `validate.py` and parse the checkpoint path with `--ckpt_path`.

```
python validate.py -c configs/convit/convit_tiny_ascend.yaml --data_dir /path/to/imagenet --ckpt_path /path/to/ckpt
```

### Deployment

Please refer to the [deployment tutorial](https://github.com/mindspore-lab/mindcv/blob/main/tutorials/deployment.md) in MindCV.
