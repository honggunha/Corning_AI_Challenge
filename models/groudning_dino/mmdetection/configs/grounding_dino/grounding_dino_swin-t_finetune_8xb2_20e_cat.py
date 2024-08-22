_base_ = 'grounding_dino_swin-t_finetune_16xb2_1x_coco.py'

data_root = 'data/'
class_name = ('Defect1', 'Defect2', 'Defect3', 'Defect4', 'Defect5')
num_classes = len(class_name)
metainfo = dict(classes=class_name, palette = [(220, 20, 60), (119, 11, 32), (0, 0, 142), (0, 255, 0), (255, 165, 0)])

model = dict(bbox_head=dict(num_classes=num_classes))

train_dataloader = dict(
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='train/_annotations.coco.json',
        data_prefix=dict(img='train/images/')))

val_dataloader = dict(
    dataset=dict(
        metainfo=metainfo,
        data_root=data_root,
        ann_file='test/_annotations.coco.json',
        data_prefix=dict(img='test/images')))

test_dataloader = val_dataloader

val_evaluator = dict(ann_file=data_root + 'test/_annotations.coco.json')
test_evaluator = val_evaluator

max_epoch = 10

default_hooks = dict(
    checkpoint=dict(interval=1, max_keep_ckpts=1, save_best='auto'),
    logger=dict(type='LoggerHook', interval=5))
train_cfg = dict(max_epochs=max_epoch, val_interval=1)

param_scheduler = [
    dict(type='LinearLR', start_factor=0.001, by_epoch=False, begin=0, end=30),
    dict(
        type='MultiStepLR',
        begin=0,
        end=max_epoch,
        by_epoch=True,
        milestones=[15],
        gamma=0.1)
]

optim_wrapper = dict(
    optimizer=dict(lr=0.00005),
    paramwise_cfg=dict(
        custom_keys={
            'absolute_pos_embed': dict(decay_mult=0.),
            'backbone': dict(lr_mult=0.1),
            'language_model': dict(lr_mult=0),
        }))

auto_scale_lr = dict(base_batch_size=16)
