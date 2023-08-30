"""Test module for pyfileflow rule classes.

This module contains unit tests for the various rule classes in the pyfileflow library.
"""

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from typeguard_ignore import suppress_type_checks

from pyfileflow.ppath import PPath
from pyfileflow.rule import CopyByValueRule, CopyRule, DeleteRule, MoveRule, Rule


# Rule class
def test_rule_context_manager() -> None:
    """Test rule context manager behavior.

    This test verifies the behavior of using a Rule instance within a context manager.
    It checks if the Rule instance can be used as a context manager without errors.
    """
    with Rule() as rule:
        assert rule


@suppress_type_checks
def test_next_not_rule() -> None:
    """Test instancing a rule with a next value not an instance of Rule."""
    with pytest.raises(TypeError):
        Rule(next=1)  # type: ignore[arg-type]


def test_check_path() -> None:
    """Test check_path method.

    This test checks the behavior of the check_path method of the Rule class.
    It tests both True and False scenarios.
    """
    with PPath("") as path:
        assert Rule(condition=[lambda x: True, lambda x: True]).check_path(path)
        assert not Rule(condition=[lambda x: True, lambda x: False]).check_path(path)


def test_next_calling_condition_true(fs: FakeFilesystem) -> None:
    """Test calling next rule when the condition is true.

    This test verifies that the 'next' rule is called when the condition of the
    current rule is true.
    """
    next = DeleteRule()
    rule = CopyRule(next, destination="copy.txt")

    path = PPath("test.txt")
    path.touch()

    rule.process_file(path)

    assert PPath("copy.txt").exists()
    assert not PPath("test.txt").exists()


def test_next_calling_condition_false(fs: FakeFilesystem) -> None:
    """Test calling next rule when the condition is false.

    This test verifies that the 'next' rule is called when the condition of
    the current rule is false.
    """
    next = DeleteRule()
    rule = CopyRule(next, condition=lambda path: False, destination="copy.txt")

    path = PPath("test.txt")
    path.touch()

    rule.process_file(path)

    assert not PPath("copy.txt").exists()
    assert not PPath("test.txt").exists()


def test_deletion_after_rules_executed(fs: FakeFilesystem) -> None:
    """Test scenario for deletion after rules are executed.

    This function tests the behavior of a deletion rule in combination with
    other rules, to check if the file is deleted after all rules have been executed
    """
    next = CopyRule(destination="copy.txt")
    rule = DeleteRule(next)

    path = PPath("test.txt")
    path.touch()

    rule.process_file(path)

    assert not PPath("test.txt").exists()
    assert PPath("copy.txt").exists()


def test_process_raise_when_file(fs: FakeFilesystem) -> None:
    """Test process method raise for file.

    This test checks if the process method of the Rule class raises a NotADirectoryError
    when attempting to process a file path.
    """
    path = PPath("test.txt")
    path.touch()

    with pytest.raises(NotADirectoryError):
        Rule().process(path)


def test_process(fs: FakeFilesystem) -> None:
    """Test process method for a folder.

    This test verifies the behavior of the process method of the Rule class when
    processing a folder. It creates a folder with files, applies a rule, and
    then checks the state of the folder and files.
    """
    folder = PPath("trash_folder/")
    folder.mkdir()

    file1 = PPath("f1.txt")
    file1.touch()

    file2 = PPath("f2.txt")
    file2.touch()

    rule = DeleteRule()
    rule.process(folder)

    assert all(not item.exists() for item in folder.iterdir())


def test_process_empty_dir(fs: FakeFilesystem) -> None:
    folder = PPath("empty_folder/")
    folder.mkdir()

    assert all(not item.exists() for item in folder.iterdir())

    rule = DeleteRule()
    rule.process(folder)


def test_eq() -> None:
    assert Rule() != ""
    assert Rule() != 0

    assert DeleteRule() == DeleteRule()
    assert DeleteRule() != CopyRule()

    assert Rule() != Rule(condition=[lambda x: True])

    assert Rule() != Rule(next=Rule())
    assert Rule(next=Rule()) != Rule(next=Rule(condition=lambda x: True))

    assert CopyRule() != CopyRule(destination="/")


# DeleteRule class


def test_apply_delete_rule(fs: FakeFilesystem) -> None:
    """Test apply_rule method for DeleteRule.

    This test checks the behavior of the apply_rule method of the DeleteRule class.
    It verifies that the method correctly deletes the provided path.
    """
    with PPath("test.txt") as path:
        path.touch()

        assert path.exists()

        assert not DeleteRule().apply_rule(path)

        assert not path.exists()


def test_process_file_delete_rule(fs: FakeFilesystem) -> None:
    """Test process_file method for DeleteRule.

    This test checks the behavior of the process_file method of the DeleteRule class.
    It verifies that the method deletes the file based on the condition provided.
    """
    path = PPath("test.txt")
    path.touch()

    with DeleteRule(condition=lambda x: False) as rule:
        rule.process_file(path)
        assert path.exists()

    with DeleteRule(condition=lambda x: True) as rule:
        rule.process_file(path)
        assert not path.exists()


# CopyRule class
def test_apply_copy_rule(fs: FakeFilesystem) -> None:
    """Test apply_rule method for CopyRule.

    This test checks the behavior of the apply_rule method of the CopyRule class.
    It verifies that the method correctly copies the original file to the
    specified destinations.
    """
    original = PPath("test.txt")
    original.touch()

    destinations = [PPath("destination1"), PPath("destination2")]
    [path.mkdir() for path in destinations]

    assert CopyRule(destination=destinations).apply_rule(original)

    assert original.exists()
    for destination in destinations:
        assert (destination / "test.txt").exists()


# MoveRule class
def test_apply_move_rule(fs: FakeFilesystem) -> None:
    """Test apply_rule method for MoveRule.

    This test checks the behavior of the apply_rule method of the MoveRule class.
    It verifies that the method correctly moves the original file to the
    specified destinations.
    """
    original = PPath("test.txt")
    original.touch()

    destinations = [PPath("destination1"), PPath("destination2")]
    [path.mkdir() for path in destinations]

    assert not MoveRule(destination=destinations).apply_rule(original)

    assert not original.exists()
    for destination in destinations:
        assert (destination / "test.txt").exists()


# CopyByValue class
def test_apply_copy_by_value_rule(fs: FakeFilesystem) -> None:
    """Test apply_rule method for CopyByValueRule.

    This test checks the behavior of the apply_rule method of the CopyByValue class.
    It verifies that the method correctly moves the original file to the
    correct folders depending of the return value of the sort_by function.
    """
    destination = PPath("destination")
    destination.mkdir()

    text_file1 = PPath("text_file1.txt")
    text_file1.touch()

    text_file2 = PPath("text_file2.txt")
    text_file2.touch()

    image_file = PPath("image_file.png")
    image_file.touch()

    def get_extension(path: PPath) -> str:
        return path.suffix

    rule = CopyByValueRule(destination=destination, sort_by=get_extension)
    assert rule.sort_by == get_extension

    for file in (text_file1, text_file2, image_file):
        assert not isinstance(file, str)
        rule.apply_rule(file)
        assert file.exists() and (destination / file.suffix / file.name).exists()


def test_apply_copy_by_value_rule_no_sort_by(fs: FakeFilesystem) -> None:
    """This function tests the apply_rule function when sort_by is not specified."""
    destination = PPath("destination")
    destination.mkdir()

    file = PPath("test.png")
    file.touch()

    rule = CopyByValueRule(destination=destination, sort_by=None)
    rule.apply_rule(file)

    assert (destination / "Undefined" / file.name).exists()
