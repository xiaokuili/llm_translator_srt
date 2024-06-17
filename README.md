# llm_translator_srt
通过大模型将英文字幕翻译成中文字幕



# Start by python 
1. install 
```
cd llm_translator_srt/translator
poetry install 
```
2. create .env 
```

# OPENAI
OPENAI_API_KEY=
OPENAI_API_BASE=

# SRT FILE
INPUT_PATH=<输入srt文件位置>
OUTPU_TPATH=<输入翻译后srt文件位置>
MAXLINE=<每次处理多少行>
```
3. run 
```
poetry run python /translator/translator/example.py
```
# Start by colab

[![在Colab中打开](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1ApDWPjf37OiioTKWreYxemYAC7APHs7D?usp=drive_link)
