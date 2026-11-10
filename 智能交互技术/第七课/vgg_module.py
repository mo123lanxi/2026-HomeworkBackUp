import numpy as np
import numpy.linalg as LA
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input

class VGGNet:
    def __init__(self):
        # 设置输入图片的尺寸为 224x224，3通道
        self.input_shape = (224, 224, 3)
        # 使用预训练的 ImageNet 权重
        self.weight = 'imagenet'
        # 池化方式
        self.pooling = 'max'
        # 加载模型，include_top=False 表示去掉最后的全连接层，只用作特征提取
        self.model = VGG16(weights=self.weight, 
                           input_shape=self.input_shape, 
                           pooling=self.pooling, 
                           include_top=False)

    def ex_feat(self, img_path):
        # 加载图片并调整大小
        img = image.load_img(img_path, target_size=(224, 224))
        # 转换为数组
        img = image.img_to_array(img)
        # 增加一个维度，变成 (1, 224, 224, 3) 供模型预测
        img = np.expand_dims(img, axis=0)
        # 预处理（减去均值等）
        img = preprocess_input(img)
        # 提取特征
        feat = self.model.predict(img)
        # 归一化特征向量 (L2范数)
        norm_feat = feat[0] / LA.norm(feat[0])
        return norm_feat
