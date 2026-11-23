from comfy.sd import CLIP
from comfy.samplers import KSAMPLER
import comfy.utils

class GHFloatSliderNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "数值": ("FLOAT", {  
                    "default": 1.00, 
                    "min": 0.00, 
                    "max": 1.00, 
                    "step": 0.05,
                    "display": "slider"
                }),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("浮点",)
    CATEGORY = "Goohai Tools"
    FUNCTION = "get_value"

    def get_value(self, 数值):  
        # 保留两位小数
        value = round(数值, 2)
        return (value,)

class GHFloatSliderNode0To2:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "数值": ("FLOAT", {  
                    "default": 1.00, 
                    "min": 0.00, 
                    "max": 2.00, 
                    "step": 0.05,
                    "display": "slider"
                }),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("浮点",)
    CATEGORY = "Goohai Tools"
    FUNCTION = "get_value"

    def get_value(self, 数值):  
        # 保留两位小数
        value = round(数值, 2)
        return (value,)

# 节点注册映射
NODE_CLASS_MAPPINGS = {
    "孤海-浮点滑条": GHFloatSliderNode,
    "孤海-浮点滑条 0-2": GHFloatSliderNode0To2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "孤海-浮点滑条": "Goohai Float Slider",
    "孤海-浮点滑条 0-2": "Goohai Float Slider 0-2"
}