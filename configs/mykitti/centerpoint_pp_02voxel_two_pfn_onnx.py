import itertools
import logging

from det3d.utils.config_tool import get_downsample_factor

tasks = [
    dict(num_class=1, class_names=["Car"]),
    # dict(num_class=1, class_names=["Cart"]),
    # dict(num_class=2, class_names=["truck", "construction_vehicle"]),
    # dict(num_class=2, class_names=["bus", "trailer"]),
    # dict(num_class=1, class_names=["barrier"]),
    # dict(num_class=2, class_names=["motorcycle", "bicycle"]),
    # dict(num_class=2, class_names=["pedestrian", "traffic_cone"]),
]

class_names = list(itertools.chain(*[t["class_names"] for t in tasks]))

# training and testing settings
target_assigner = dict(
    tasks=tasks,
)


# model settings
model = dict(
    type="PointPillars",
    pretrained=None,
    export_onnx=True,
    reader=dict(
        type="PillarFeatureNet",
        num_filters=[64, 64],
        num_input_features=3, #changed
        with_distance=False,
        voxel_size=(0.2, 0.2, 10),
        # pc_range=(-51.2, -51.2, -5.0, 51.2, 51.2, 3.0),
        pc_range=(0, -40, -10, 160, 40, 0),
        export_onnx=True,
    ),
    backbone=dict(type="PointPillarsScatter", ds_factor=1),
    neck=dict(
        type="RPN",
        layer_nums=[3, 5, 5],
        ds_layer_strides=[2, 2, 2],
        ds_num_filters=[64, 128, 256],
        us_layer_strides=[0.5, 1, 2],
        us_num_filters=[128, 128, 128],
        num_input_features=64,
        logger=logging.getLogger("RPN"),
    ),
    bbox_head=dict(
        # type='RPNHead',
        type="CenterHead",
        in_channels=sum([128, 128, 128]),
        tasks=tasks,
        dataset='nuscenes',
        weight=0.25,
        # code_weights=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.2, 0.2, 1.0, 1.0],
        code_weights=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.2, 0.2],
        # common_heads={'reg': (2, 2), 'height': (1, 2), 'dim':(3, 2), 'rot':(2, 2), 'vel': (2, 2)}, # (output_channel, num_conv)
        common_heads={'reg': (2, 2), 'height': (1, 2), 'dim':(3, 2), 'rot':(2, 2)},# (output_channel, num_conv)
    ),
)

assigner = dict(
    target_assigner=target_assigner,
    out_size_factor=get_downsample_factor(model),
    gaussian_overlap=0.1,
    max_objs=500,
    min_radius=2,
)


train_cfg = dict(assigner=assigner)

test_cfg = dict(
    # post_center_limit_range=[-61.2, -61.2, -10.0, 61.2, 61.2, 10.0],
    post_center_limit_range=[0, -40, -10, 160, 40, 0],
    max_per_img=500,
    nms=dict(
        nms_pre_max_size=1000,
        nms_post_max_size=83,
        nms_iou_threshold=0.2,
    ),
    score_threshold=0.1,
    pc_range=[0, -40],
    out_size_factor=get_downsample_factor(model),
    voxel_size=[0.2, 0.2]
)

# dataset settings
dataset_type = "KittiDataset"
nsweeps = 1
data_root = "/home/ubuntu/PycharmProjects/det3/CenterPoint/download/mydata01"
# data_root = "/home/ubuntu/PycharmProjects/det3/CenterPoint/download/mykitti-origin"

db_sampler = dict(
    type="GT-AUG",
    enable=False,
    db_info_path="/home/ubuntu/PycharmProjects/det3/CenterPoint/download/mydata01/dbinfos_train.pkl",
    sample_groups=[
        dict(Car=2),
        # dict(truck=3),
        # dict(construction_vehicle=7),
        # dict(bus=4),
        # dict(trailer=6),
        # dict(barrier=2),
        # dict(motorcycle=6),
        # dict(bicycle=6),
        # dict(pedestrian=2),
        # dict(traffic_cone=2),
    ],
    db_prep_steps=[
        dict(
            filter_by_min_num_points=dict(
                Car=5,
                # truck=5,
                # bus=5,
                # trailer=5,
                # construction_vehicle=5,
                # traffic_cone=5,
                # barrier=5,
                # motorcycle=5,
                # bicycle=5,
                # pedestrian=5,
            )
        ),
        dict(filter_by_difficulty=[-1],),
    ],
    global_random_rotation_range_per_object=[0, 0],
    rate=1.0,
)
train_preprocessor = dict(
    mode="train",
    shuffle_points=True,
    global_rot_noise=[-0.3925, 0.3925],
    global_scale_noise=[0.95, 1.05],
    #db_sampler=db_sampler,
    db_sampler=None,
    class_names=class_names,
)

