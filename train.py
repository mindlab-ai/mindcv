import mindspore as ms
import mindspore.nn as nn
from mindspore import FixedLossScaleManager, Model, LossMonitor, TimeMonitor, CheckpointConfig, ModelCheckpoint
from mindspore.communication import init, get_rank, get_group_size

from mindcv.models import create_model
from mindcv.data import create_dataset, create_transforms, create_loader
from mindcv.loss import create_loss
from mindcv.optim import create_optimizer
from mindcv.scheduler import create_scheduler
from mindcv.utils import ValAccSaveMonitor, LossAccSummary
from config import parse_args

ms.set_seed(1)


def train(args):
    ms.set_context(mode=args.mode)

    if args.distribute:
        init()
        device_num = get_group_size()
        rank_id = get_rank()
        ms.set_auto_parallel_context(device_num=device_num,
                                     parallel_mode='data_parallel',
                                     gradients_mean=True)
    else:
        device_num = None
        rank_id = None

    # create dataset
    dataset_train = create_dataset(
        name=args.dataset,
        root=args.data_dir,
        split=args.train_split,
        shuffle=args.shuffle,
        num_samples=args.num_samples,
        num_shards=device_num,
        shard_id=rank_id,
        num_parallel_workers=args.num_parallel_workers,
        download=args.dataset_download)

    dataset_eval = create_dataset(
        name=args.dataset,
        root=args.data_dir,
        split=args.val_split,
        num_parallel_workers=args.num_parallel_workers,
        download=args.dataset_download)

    # create transforms
    transform_list = create_transforms(
        dataset_name=args.dataset,
        is_training=True,
        image_resize=args.image_resize,
        scale=args.scale,
        ratio=args.ratio,
        hflip=args.hflip,
        vflip=args.vflip,
        color_jitter=args.color_jitter,
        interpolation=args.interpolation,
        auto_augment=args.auto_augment,
        mean=args.mean,
        std=args.std,
        re_prob=args.re_prob,
        re_scale=args.re_scale,
        re_ratio=args.re_ratio,
        re_value=args.re_value,
        re_max_attempts=args.re_max_attempts
    )

    transform_list_eval = create_transforms(
        dataset_name=args.dataset,
        is_training=False,
        image_resize=args.image_resize,
        crop_pct=args.crop_pct,
        interpolation=args.interpolation,
        mean=args.mean,
        std=args.std
    )

    # load dataset
    loader_train = create_loader(
        dataset=dataset_train,
        batch_size=args.batch_size,
        drop_remainder=args.drop_remainder,
        is_training=True,
        mixup=args.mixup,
        num_classes=args.num_classes,
        transform=transform_list,
        num_parallel_workers=args.num_parallel_workers,
    )

    loader_eval = create_loader(
        dataset=dataset_eval,
        batch_size=args.batch_size,
        drop_remainder=False,
        is_training=False,
        transform=transform_list_eval,
        num_parallel_workers=args.num_parallel_workers,
    )

    steps_per_epoch = loader_train.get_dataset_size()

    # create model
    network = create_model(model_name=args.model,
                           num_classes=args.num_classes,
                           in_channels=args.in_channels,
                           drop_rate=args.drop_rate,
                           drop_path_rate=args.drop_path_rate,
                           pretrained=args.pretrained,
                           checkpoint_path=args.ckpt_path)

    # create loss
    loss = create_loss(name=args.loss,
                       reduction=args.reduction,
                       label_smoothing=args.label_smoothing,
                       aux_factor=args.aux_factor)

    # create learning rate schedule
    lr_scheduler = create_scheduler(steps_per_epoch,
                                    scheduler=args.scheduler,
                                    lr=args.lr,
                                    min_lr=args.min_lr,
                                    warmup_epochs=args.warmup_epochs,
                                    decay_epochs=args.decay_epochs,
                                    decay_rate=args.decay_rate)

    # create optimizer
    #TODO: consistent naming opt, name, dataset_name 
    #TODO: network as input param can be simpler.   
    optimizer = create_optimizer(network.trainable_params(),
                                 opt=args.opt,
                                 lr=lr_scheduler,
                                 weight_decay=args.weight_decay,
                                 momentum=args.momentum,
                                 nesterov=args.use_nesterov,
                                 filter_bias_and_bn=args.filter_bias_and_bn,
                                 loss_scale=args.loss_scale)
    
    # TODO: this following code for training the network is too complex!! Needs to be simplified! warp into a trainer? 
    # Define eval metrics.
    eval_metrics = {'Top_1_Accuracy': nn.Top1CategoricalAccuracy(),
                    'Top_5_Accuracy': nn.Top5CategoricalAccuracy()}
    # init model
    if args.loss_scale > 1.0:
        loss_scale_manager = FixedLossScaleManager(loss_scale=args.loss_scale, drop_overflow_update=False)
        model = Model(network, loss_fn=loss, optimizer=optimizer, metrics=eval_metrics, amp_level=args.amp_level,
                      loss_scale_manager=loss_scale_manager)
    else:
        model = Model(network, loss_fn=loss, optimizer=optimizer, metrics=eval_metrics, amp_level=args.amp_level)

    # callback
    loss_cb = LossMonitor(per_print_times=steps_per_epoch)
    time_cb = TimeMonitor(data_size=steps_per_epoch)
    callbacks = [loss_cb, time_cb]
    ckpt_config = CheckpointConfig(
        save_checkpoint_steps=int(steps_per_epoch * args.ckpt_save_interval),
        keep_checkpoint_max=args.keep_checkpoint_max)
    ckpt_cb = ModelCheckpoint(prefix=args.model,
                              directory=args.ckpt_save_dir,
                              config=ckpt_config)
    if args.val_while_train:
        val_cb = ValAccSaveMonitor(model, loader_eval, metric_name="Top_1_Accuracy",
                                   ckpt_dir=args.ckpt_save_dir,
                                   best_ckpt_name=args.model + '_best.ckpt',
                                   dataset_sink_mode=args.dataset_sink_mode)

    if args.summary:
        summary_dir = "./summary_dir/summary"
        summary_collector = LossAccSummary(summary_dir, model, loader_eval, metric_name="Top_1_Accuracy")
    if args.distribute:
        if rank_id == 0:
            callbacks.append(ckpt_cb)
            if args.val_while_train:
                callbacks.append(val_cb)
            if args.summary:
                callbacks.append(summary_collector)
    else:
        callbacks.append(ckpt_cb)
        if args.val_while_train:
            callbacks.append(val_cb)
        if args.summary:
            callbacks.append(summary_collector)

    # train model
    model.train(args.epoch_size, loader_train, callbacks=callbacks, dataset_sink_mode=args.dataset_sink_mode)


if __name__ == '__main__':
    args = parse_args()
    train(args)
