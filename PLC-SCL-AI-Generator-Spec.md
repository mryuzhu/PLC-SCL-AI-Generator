
# PLC SCL AI Generator
## 开发需求文档 v1.0

---

# 1 项目概述

## 1.1 项目目标
开发一个 **基于 Web 的 PLC SCL 自动生成系统**。

系统允许用户通过自然语言描述控制逻辑，然后利用大模型生成符合 Siemens TIA Portal 规范的 **SCL 代码**。

生成代码可以：

- 导出为 SCL 源文件
- 自动导入 TIA Portal V17+ 项目
- 通过工程规则进行校验

---

# 2 系统目标架构

Web Frontend  
↓  
REST API  
↓  
Backend Service

模块：
- Task Manager
- Prompt Engine
- LLM Adapter
- SCL Generator
- Code Validator
- TIA Integration

LLM Providers
- Coze API
- OpenAI Compatible API
- Local Model

TIA Portal Integration
- Source Import
- Openness API

---

# 3 首版功能范围

## 3.1 代码生成范围

首版支持：

- FC
- FB
- DB
- UDT

同时支持：

- OB 框架代码生成

但默认 **不自动修改现有 OB**。

OB 仅允许：

- 生成模板
- 生成插入代码片段

---

# 4 输入方式

首版输入方式：

自然语言描述

示例：

创建一个电机控制 FB

输入：
Start  
Stop  
Fault

逻辑：
Start 且无 Fault 时启动  
Stop 或 Fault 停止

系统生成：

- FB_MotorControl
- UDT_MotorState
- DB_Motor_Instance

---

# 5 生成模式

系统支持三种模式。

## 5.1 安全模式

特点：

- 强制命名规范
- 强制接口检查
- 禁止修改 OB
- 强制人工确认

适合生产环境。

## 5.2 平衡模式（默认）

特点：

- 常见逻辑自动生成
- 基本规则检查
- 简单逻辑允许直接生成

## 5.3 自由生成模式

特点：

- 尽量完整生成
- 允许跳过部分规则
- 导入前给出风险提示

---

# 6 Web 前端

推荐技术：

- React
- Next.js
- TypeScript
- Monaco Editor

页面模块：

## 项目管理
- 创建项目
- 查看项目
- 删除项目

## 生成任务
输入：
- 自然语言
- 生成模式
- 模板

输出：
- SCL代码
- 代码结构

## 代码审查
功能：
- 代码高亮
- Diff 对比
- 重新生成
- 附加条件生成

## 发布
支持：
- 导出 SCL
- 导入 TIA

---

# 7 后端架构

推荐语言：

Python

框架：

FastAPI

模块：

## Task Manager

POST /task/create  
GET /task/status  
GET /task/result

## Prompt Engine

输入：
- 用户需求
- 模板
- 模式

输出：
- Prompt

## LLM Adapter

统一接口：

generate_code(prompt)

实现：

- CozeProvider
- OpenAIProvider
- LocalModelProvider

## SCL Generator

负责：

- PLC对象结构生成
- 代码模板生成
- 变量接口生成

## Code Validator

检查：

- SCL语法
- 命名规范
- 变量冲突
- 块依赖
- 危险逻辑

返回：

- pass
- warning
- error

## TIA Integration

方式1：

导出：
- .scl
- .xml

方式2：

使用 TIA Portal Openness API：

- 创建块
- 导入SCL
- 编译项目

---

# 8 数据库结构

推荐：

PostgreSQL

## Project

- id
- name
- created_at

## Task

- id
- project_id
- prompt
- mode
- status
- result

## Code

- task_id
- scl_code
- validation_result

---

# 9 API设计

## 生成代码

POST /generate

参数：

- prompt
- mode
- model

返回：

- scl_code
- validation

## 校验代码

POST /validate

返回：

- errors
- warnings

## 导入TIA

POST /tia/import

参数：

- project_path
- scl_file

---

# 10 推荐目录结构

backend
- api
- core
  - prompt_engine
  - scl_generator
  - validator
  - tia_integration
- llm
  - coze
  - openai
  - local
- models

frontend
- pages
- components
- editor
- api

docs
- architecture.md

---

# 11 技术栈

前端：

- React
- Next.js
- TypeScript
- Monaco Editor

后端：

- Python
- FastAPI
- PostgreSQL
- Redis

AI：

- Coze API
- OpenAI Compatible API
- Local LLM

工业接口：

- TIA Portal Openness
- .NET API

---

# 12 版本路线

## v1

- SCL生成
- 代码校验
- Web界面
- 导出SCL

## v2

- TIA Openness 自动导入

## v3

- 读取现有PLC项目
- AI修改代码
- 自动工程生成

---

# 13 预计规模

前端：约 6000 行  
后端：约 8000 行  
核心引擎：约 6000 行  

总规模：约 20000 行代码

---

# 14 项目最终目标

构建一个 **AI PLC 工程自动生成平台**

实现：

自然语言 → PLC程序 → 自动导入 TIA Portal
