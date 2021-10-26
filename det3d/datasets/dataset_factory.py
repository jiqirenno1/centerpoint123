from .nuscenes import NuScenesDataset
from .waymo import WaymoDataset
from .kitti import KittiDataset

dataset_factory = {
    "KITTI": KittiDataset,
    "NUSC": NuScenesDataset,
    "WAYMO": WaymoDataset
}


def get_dataset(dataset_name):
    return dataset_factory[dataset_name]
