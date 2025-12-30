# Anthropic Agent Skills Example (with ChatOpenAI)

这是一个展示如何使用 Anthropic 发布的 **Agent Skills** 标准，并结合 `ChatOpenAI` (OpenAI LLM) 驱动智能体的示例项目。

## 什么是 Agent Skills？

Agent Skills 是一种模块化的能力扩展方式，采用 **“渐进式披露 (Progressive Disclosure)”** 原则：
- **启动时**：智能体只知道技能的名字和简短描述。
- **执行时**：当任务匹配到某个技能时，智能体通过工具自主读取该技能目录下的详细指令（如 `instructions.md`）或数据文件。

## 目录结构

```text
opensource/example-skills/
├── calculator/                # 计算机技能
│   ├── SKILL.md               # 技能定义
│   └── conversion_rates.json  # 技能专用数据
├── text-processor/            # 文本处理技能
│   ├── SKILL.md               # 技能定义
│   └── instructions.md        # 详细操作指南
├── main.py                    # 驱动程序 (LangChain + OpenAI)
├── pyproject.toml             # uv 项目配置
└── uv.lock                    # 依赖锁定文件
```

## 快速开始

本项目使用 [uv](https://github.com/astral-sh/uv) 进行依赖管理。

### 1. 环境准备

确保已安装 `uv`。如果未安装，可以使用 pip 安装：
```bash
pip install uv
```

### 2. 安装依赖

在项目根目录下运行：
```bash
uv sync
```

### 3. 配置 API Key

设置您的 OpenAI API Key：
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 4. 运行示例

执行主程序：
```bash
uv run python main.py
```

## 如何工作？

1. **技能加载**：`main.py` 会扫描目录并提取 `SKILL.md` 中的元数据。
2. **动态提示词**：技能描述被注入到系统提示词中，让 LLM 知道有哪些可用技能。
3. **自主探索**：智能体配备了 `list_skill_contents` 和 `read_skill_file` 工具。当您询问“分析这段文字的情感”时，它会发现 `text-processor` 技能，然后读取其内部的 `instructions.md` 来获取具体的处理逻辑。

## 扩展建议

您可以创建自己的文件夹并添加 `SKILL.md` 来扩展智能体的能力，无需修改 `main.py` 的核心逻辑。
