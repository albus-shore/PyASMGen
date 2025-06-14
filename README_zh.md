<p align="center">
<img width="100" src="https://raw.githubusercontent.com/albus-shore/PyASMGen/main/assets/logo.png" alt="PyASMGen Logo">
</p>

---

# PyASMGen

> 用 Python 写 8051 汇编代码。  
> 写汇编不如写 SDK 😎

---

## 这是什么？

**PyASMGen** 是一个使用 Python 编写的 8051 汇编代码生成器。

它是专门为那些：

- 不想再写满屏 `MOV A, #0FFH`
- 总是写错 `SJMP` 跳转地址
- 明明会写逻辑但就是讨厌“语法细节”的

电子信息类专业学生准备的。

你写的是 Python，输出的是纯正的汇编。  
既能跑、又能交作业，老师也挑不出毛病 👨‍🏫

---

## 为什么做这个？

因为：

- Python 写起来就是比汇编舒服
- 汇编指令错一个字母就报错，太烦
- 写项目也好，交作业也罢，生成代码更安心
- 这玩意儿写着写着，还挺好玩 🤪

---

## 特性亮点

- ✅ 全部指令封装成 Python 方法，语法清晰
- 🧠 内置参数检查，写错直接报错提醒
- 🧱 支持声明式组合写法（计划中）
- 🔌 可以和 LLM 项目集成（比如集成你自己的 [Llyra](https://github.com/albus-shore/Llyra)）
- 🐍 纯 Python 实现，跨平台无压力

---

## 计划中功能

- [X] 自动纠错 + 汇编语义检查
- [X] 中断与串口通信模块封装
- [ ] 支持宏定义、条件生成等高级语法
- [ ] 汇编代码自动注释
- [ ] 和 Keil/Proteus 集成的 HEX 文件生成功能

---

## 安装方式

```bash
pip install pyasmgen
```

---

## 口号

> **“写汇编不如写 SDK 😎”**

---

## 授权协议

MIT License — 学生帮助学生，当然是免费开源 🧑‍🤝‍🧑

---