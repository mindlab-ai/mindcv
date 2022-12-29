# MindCV

<p align="left">
    <a href="https://mindcv.readthedocs.io/en/latest">
        <img alt="docs" src="https://img.shields.io/badge/docs-latest-blue">
    </a>
    <a href="https://github.com/mindspore-lab/mindcv/blob/main/LICENSE">
        <img alt="GitHub" src="https://img.shields.io/github/license/mindspore-lab/mindcv.svg">
    </a>
    <a href="https://github.com/mindspore-lab/mindcv/pulls">
        <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-pink.svg">
    </a>
    <a href="https://github.com/mindspore-lab/mindcv/issues">
        <img alt="open issues" src="https://img.shields.io/github/issues/mindspore-lab/mindcv">
    </a>
    <!---
    <a href="https://github.com/mindspore-lab/mindcv/tags">
        <img alt="GitHub tags" src="https://img.shields.io/github/tags/mindspore-lab/mindcv">
    </a>
    -->
</p>

| **Build Type**   |`Linux`           |`MacOS`           |`Windows`         |
| :---:            | :---:            | :---:            | :---:            |
| **Build Status** | [![Status](https://github.com/mindspore-lab/mindcv/actions/workflows/main.yml/badge.svg)](https://github.com/mindspore-lab/mindcv/actions) | [![Status](https://github.com/mindspore-lab/mindcv/actions/workflows/mac.yml/badge.svg)](https://github.com/mindspore-lab/mindcv/actions) | Not tested|

[简介](#简介) |
[安装](#安装) |
[快速入门](#快速入门) |
[教程](#教程) |
[模型列表](#模型列表) |
[支持算法](#支持算法) |
[日志](#日志)

## 简介

MindCV是一个基于 [MindSpore](https://www.mindspore.cn/)
开发的，致力于计算机视觉相关技术研发的开源工具箱。它提供大量的计算机视觉领域的经典模型和SoTA模型以及它们的预训练权重。同时，还提供了AutoAugment等SoTA算法来提高性能。通过解耦的模块设计，您可以轻松地将MindCV应用到您自己的CV任务中。

<details open>
<summary> 主要特性 </summary>

- **高易用性** MindCV将视觉框架分解为各种可配置组件，方便您使用MindCV定制您的数据管道、模型和学习管道。

```python
>>> import mindcv
# 创建一个数据集
>>> dataset = mindcv.create_dataset('cifar10', download=True)
# 创建一个模型
>>> network = mindcv.create_model('resnet50', pretrained=True)
```

用户可以在一个命令行中自定义和启动他们的迁移学习或训练任务。

```shell
# 仅使用一个命令行即可启动迁移学习任务
python train.py --model swin_tiny --pretrained --opt adamw --lr 0.001 --data_dir = {data_dir} 
```

- **业内最佳** MindCV提供了大量包括SwinTransformer在内的基于CNN和基于Transformer结构的视觉模型。同时，还提供了它们的预训练权重以及性能测试报告，帮助用户正确地选择和使用他们所需要的模型。

- **灵活高效** MindCV是基于新一代高效的深度学习框架MindSpore编写的，可以运行在多种硬件平台上（CPU/GPU/Ascend），还同时支持高效的图模式和灵活的调试模式。

</details>

### 性能报告

使用MindCV进行训练的模型测试结果汇总在[benchmark_results.md](./benchmark_results.md)，测试使用的是标准的ImageNet测试集。

## 安装

### 依赖

- mindspore >= 1.8.1
- numpy >= 1.17.0
- pyyaml >= 5.3
- tqdm
- openmpi 4.0.3 (for distributed mode)

运行以下脚本，安装相关依赖。

```shell
pip install -r requirements.txt
```

用户可遵从[官方指导](https://www.mindspore.cn/install) 并根据自身使用的硬件平台选择最适合您的MindSpore版本来进行安装。如果需要在在分布式条件下使用，还需安装[openmpi](https://www.open-mpi.org/software/ompi/v4.0/) 。

之后的说明将默认用户已正确安装好相关依赖。

<!---
### pip安装

MindCV可以通过pip安装。

```shell
pip install https://github.com/mindspore-lab/mindcv/releases/download/v0.0.1-beta/mindcv-0.0.1b0-py3-none-any.whl
```
-->

### 源码安装

运行以下脚本，通过源码安装MindCV。

```shell
pip install git+https://github.com/mindspore-lab/mindcv.git
```

> 注：MindCV可以在Linux和Mac系统安装，但是目前还不能在Windows系统上安装。

## 快速入门

### 动手教程

在开始上手MindCV前，可以阅读MindCV的[迁移学习教程](tutorials/finetune_CN.ipynb)，该教程可以帮助用户快速了解MindCV的各个重要组件以及训练、验证、测试流程。

以下是一些供您练习的代码片段。

```python
>>> import mindcv
# List and find a pretrained vision model 列出满足条件的预训练模型名称
>>> mindcv.list_models("swin*", pretrained=True)
['swin_tiny']
# 创建模型
>>> network = mindcv.create_model('swin_tiny', pretrained=True)
# 验证模型的准确率
>>> !python validate.py - -model = swin_tiny - -pretrained - -dataset = imagenet - -val_split = validation
{'Top_1_Accuracy': 0.808343989769821, 'Top_5_Accuracy': 0.9527253836317136, 'loss': 0.8474242982580839}
```

**图片分类示例**

<p align="left">
  <img src="./tutorials/data/test/dog/dog.jpg" width=360 />
</p>

使用加载了预训练参数的SoTA模型对一张图片进行推理。

```python
>>> !python
infer.py - -model = swin_tiny - -image_path = './tutorials/data/test/dog/dog.jpg'
{'Labrador retriever': 0.5700152, 'golden retriever': 0.034551315, 'kelpie': 0.010108651,
 'Chesapeake Bay retriever': 0.008229004, 'Walker hound, Walker foxhound': 0.007791956}
```

预测结果排名前1的是拉布拉多犬，正是这张图片里的狗狗的品种。

### 训练和验证

使用MindCV，用户可以很容易地在标准数据集或自定义数据集上训练模型。仅几行代码就可以完成模型训练、迁移学习、模型验证等任务。

- 单卡训练

用户可以使用`train.py`便捷地进行模型训练。下面是一个示例是在CIFAR10数据集上单卡训练DenseNet（单卡GPU）。

```shell
python train.py --model resnet50 --dataset cifar10 --dataset_download
```

更多参数说明，请运行`python train.py --help'。用户可以便捷地修改模型名称，优化器等其他超参。

**训练过程中进行验证** 要跟踪训练期间验证精度的变化，请启用参数`--val_while_train`。

```shell
python train.py -model resnet50 -dataset cifar10 -val_while_train -val_split test -val_interval 1
``` 

每个轮次的训练损失和验证精度将保存在`{ckpt_save_dir}/results.log`中。

**恢复训练** 要恢复训练，需要为恢复的指定检查点`--ckpt_path`和`--ckpt_save_dir`。包括上一轮次的学习率在内的优化器状态也将被恢复。

```shell
python train.py --model resnet50 --dataset cifar10 --ckpt_save_dir checkpoints --ckpt_path checkpoints/resnet50_30-100.ckpt
``` 

- 分布式训练

对于像ImageNet这样的大型数据集，有必要在多个设备上以分布式模式进行训练，MindCV对分布式相关功能支持良好。以下脚本是在ImageNet上使用4个GPU训练DenseNet121的示例。

```shell
export CUDA_VISIBLE_DEVICES=0,1,2,3  # suppose there are 4 GPUs
mpirun --allow-run-as-root -n 4 python train.py --distribute \
	--model densenet121 --dataset imagenet --data_dir ./datasets/imagenet   
```

- Yaml文件设置

用户可以使用yaml文件或设置外部参数来指定要使用的模型等其他组件。以下是使用预设的yaml文件进行训练的示例。

```shell
mpirun --allow-run-as-root -n 4 python train.py -c configs/squeezenet/squeezenet_1.0_gpu.yaml    
```

**用于模型训练的参数文件汇总在[`configs`](configs)文件夹中。**

- 验证

使用`validate.py`可以便捷地验证训练好的模型。

```shell
# 验证模型的预训练参数
python validate.py --model resnet50 --dataset imagenet --val_split validation --ckpt_path './ckpt/densenet121-best.ckpt' 
``` 

- 使用ms_function的调试模式 (高级)

在默认情况下，训练管道（`train.py`）在[图模式](https://www.mindspore.cn/tutorials/zh-CN/r1.8/advanced/pynative_graph/mode.html) 下运行，虽然在该模型下运行的性能极佳，但是该模式不方便进行调试。为了方便调试，用户可以使用参数`--mode`将运行模式设置为调试模式。


[使用ms_function的调试模式](https://www.mindspore.cn/tutorials/zh-CN/r1.8/advanced/pynative_graph/combine.html) 是兼顾了MindSpore的效率和灵活的混合模式。用户可通过使用`train_with_func.py`文件来使用该混合模式进行训练。

```shell
python train_with_func.py --model resnet50 --dataset cifar10 --dataset_download --epoch_size 10  
```

更多教程请参见[examples/scripts](examples/scripts)。

## 教程

我们提供了[jupyter notebook格式的教程](tutorials)

- [了解模型配置](tutorials/learn_about_config_CN.ipynb)
- [模型推理](tutorials/inference_CN.ipynb)
- [自定义数据集上的模型微调训练](tutorials/finetune_CN.ipynb)
- [定制化模型] //coming soon
- [vision transformer性能优化] //coming soon
- [部署推理服务](tutorials/deployment_CN.ipynb)

## 模型列表

目前，MindCV支持以下列出的模型族。更多包含预训练权重的模型正在开发中，将于近期发布。

<details open>
<summary> 支持模型 </summary>

* Big Transfer ResNetV2 (BiT) - https://arxiv.org/abs/1912.11370
* ConvNeXt - https://arxiv.org/abs/2201.03545
* ConViT (Soft Convolutional Inductive Biases Vision Transformers)- https://arxiv.org/abs/2103.10697
* DenseNet - https://arxiv.org/abs/1608.06993
* DPN (Dual-Path Network) - https://arxiv.org/abs/1707.01629
* EfficientNet (MBConvNet Family) https://arxiv.org/abs/1905.11946
* EfficientNet V2 - https://arxiv.org/abs/2104.00298
* GhostNet - https://arxiv.org/abs/1911.11907
* GoogleNet - https://arxiv.org/abs/1409.4842
* Inception-V3 - https://arxiv.org/abs/1512.00567
* Inception-ResNet-V2 and Inception-V4 - https://arxiv.org/abs/1602.07261
* MNASNet - https://arxiv.org/abs/1807.11626
* MobileNet-V1 - https://arxiv.org/abs/1704.04861
* MobileNet-V2 - https://arxiv.org/abs/1801.04381
* MobileNet-V3 (MBConvNet w/ Efficient Head) - https://arxiv.org/abs/1905.02244
* NASNet - https://arxiv.org/abs/1707.07012
* PNasNet - https://arxiv.org/abs/1712.00559
* PVT (Pyramid Vision Transformer) - https://arxiv.org/abs/2102.12122
* PoolFormer models - https://github.com/sail-sg/poolformer
* RegNet - https://arxiv.org/abs/2003.13678
* RepMLP https://arxiv.org/abs/2105.01883
* RepVGG - https://arxiv.org/abs/2101.03697
* ResNet (v1b/v1.5) - https://arxiv.org/abs/1512.03385
* ResNeXt - https://arxiv.org/abs/1611.05431
* Res2Net - https://arxiv.org/abs/1904.01169
* ReXNet - https://arxiv.org/abs/2007.00992
* ShuffleNet v1 - https://arxiv.org/abs/1707.01083
* ShuffleNet v2 - https://arxiv.org/abs/1807.11164
* SKNet - https://arxiv.org/abs/1903.06586
* SqueezeNet - https://arxiv.org/abs/1602.07360
* Swin Transformer - https://arxiv.org/abs/2103.14030
* VGG - https://arxiv.org/abs/1409.1556
* Visformer - https://arxiv.org/abs/2104.12533
* Vision Transformer (ViT) - https://arxiv.org/abs/2010.11929
* Xception - https://arxiv.org/abs/1610.02357

更多关于模型性能和预训练权重的信息请查看 [configs](./configs) 文件夹。

</details>

## 支持算法

<details open>
<summary> 支持算法 </summary>

* 数据增强
    * [AutoAugment](https://arxiv.org/abs/1805.09501)
    * [RandAugment](https://arxiv.org/abs/1909.13719)
    * [Repeated Augmentation](https://openaccess.thecvf.com/content_CVPR_2020/papers/Hoffer_Augment_Your_Batch_Improving_Generalization_Through_Instance_Repetition_CVPR_2020_paper.pdf)
    * RandErasing (Cutout)
    * CutMix
    * Mixup
    * RandomResizeCrop
    * Color Jitter, Flip, etc
* 优化率
    * Adam
    * Adamw
    * Adan (experimental)
    * AdaGrad
    * LAMB
    * Momentum
    * RMSProp
    * SGD
    * NAdam
* 学习率策略
    * Warmup Cosine Decay
    * Step LR
    * Polynomial Decay
    * Exponential Decay
* 正则化
    * Weight Decay
    * Label Smoothing
    * Stochastic Depth (depends on networks)
    * Dropout (depends on networks)
* 损失函数
    * Cross Entropy (w/ class weight and auxilary logit support)
    * Binary Cross Entropy  (w/ class weight and auxilary logit support)
    * Soft Cross Entropy Loss (automatically enabled if mixup or label smoothing is used)
    * Soft Binary Cross Entropy Loss (automatically enabled if mixup or label smoothing is used)
* 融合
    * Warmup EMA (Exponential Moving Average)

</details>

## 日志

### 更新

- 2022/12/09

1. 支持在所有学习率策略中添加学习率预热操作，除cosine decay策略外。
2. 支持`Repeated Augmenation`操作，可以通过`--aug_repeats`对其进行设置，设置值应大于1(通常为3或4)。
3. 支持EMA。
4. 通过支持mixup和cutmix操作进一步优化BCE损失函数。

- 2022/11/21

1. 支持模型损失和正确率的可视化。
2. 支持伦次维度的cosine decay策略的学习率预热操作（之前仅支持步维度）。

- 2022/11/09

1. 支持2个ViT预训练模型。
2. 支持RandAugment augmentation操作。
3. 提高了CutMix操作的可用性，CutMix和Mixup目前可以一起使用。
4. 解决了学习率画图的bug。

- 2022/10/12

1. BCE和CE损失函数目前都支持class-weight config操作、label smoothing操作、auxilary logit input操作（适用于类似Inception模型）。

- 2022/09/13

1. 支持Adan优化器(试用版)。

### 贡献方式

我们感谢包括提出问题和代码提交等在内的所有形式的贡献，来让MindCV变得更好。

有关贡献指南，请参阅[CONTRIBUTING.md](CONTRIBUTING.md)。请遵循[模型编写指南](mindcv/models/model_template_CN.md)所规定的规则来贡献模型接口：)

### 许可证

本项目在[Apache License 2.0](License.md)下发布。

### 声明

MindCV是一个开源项目，欢迎任何形式的贡献和反馈。我们希望MindCV可以通过提供灵活和标准化的工具包来服务于相关的研究群体，帮助他们快速复现已有的方法并开发自己的新的计算机视觉方法。

### 引用

如果你觉得该项目对你的项目有帮助，请考虑引用我们的项目：

```latex
@misc{MindSpore Computer Vision 2022,
    title={{MindSpore Computer  Vision}:MindSpore Computer Vision Toolbox and Benchmark},
    author={MindSpore Vision Contributors},
    howpublished = {\url{https://github.com/mindlab-ecosystem/mindcv/}},
    year={2022}
}
```
