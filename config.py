import os
import yaml

# 尝试从环境变量中获取配置值
DATABASE_BASENAME = os.environ.get("DATABASE_BASENAME")
DATABASE_ADDRESS = os.environ.get("DATABASE_ADDRESS")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

# 如果环境变量不存在，则从 YAML 文件中获取配置值
if not all([DATABASE_BASENAME, DATABASE_ADDRESS, DATABASE_USER, DATABASE_PASSWORD]):
    with open('config.yml', 'r') as f:
        config_yaml = yaml.safe_load(f)['database']

    DATABASE_BASENAME = DATABASE_BASENAME or config_yaml['database']
    DATABASE_ADDRESS = DATABASE_ADDRESS or config_yaml['host']
    DATABASE_USER = DATABASE_USER or config_yaml['user']
    DATABASE_PASSWORD = DATABASE_PASSWORD or config_yaml['password']