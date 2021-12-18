# Testing CMDParser
from app.cli_tool import CMDParser, CommandType


def test_get_type_method_1() -> None:
    assert CMDParser.get_cmd_type('subscribe <Alice> to <Pewdiepie>') == CommandType.SUBSCRIBE
    assert CMDParser.get_cmd_type('subscribe <Jake> to <MrBeast>') == CommandType.SUBSCRIBE


def test_get_type_method_2() -> None:
    assert CMDParser.get_cmd_type('publish video on <MrBeast>') == CommandType.PUBLISH_VIDEO
    assert CMDParser.get_cmd_type('publish video on <Pewdiepie>') == CommandType.PUBLISH_VIDEO


def test_get_type_exception_1() -> None:
    try:
        CMDParser.get_cmd_type('')
        assert 1 == 2
    except ValueError:
        return
    except Exception as e:
        assert 1 == 2, f"Unexpected error occurred: {e}"


def test_get_type_exception_2() -> None:
    try:
        CMDParser.get_cmd_type('publish video on ')
        assert 1 == 2
    except ValueError:
        pass
    except Exception as e:
        assert 1 == 2, f"Unexpected error occurred: {e}"


def test_parse_publish_video_cmd() -> None:
    assert CMDParser.parse_publish_video_cmd('publish video on <MrBeast>') == "MrBeast"
    assert CMDParser.parse_publish_video_cmd('publish video on <Pewdiepie>') == "Pewdiepie"


def test_parse_publish_video_cmd_exception_1() -> None:
    try:
        CMDParser.parse_publish_video_cmd('publish video on <Pewdiepie')
        assert 1 == 2
    except ValueError:
        pass


def test_parse_publish_video_cmd_exception_2() -> None:
    try:
        CMDParser.parse_publish_video_cmd('publish video on Pewdiepie>')
        assert 1 == 2
    except ValueError:
        pass


def test_parse_publish_video_cmd_exception_3() -> None:
    try:
        CMDParser.parse_publish_video_cmd('published videos on <>')
        assert 1 == 2
    except ValueError:
        pass


def test_parse_subscribe_cmd() -> None:
    subscriber, channel = CMDParser.parse_subscribe_cmd('subscribe <Jake> to <MrBeast>')
    assert subscriber == 'Jake' and channel == 'MrBeast'

    subscriber, channel = CMDParser.parse_subscribe_cmd('subscribe <Alice> to <Pewdiepie>')
    assert subscriber == 'Alice' and channel == 'Pewdiepie'


def test_parse_subscribe_cmd_exception_1() -> None:
    try:
        CMDParser.parse_subscribe_cmd('subscribe <')
        assert 1 == 2
    except ValueError:
        pass


def test_parse_subscribe_cmd_exception_2() -> None:
    try:
        CMDParser.parse_subscribe_cmd('subscribe <> to <Pewdiepie>')
        assert 1 == 2
    except ValueError:
        pass


def test_parse_subscribe_cmd_exception_3() -> None:
    try:
        CMDParser.parse_subscribe_cmd('subscribe <Alice> to <>')
        assert 1 == 2
    except ValueError:
        pass
