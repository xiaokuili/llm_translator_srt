import os
from typing import List, Dict
from operator import itemgetter
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda


from dotenv import load_dotenv

load_dotenv()

OPENAIMODEL = "gpt-3.5-turbo-16k"


class translateResult(BaseModel):
    msgs: List[str]
    token_usage: Dict[str, int] = {}


class SRT(BaseModel):
    id: int
    start_end_time: str
    msg: str


def _translator_chain():
    """翻译
    Args
        msg: 带翻译句子
        context: 上下文, 可以为空
    """
    llm = ChatOpenAI(name=OPENAIMODEL)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful translator. Translate the user sentence to chinese.",
            ),
            ("human", "{msg}"),
            ("ai", "{context}"),
        ]
    )
    chain = (
        {
            "question": RunnableLambda(itemgetter("question")),
            "search": RunnableLambda(itemgetter("search")),
        }
        | prompt
        | llm
    )
    chain = prompt | llm
    return chain


def _translator(msgs: List[str]) -> translateResult:
    _msgs = []
    for i, msg in enumerate(msgs):
        context = ""
        if i == 0:
            context = msgs[1]
        elif i == len(msgs) - 1:
            context = msgs[i - 1]
        else:
            context = msgs[i - 1] + msgs[i + 1]
        chain = _translator_chain()
        result = chain.invoke({"msg": msg, "context": context})
        _msgs.append(result.content)

    return translateResult(msgs=_msgs)


def read_srt(file_path):
    """read srt file"""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    entries = content.strip().split("\n\n")
    srt_list = []
    for entry in entries:
        lines = entry.split("\n")
        srt_list.append(
            SRT(id=int(lines[0]), start_end_time=lines[1], msg=" ".join(lines[2:]))
        )
    return srt_list


def write_srt(file_path, srts: List[SRT]):
    """write srt file"""
    with open(file_path, "a", encoding="utf-8") as file:
        for srt in srts:
            file.write(f"{srt.id}\n{srt.start_end_time}\n{srt.msg}\n\n")


def translator():
    """将英文srt文件翻译成中文srt文件，文件位置请修改.env"""

    input_file = os.environ["INPUT_FILE"]
    output = os.environ["OUTPUT_FILE"]
    maxline = os.environ["MAXLINE"]

    srts = read_srt(input_file)

    for i in range(0, len(srts), maxline):
        chunk = srts[i : i + maxline]
        msgs = [srt.msg for srt in chunk]

        tr = _translator(msgs)

        new_rsts = []

        for i, msg in enumerate(tr.msgs):
            new_rsts.append(
                SRT(id=chunk[i].id, start_end_time=chunk[i].start_end_time, msg=msg),
            )
            write_srt(output, new_rsts)
