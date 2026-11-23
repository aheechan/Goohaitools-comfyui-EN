import os
import importlib.util
import logging
import sys
from pathlib import Path

# 获取当前包目录的路径
current_dir = Path(__file__).parent
nodes_dir = current_dir / "nodes"

# 设置WEB目录路径 - 这是关键配置
WEB_DIRECTORY = "./web"

# 初始化全局映射字典
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 遍历nodes目录中的所有Python文件
for file_path in nodes_dir.glob("*.py"):
    # 跳过__init__.py文件
    if file_path.name == "__init__.py":
        continue
        
    # 提取模块名（不含.py后缀）
    module_name = file_path.stem
    
    # 使用importlib动态加载模块
    spec = importlib.util.spec_from_file_location(f"goohaitools.nodes.{module_name}", file_path)
    module = importlib.util.module_from_spec(spec)
    
    try:
        # 执行模块代码
        spec.loader.exec_module(module)
        
        # 检查并合并NODE_CLASS_MAPPINGS
        if hasattr(module, 'NODE_CLASS_MAPPINGS'):
            NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
            
        # 检查并合并NODE_DISPLAY_NAME_MAPPINGS
        if hasattr(module, 'NODE_DISPLAY_NAME_MAPPINGS'):
            NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
            
    except Exception as e:
        print(f"Error loading node module {module_name}: {str(e)}")
        continue

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

# English dropdown values: show English in the UI, map back to the original
# value right before the node function runs.
try:
    _i18n_spec = importlib.util.spec_from_file_location(
        "goohaitools_i18n_options", current_dir / "i18n_options.py"
    )
    _i18n_module = importlib.util.module_from_spec(_i18n_spec)
    _i18n_spec.loader.exec_module(_i18n_module)
    _i18n_module.apply_english_options(NODE_CLASS_MAPPINGS)
except Exception as _i18n_error:  # pragma: no cover
    logging.warning("[GoohaiTools] English option values disabled: %s", _i18n_error)

# 打印加载信息
logging.info(
    '\033[1m[GoohaiTools] %s nodes loaded | ColorWidget enabled\033[0m',
    len(NODE_CLASS_MAPPINGS),
    extra={"color": "cyan"},
)
