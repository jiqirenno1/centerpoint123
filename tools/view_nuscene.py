from nuscenes.nuscenes import NuScenes

nusc = NuScenes(version='v1.0-mini', dataroot='/home/ubuntu/PycharmProjects/det3/CenterPoint/download/v1.0-mini', verbose=False)



my_sample = nusc.sample[10]
print(len(nusc.sample))


nusc.render_sample_data(my_sample['data']['LIDAR_TOP'], nsweeps=5, underlay_map=False)

if __name__ == '__main__':
    from pathlib import Path
    pp = Path('/home/ubuntu/PycharmProjects/det3/CenterPoint/download/v1.0-mini')
    print()
    print('/home/ubuntu/PycharmProjects/det3/CenterPoint/download/v1.0-mini')
    out = Path("./download//v1.0-mini").resolve().parent
    print(out)

