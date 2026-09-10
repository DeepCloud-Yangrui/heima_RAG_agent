from openai import OpenAI
from pyexpat.errors import messages

# 1. 获取client对象，OpenAI类对象
client = OpenAI(
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    base_url="http://localhost:11434/v1"
)

# 示例数据
examples_data = {
    '新闻报道': '今日，股市经历了一轮震荡，受到宏观经济数据和全球贸易紧张局势的影响。投资者密切关注美联储可能的政策调整，以适应市场的不确定性。',
    '财务报告': '本公司年度财务报告显示，去年公司实现了稳步增长的盈利，同时资产负债表呈现强劲的状况。经济环境的稳定和管理层的有效战略执行为公司的健康发展奠定了基础。',
    '公司公告': '本公司高兴地宣布成功完成最新一轮并购交易，收购了一家在人工智能领域领先的公司。这一战略举措将有助于扩大我们的业务领域，提高市场竞争力',
    '分析师报告': '最新的行业分析报告指出，科技公司的创新将成为未来增长的主要推动力。云计算、人工智能和数字化转型被认为是引领行业发展的关键因素，投资者应关注这些趋势'
}
# 分类列表
examples_types = ['新闻报道', '财务报道', '公司公告', '分析师报告']

# 提问数据
questions = [
    "今日，央行发布公告宣布降低利率，以刺激经济增长。这一降息举措将影响贷款利率，并在未来几个季度内对金融市场产生影响。",
    "ABC公司今日发布公告称，已成功完成对XYZ公司股权的收购交易。本次交易是ABC公司在扩大业务范围、加强市场竞争力方面的重要举措。据悉，此次收购将进一步巩固ABC公司在行业中的地位，并为未来业务发展提供更广阔的发展空间。详情请见公司官方网站公告栏",
    "公司资产负债表显示，公司偿债能力强劲，现金流充足，为未来投资和扩张提供了坚实的财务基础。",
    "最新的分析报告指出，可再生能源行业预计将在未来几年经历持续增长，投资者应该关注这一领域的投资机会",
    "小明喜欢小新哟"
]

"""
[
    {"role": "system",      "content": "你是金融专家，将文本分类为['新闻报道', '财务报道', '公司公告', '分析师报告']，不清楚的分类为'不清楚类别' 下面有示例："},

    {"role": "user",        "content": "今日，央行发布公告宣布降............."},
    {"role": "assistant",   "content": "新闻报道"},
    {"role": "user",        "content": "ABC公司今日发布公告称，已成功完成对XYZ公司股................."},
    {"role": "assistant",   "content": "财务报告},
    {"role": "user",        "content": "公司资产负债表显示，公司偿债能力强劲，现金流充足..................."},
    {"role": "assistant",   "content": "公司公告"},
    {"role": "user",        "content": "最新的分析报告指出，可再生能源............."},
    {"role": "assistant",   "content": "分析师报告"},

    {"role": "user",        "content": "要提问的问题"}
]
"""


# 2、组装messages

# messages本质是一个列表，大语言模型（如 Qwen、GPT 等）本质上是没有记忆的，
# 必须通过 messages 列表把“系统设定”、“参考示例”以及“用户最新问题”一次性全部发给它。
messages=[

    # 2.1 这里先给模型设定一个系统角色
    {"role": "system","content": "你是金融专家，将文本分类为['新闻报道', '财务报道', '公司公告', '分析师报告']，不清楚的分类为'不清楚类别' 下面有示例："},
]

    # 2.2完成角色设定之后，才在messages中添加示例
    # 这里可以用for循环把 字典examples_data 中的信息添加到messages中，
    # 但在这里 由于examples_data 是一个 Python 字典（Dictionary），采用 .items() 是为了同时一次性取出“键（Key）”和“值（Value）”。
for key,value in examples_data.items():
    messages.append({"role":"user","content":value})
    messages.append({"role":"assistant","content":key})
    # 已经把示例信息都添加到messages中了

    # 2.3 对于questions中的提问数据，挨个向模型进行提问
for q in questions:
    response = client.chat.completions.create(
        # model="qwen3.8-max",
        model="qwen",   # 使用本地模型需要检查ollama是否已经启动了，如果没启动需要先把ollama模型启动起来才可以运行本地模型
        messages=messages + [{"role": "user", "content": f"按照示例，来回答这段文本的分类类别{q}"}]
    )
    print(response.choices[0].message.content)

