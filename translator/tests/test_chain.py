import os
from translator.chain import _translator_chain, _translator
from translator.chain import read_srt, write_srt
from translator.chain import SRT
from translator.chain import translator

msgs = [
    "cheat that he sent me",
    "and it's got a list of a ton of things",
    "can I just read off and ask questions",
]


def test__translator_chain():
    msg = msgs[0]
    chain = _translator_chain()
    result = chain.invoke({"msg": msg, "context": ""})
    assert result.content != ""
    assert result.usage_metadata is not None


def test_write_read_srt_file():
    file_path = "/workspaces/llm_translator_srt/translator/srt/test.srt"
    srts = [
        SRT(id=1, start_end_time="s0e0", msg="this is test 1"),
        SRT(id=2, start_end_time="s1e1", msg="this is test 2"),
        SRT(id=3, start_end_time="s2e2", msg="this is test 3"),
    ]
    write_srt(file_path, srts)
    _srts = read_srt(file_path)
    assert srts[0].msg == _srts[0].msg
    assert srts[1].msg == _srts[1].msg
    assert srts[2].msg == _srts[2].msg


def test_write_read_srt_file2():
    file_path = "/workspaces/llm_translator_srt/translator/srt/example.srt"
    result = read_srt(file_path)
    assert result[-1].msg == "like what's the conversion of monopoly money to USD"


def test_translator():
    translator()
    from dotenv import load_dotenv

    load_dotenv()
    output_file = os.environ["OUTPUT_PATH"]
    srts = read_srt(output_file)
    assert len(srts) is not None
