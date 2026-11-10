import os
import h5py
import numpy as np
from vgg_module import VGGNet

def get_img(path):
    # 获取文件夹下所有的 .jpg 文件
    return (os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg'))

if __name__ == '__main__':
    # 1. 设置你的图片数据集文件夹路径
    dataset_dir = './greatwall/'
    img_list = list(get_img(dataset_dir))
    
    print('--------开始提取特征--------')
    feats = []
    names = []
    model = VGGNet()
    
    for i, img_path in enumerate(img_list):
        # 提取特征
        norm_feat = model.ex_feat(img_path)
        # 获取文件名
        img_name = os.path.split(img_path)[1]
        feats.append(norm_feat)
        names.append(img_name)
        print(f'已提取 {i+1}/{len(img_list)} 张图特征: {img_name}')
    
    # 将列表转为numpy数组
    feats = np.array(feats)
    # 把字符串数组转为 bytes，方便保存到 h5 文件
    names = np.array(names, dtype='S')
    
    # 2. 保存到 HDF5 文件
    print('--------开始保存特征--------')
    with h5py.File('featCNN.h5', 'w') as h5f:
        h5f.create_dataset('dataset_1', data=feats)
        h5f.create_dataset('dataset_2', data=names)
    
    print('特征库构建完成！生成了 featCNN.h5 文件。')