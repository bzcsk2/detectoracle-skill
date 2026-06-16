[English](README.md) | [中文](README.zh.md)

# IssueOracle Skill

从 GitHub 已修复的 issue 中挖掘 bug 模式，再用具体证据审查本地代码。
v0.2 新增三命令流水线：**scan → mine → review**。

## 快速开始

```bash
# 安装
npx skills add bzcsk2/issueoracle-skill -g

# 扫描项目 → 获取画像 + 同类 OSS 推荐
/issueoracle scan .

# 审查当前仓库
/issueoracle review .

# 用 bug 经验文档审查
/issueoracle review . --experience ~/.issueoracle/bugplay/bug-experience.md

# 从 GitHub 仓库挖掘 bug 模式（逗号分隔）
/issueoracle mine fastapi/fastapi,encode/starlette

# 校验模式包
/issueoracle validate packs
```

## 流水线

```text
scan ./my-project                     → 项目画像 + 5 个推荐仓库
mine owner1/repo1,owner2/repo2,...    → ~/.issueoracle/bugplay/bug-experience.md
review ./my-project --experience ...  → 由挖掘经验驱动的审查结果
```

## 用法

### 扫描项目

```bash
/issueoracle scan . --emit markdown
/issueoracle scan src/ --emit json --max-repos 3
```

输出包括：语言/框架检测、风险面分析、项目类型分类（`web_api` / `cli` / `library` / `frontend`），以及按 star 数排序的 5 个同类开源项目。

### 审查本地代码

```bash
# 全量审查
/issueoracle review .
# Diff 审查（仅变更文件）
/issueoracle review . --changed --base main
# JSON 输出
/issueoracle review src/ --emit json
# 经验驱动审查
/issueoracle review . --experience ~/.issueoracle/bugplay/bug-experience.md
```

### 从 GitHub 挖掘 bug 模式

```bash
# 单个仓库
/issueoracle mine fastapi/fastapi
# 批量挖掘
/issueoracle mine fastapi/fastapi,encode/starlette,sqlalchemy/sqlalchemy --max-issues 30
```

挖掘结果保存到 `~/.issueoracle/bugplay/bug-experience.md`，按 bug 类型组织的叙事文档。每条包含：症状 → 根因 → 触发条件 → 坏代码信号 → 修复方式 → 证据链接。

### 校验模式包

```bash
/issueoracle validate packs
/issueoracle validate packs --emit json
```

### 诊断

```bash
/issueoracle diagnose
```

## 工作原理

1. **Scan**：对本地项目画像（语言、框架、依赖、风险面），分类项目类型，推断 GitHub 搜索关键词，推荐 5 个同类开源项目。
2. **Mine**：批量搜索 GitHub 已关闭的 bug issue，过滤真实 bug，链接到修复 PR，提取候选 bug 模式，聚合成叙事型 bug 经验 markdown 文档。
3. **Review**：加载种子模式 + 可选经验文档，索引本地代码，匹配信号，生成带证据的发现报告。

## 开发

```bash
uv sync
python3 -m pytest tests/ -q
python3 skills/issueoracle/scripts/issueoracle.py diagnose
python3 skills/issueoracle/evals/run_eval.py
```

## 要求

- Python 3.12+
- `GITHUB_TOKEN`（可选，用于更高 API 频率限制）

## 许可证

MIT
