import cv2
import numpy as np

from service.constants import Color, Size


class Picture:

    def __init__(self, content, color=Color.WHITE, size=Size.P720):
        """
        :param color: 填充reshape后图片至目标尺寸的颜色
        """
        self.picture_stream = content
        self.color = color
        self.size = size
        self.picture = self.convert()
        self.picture = self.reshape()
        self.failures = []

    def __call__(self, *args, **kwargs):
        return self.picture

    @property
    def failure(self):
        if not self.failures:
            return None
        return "\n".join(self.failures)

    def convert(self):
        """
        convert bytes type picture_stream to numpy.ndarray type cv2.image object
        """
        return cv2.imdecode(
            np.frombuffer(self.picture_stream, np.uint8),
            cv2.IMREAD_COLOR
        )

    def reshape(self):
        """
        shape irregular size picture to target size picture
        example: 500 x 500 to 720 x 1280
        Variables:
            origin_height: 目标尺寸的高度
            target_width: 目标尺寸的宽度
            picture_height: 当前图片的高度
            picture_width: 当前图片的宽度
            target_height: 原始比例缩放后目标图片的高度
            short: 缩放后需填充至目标高度的缺口高度
        """
        if not hasattr(self.picture, "shape"):
            self.failures.append("picture format error")
            return None

        origin_height = self.size[1]
        target_width = self.size[0]
        picture_height = self.picture.shape[0]
        picture_width = self.picture.shape[1]
        target_height = int(picture_height * target_width / picture_width)

        picture = cv2.resize(
            self.picture, (target_width, target_height),
            interpolation=cv2.INTER_LINEAR
        )

        short = (origin_height - target_height) // 2 if (origin_height - target_height) % 2 == 0 \
            else (origin_height - target_height + 1) // 2

        if short <= 0:
            self.failures.append("picture doesn't fit the size of target video")
            return None
            # raise ValueError("picture doesn't fit the size of target video")

        picture = cv2.copyMakeBorder(
            picture,
            short, origin_height - target_height - short, 0, 0,
            cv2.BORDER_CONSTANT,
            value=self.color
        )

        return picture
