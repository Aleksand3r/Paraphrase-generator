from lyrics import Lyrics, setup_config

CONFIG = setup_config("config.json")
TEXT1 = CONFIG["test_text"]["text1_medium"]
SONG1 = CONFIG["test_text"]["song1"]


def test_Lyrics__str__():
    example_poem = Lyrics(TEXT1)
    assert str(example_poem) == "\n".join(TEXT1[0]["lines"])


def test_Lyrics_author():
    example_poem = Lyrics(TEXT1)
    assert example_poem.author() == "William Cowper"


def test_Lyrics_title():
    example_poem = Lyrics(TEXT1)
    assert example_poem.title() == "Prayer for Children"


def test_Lyrics_lines():
    example_poem = Lyrics(TEXT1)
    assert example_poem.lines() == TEXT1[0]["lines"]
