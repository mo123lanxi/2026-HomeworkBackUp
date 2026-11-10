import numpy as np
import h5py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from vgg_module import VGGNet

if __name__ == '__main__':
    # 1. 读取特征库
    print('正在加载特征库...')
    h5f = h5py.File('featCNN.h5', 'r')
    feats = h5f['dataset_1'][:]
    # 将读取到的 bytes 转换回字符串
    names = [name.decode('utf-8') for name in h5f['dataset_2'][:]]
    h5f.close()

    # 2. 读取要搜索的源图
    queryDir = './query.jpg'  # 确保这个位置有一张你要搜的图片
    queryImg = mpimg.imread(queryDir)

    # 3. 提取待搜图的特征
    print('正在提取查询图片的特征...')
    model = VGGNet()
    queryVec = model.ex_feat(queryDir)

    # 4. 计算相似度（点积）
    scores = np.dot(queryVec, feats.T)
    # 对分数进行降序排列
    rank_ID = np.argsort(scores)[::-1]
    
    # 取前3个最高分的索引
    maxres = 3
    top_indices = rank_ID[0:maxres]
    imlist = [names[index] for index in top_indices]
    
    print(f'最相似的 {maxres} 张图是: {imlist}')

    # 5. 显示搜索结果
    plt.figure(figsize=(16, 5))
    
    # 显示原图
    plt.subplot(1, 4, 1)
    plt.title('Query Image')
    plt.imshow(queryImg)
    plt.axis('off')

    # 循环显示前3个结果
    dataset_dir = './greatwall/' # 你的数据集文件夹
    for i, im in enumerate(imlist):
        image_path = dataset_dir + im
        result_img = mpimg.imread(image_path)
        
        plt.subplot(1, 4, i + 2)
        plt.title(f'Search Result {i+1}')
        plt.imshow(result_img)
        plt.axis('off')

    plt.show()