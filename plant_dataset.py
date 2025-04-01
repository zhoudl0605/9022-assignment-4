import os
import numpy as np
from collections import defaultdict
from PIL import Image
from torch.utils.data import Dataset


class PlantDataset(Dataset):
    def __init__(self, root_dir, transform=None, mode='train'):
        self.root_dir = os.path.join(root_dir, mode)
        self.transform = transform
        self.plant_to_status = defaultdict(list)
        self.status_to_plant = {}
        self.samples = []

        # 验证并构建层级关系
        self._validate_structure()

        # 获取类别信息
        self.plant_classes = sorted(self.plant_to_status.keys())
        self.status_classes = sorted(self.status_to_plant.keys())
        self.num_plant_classes = len(self.plant_classes)
        self.num_status_classes = len(self.status_classes)

        # 创建映射字典
        self.plant_to_idx = {plant: idx for idx,
                             plant in enumerate(self.plant_classes)}
        self.status_to_idx = {status: idx for idx,
                              status in enumerate(self.status_classes)}

        self._build_status_matrix()

    def _build_status_matrix(self):
        """构建植物-状态的层级关系"""
        self.status_matrix = np.zeros(
            (len(self.plant_classes), len(self.status_classes)), dtype=int)
        for plant, statuses in self.plant_to_status.items():
            plant_idx = self.plant_to_idx[plant]
            for status in statuses:
                status_idx = self.status_to_idx[status]
                self.status_matrix[plant_idx][status_idx] = 1

    def _validate_structure(self):
        """验证文件夹结构并建立植物-状态映射关系"""
        for plant in os.listdir(self.root_dir):
            plant_path = os.path.join(self.root_dir, plant)
            if not os.path.isdir(plant_path):
                continue

            for status in os.listdir(plant_path):
                status_path = os.path.join(plant_path, status)
                if not os.path.isdir(status_path):
                    continue

                # 验证状态是否属于该植物的有效状态
                if plant in self.plant_to_status and status in self.plant_to_status[plant]:
                    pass  # 已经存在的关系
                else:
                    self.plant_to_status[plant].append(status)
                    self.status_to_plant[status] = plant

                # 添加样本
                for img_name in os.listdir(status_path):
                    if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        img_path = os.path.join(status_path, img_name)
                        self.samples.append((img_path, plant, status))

    def is_valid_status(self, plant, status):
        return plant in status

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, plant, status = self.samples[idx]
        image = Image.open(img_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        # 返回图像、植物类别索引、状态类别索引
        return image, self.plant_to_idx[plant], self.status_to_idx[status]

    def verify_status(self, plant, status):
        """验证植物和状态的关系"""
        if plant in self.plant_to_status:
            return status in self.plant_to_status[plant]
        return False