val_preprocessor = dict(
    mode="val",
    shuffle_points=False,
)

voxel_generator = dict(
    # range=[-51.2, -51.2, -5.0, 51.2, 51.2, 3.0],
    # range=[0, -32, -10, 160, 32, 0],
    range=[0, -40, -10, 160, 40, 0],
    voxel_size=[0.2, 0.2, 10],
    max_points_in_voxel=20,
    #max_voxel_num=[30000, 60000],
    max_voxel_num=30000,
)

train_pipeline = [
    dict(type="LoadPointCloudFromFile", dataset=dataset_type),
    dict(type="LoadPointCloudAnnotations", with_bbox=True),
    dict(type="Preprocess", cfg=train_preprocessor),
    dict(type="Voxelization", cfg=voxel_generator),
    dict(type="AssignLabel", cfg=train_cfg["assigner"]),
    dict(type="Reformat"),
]
test_pipeline = [
    dict(type="LoadPointCloudFromFile", dataset=dataset_type),
    dict(type="LoadPointCloudAnnotations", with_bbox=True),
    dict(type="Preprocess", cfg=val_preprocessor),
    dict(type="Voxelization", cfg=voxel_generator),
    dict(type="AssignLabel", cfg=train_cfg["assigner"]),
    dict(type="Reformat"),
]

train_anno = "/home/ubuntu/PycharmProjects/det3/CenterPoint/download/mydata01/kitti_infos_train.pkl"
val_anno = "/home/ubuntu/PycharmProjects/det3/CenterPoint/download/mydata01/kitti_infos_val.pkl"

# train_anno = "/home/ubuntu/PycharmProjects/det3/CenterPoint/download/mykitti-origin/kitti_infos_train.pkl"
# val_anno = "/home/ubuntu/PycharmProjects/det3/CenterPoint/download/mykitti-origin/kitti_infos_val.pkl"

test_anno = None

data = dict(
    samples_per_gpu=2,
    workers_per_gpu=1,
    train=dict(
        type=dataset_type,
        root_path=data_root,
        info_path=train_anno,
        ann_file=train_anno,
        nsweeps=nsweeps,
        class_names=class_names,
        pipeline=train_pipeline,
    ),
    val=dict(
        type=dataset_type,
        root_path=data_root,
        info_path=val_anno,
        test_mode=True,
        ann_file=val_anno,
        nsweeps=nsweeps,
        class_names=class_names,
        pipeline=test_pipeline,
    ),
    test=dict(
        type=dataset_type,
        root_path=data_root,
        info_path=test_anno,
        ann_file=test_anno,
        nsweeps=nsweeps,
        class_names=class_names,
        pipeline=test_pipeline,
    ),
)


optimizer_config = dict(grad_clip=dict(max_norm=35, norm_type=2))
# optimizer
optimizer = dict(
    type="adam", amsgrad=0.0, wd=0.01, fixed_wd=True, moving_average=False,
)
lr_config = dict(
    type="one_cycle", lr_max=0.001, moms=[0.95, 0.85], div_factor=10.0, pct_start=0.4,
)

checkpoint_config = dict(interval=5)
# yapf:disable
log_config = dict(
    interval=5,
    hooks=[
        dict(type="TextLoggerHook"),
        # dict(type='TensorboardLoggerHook')
    ],
)
# yapf:enable
# runtime settings
total_epochs = 50
device_ids = range(8)
dist_params = dict(backend="nccl", init_method="env://")
log_level = "INFO"
work_dir = './work_dirs/{}/'.format(__file__[__file__.rfind('/') + 1:-3])
load_from = None
resume_from = None 
workflow = [('train', 1)]
