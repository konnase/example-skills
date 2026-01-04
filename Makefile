.PHONY: fmt lint test run help

# 默认目标
help:
	@echo "Available commands:"
	@echo "  make fmt   - Format code using ruff"
	@echo "  make lint  - Check code style and quality using ruff"
	@echo "  make test  - Run tests using pytest"
	@echo "  make run   - Execute the main application"

# 格式化代码
fmt:
	uv run ruff format .

# 代码检查
lint:
	uv run ruff check .

# 运行测试
test:
	uv run pytest

# 运行主程序
run:
	uv run src/example_skills/main.py
