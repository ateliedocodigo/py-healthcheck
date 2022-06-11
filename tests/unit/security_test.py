from datetime import datetime
from unittest import TestCase

from ddt import data, ddt, unpack

from healthcheck.security import safe_dict


def make_test_dict(test_key, test_value, deep=1):
    if deep > 1:
        return dict(dummy=make_test_dict(test_key, test_value, deep - 1))
    return {test_key: test_value}


class MakeTestDictTest(TestCase):

    def test_should_return_input_value_if_deep_is_lte_0(self):
        self.assertEqual({"a": "asd"}, make_test_dict("a", "asd", 0))

    def test_should_make_test_dict_first_level(self):
        self.assertEqual({"a": "asd"}, make_test_dict("a", "asd"))
        self.assertEqual({"a": "***"}, make_test_dict("a", "***"))

    def test_should_make_test_dict_second_level(self):
        self.assertEqual({"dummy": {"a": "asd"}}, make_test_dict("a", "asd", 2))
        self.assertEqual({"dummy": {"a": "***"}}, make_test_dict("a", "***", 2))

    def test_should_make_test_dict_third_level(self):
        self.assertEqual({"dummy": {"dummy": {"a": "asd"}}}, make_test_dict("a", "asd", 3))
        self.assertEqual({"dummy": {"dummy": {"a": "***"}}}, make_test_dict("a", "***", 3))


@ddt
class SafeDictTest(TestCase):

    def test_should_return_input_value_if_max_deep_is_lte_0(self):
        self.assertEqual({"a": "asd"}, safe_dict({"a": "asd"}, max_deep=0))

    @unpack
    @data(
        (1, "a", "asdf"),
        (1, "a", 42),
        (1, "a", 3.14),
        (1, "a", datetime.now()),
    )
    def test_should_dump_dictionary_without_blacklisted_keys(self, deep, key_to_test, value):
        input_dict = make_test_dict(key_to_test, value, deep)
        to_dict = safe_dict(input_dict)

        self.assertEqual(input_dict, to_dict)

    @unpack
    @data(
        (1, "key", "asdf"),
        (1, "Key", "asdf"),
        (1, "somekey", "asdf"),
        (1, "someKey", "asdf"),
        (1, "key_value", "asdf"),
        (1, "Key_value", "asdf"),

        (1, "key", 42),
        (1, "Key", 42),
        (1, "somekey", 42),
        (1, "someKey", 42),
        (1, "key_value", 42),
        (1, "Key_value", 42),

        (1, "key", 3.14),
        (1, "Key", 3.14),
        (1, "somekey", 3.14),
        (1, "someKey", 3.14),
        (1, "key_value", 3.14),
        (1, "Key_value", 3.14),

        (1, "key", datetime.now()),
        (1, "Key", datetime.now()),
        (1, "somekey", datetime.now()),
        (1, "someKey", datetime.now()),
        (1, "key_value", datetime.now()),
        (1, "Key_value", datetime.now()),

        (2, "key", "asdf"),
        (2, "Key", "asdf"),
        (2, "somekey", "asdf"),
        (2, "someKey", "asdf"),
        (2, "key_value", "asdf"),
        (2, "Key_value", "asdf"),

        (3, "key", "asdf"),
        (3, "Key", "asdf"),
        (3, "somekey", "asdf"),
        (3, "someKey", "asdf"),
        (3, "key_value", "asdf"),
        (3, "Key_value", "asdf"),

        (4, "key", "asdf"),
        (4, "Key", "asdf"),
        (4, "somekey", "asdf"),
        (4, "someKey", "asdf"),
        (4, "key_value", "asdf"),
        (4, "Key_value", "asdf"),

        (5, "key", "asdf"),
        (5, "Key", "asdf"),
        (5, "somekey", "asdf"),
        (5, "someKey", "asdf"),
        (5, "key_value", "asdf"),
        (5, "Key_value", "asdf"),
    )
    def test_should_dump_dictionary_with_blacklisted_key_deep(self, deep, key_to_test, value):
        input_dict = make_test_dict(key_to_test, value, deep)
        to_dict = safe_dict(input_dict)

        self.assertEqual(make_test_dict(key_to_test, "********", deep), to_dict)
