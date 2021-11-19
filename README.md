# Center-based 3D Object Detection and Tracking

# how to train my own data

## 1. label my own data
- [
point_cloud_ros_annotation_tool ](https://github.com/Qjizhi/point_cloud_ros_annotation_tool)


## 2. train my own data
```
#create data
 python tools/create_data.py  kitti_data_prep --root_path=./download/mykitti-origin
 
 # if "ModuleNotFoundError: No module named 'det3d'"
 export PYTHONPATH="${PYTHONPATH}:/home/ubuntu/PycharmProjects/det3/CenterPoint"
 
 #train
 python tools/train.py /home/ubuntu/PycharmProjects/det3/CenterPoint/configs/mykitti/centerpoint_pp_02voxel_two_pfn.py 
```
## 3. pth2onnx2trt
```
# 1.
export_pointpillars_onnx.py
# 2.
simplify_model.py
# 3.
merge_pfe_rpn_model.py

```