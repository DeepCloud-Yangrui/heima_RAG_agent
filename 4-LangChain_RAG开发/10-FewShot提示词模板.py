from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.llms.tongyi import Tongyi

# 示例模板，规定了每个示例在发给模型时的文本格式为：单词:{word}, 反义词:{antonym}
example_template = PromptTemplate.from_template("单词{word}，反义词{antonym}")

# 示例的动态数据注入,要求是list内部套字典
examples_data=[
    {"word":"大", "antonym":"小"},
    {"word":"上", "antonym":"下"},
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=example_template,
    examples=examples_data,
    prefix="告诉我单词的反义词，我提供如下的示例：",
    suffix="基于前面的示例告诉我，{input_word}的反义词是?",
    input_variables=['input_word']
)
prompt_text = few_shot_template.invoke(input={"input_word": "左"}).to_string()
print(prompt_text)

model= Tongyi(model="qwen-max")
res = model.invoke(input=prompt_text)
print(res)