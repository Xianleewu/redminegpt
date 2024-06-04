import logging

# 创建一个 Formatter 对象，指定日志的格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s+%(lineno)d: %(message)s')

# 创建一个 Handler 对象，指定日志输出到控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 创建一个 Logger 对象
logger = logging.getLogger('redmine_gpt')
logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

# 将 Handler 对象添加到 Logger 对象中
logger.addHandler(console_handler)
