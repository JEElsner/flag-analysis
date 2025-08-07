from typing import Tuple, Callable, Optional

from os import PathLike

from torch import Tensor
from torch.utils.data import Dataset
from torchvision.io import decode_image
from torchvision.transforms.v2 import GaussianNoise

from downlad_data import get_flag_data

class FlagImagesDataset(Dataset):
    def __init__(self, data_dir: PathLike | str = '../data', transform: Optional[Callable[[Tensor], Tensor]] = None, target_transform: Optional[Callable[[str], str]] = None) -> None:
        self.flag_table = get_flag_data(data_dir) # type: ignore

        self.transform = transform
        self.target_transform = target_transform

    def __len__(self) -> int:
        return len(self.flag_table)
    
    def __getitem__(self, index) -> Tuple[Tensor, str]:
        row = self.flag_table.iloc[index]
        image = decode_image(row['path'])

        label = f"{row['Flag(s)']}-{row['State']}"

        if self.transform:
            image = self.transform(image)

        if self.target_transform:
            label = self.target_transform(label)

        return image, label
    

class NoisyFlags(Dataset):
    def __init__(self, data_dir: PathLike | str = '../data', n_noisy=10, transform: Optional[Callable[[Tensor], Tensor]] = None, target_transform: Optional[Callable[[Tensor], Tensor]] = None) -> None:
        self.flag_images = FlagImagesDataset(data_dir)
        self.n_noisy = n_noisy

        self.noise_transform = GaussianNoise()

        self.transform = transform
        self.target_transform = target_transform

    def __len__(self) -> int:
        return self.n_noisy * len(self.flag_images)
    
    def __getitem__(self, index) -> Tuple[Tensor, Tensor]:
        original_img, _ = self.flag_images[index // self.n_noisy]
        noisy_img = self.noise_transform(original_img)

        if self.transform:
            noisy_img = self.transform(noisy_img)

        if self.target_transform:
            original_img = self.target_transform(original_img)

        return noisy_img, original_img
