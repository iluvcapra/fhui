import pytest

from fhui.charsets import SmallDisplayCharSet, LargeDisplayCharSet

class TestSmallDisplayCharSet:
    def test_encode(self):
        assert SmallDisplayCharSet.encode("ü") == [0x1a]
        assert SmallDisplayCharSet.encode("a") == [0x61]

    def test_encode_many(self):
        assert SmallDisplayCharSet.encode("a12→à") == [0x61,0x31,0x32,0x02,0x06]

    def test_encode_invalid(self):
        assert SmallDisplayCharSet.encode("😀", replacement_code=0x20) == [0x20]
        assert SmallDisplayCharSet.encode("˧", replacement_code=None) == [None]

class TestLargeDisplayCharSet:
    def test_encode(self):
        assert LargeDisplayCharSet.encode("a") == [0x61]
        assert LargeDisplayCharSet.encode("♪") == [0x19]

    def test_decode(self):
        assert LargeDisplayCharSet.decode([0x1d, 0x53,0x40, 0x77]) == "⏵S@w"

