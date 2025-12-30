import os
from main import load_agent_skills


def test_load_agent_skills():
    # 验证函数是否存在且可调用
    assert callable(load_agent_skills)


def test_skill_structure():
    # 验证 text-processor 技能是否存在
    assert os.path.exists("text-processor/SKILL.md")
    assert os.path.exists("calculator/SKILL.md")
