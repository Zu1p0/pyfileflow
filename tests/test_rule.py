"""Test module for pyfileflow rule classes.

This module contains unit tests for the various rule classes in the pyfileflow library.
"""

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from typeguard_ignore import suppress_type_checks

from pyfileflow.ppath import PPath
from pyfileflow.rule import CopyByValueRule, CopyRule, DeleteRule, MoveRule, Rule


# Rule class
def test_rule_instancing() -> None:
    """Test rule instance creation.

    This test verifies the creation of different rule instances using the Rule
    class constructor. It checks whether instances of DeleteRule, CopyRule,
    MoveRule, and CopyByValueRule can be created.
    """
    assert isinstance(Rule(action="delete"), DeleteRule)
    assert isinstance(Rule(action="copy"), CopyRule)
    assert isinstance(Rule(action="move"), MoveRule)
    assert isinstance(Rule(action="copy_by_value"), CopyByValueRule)


def test_rule_context_manager() -> None:
    """Test rule context manager behavior.

    This test verifies the behavior of using a Rule instance within a context manager.
    It checks if the Rule instance can be used as a context manager without errors.
    """
    with Rule() as rule:
        assert rule


@suppress_type_checks
def test_not_implemented_rule_instancing() -> None:
    """Test instancing of not implemented rule.

    This test checks if attempting to create a Rule instance with a non-existin
    action raises a NotImplementedError.
    """
    with pytest.raises(NotImplementedError):
        Rule(action="not existing rule action")  # type: ignore[arg-type]


@suppress_type_checks
def test_next_not_rule() -> None:
    """Test instancing a rule with a next value not an instance of Rule."""
    with pytest.raises(TypeError):
        Rule(next=1)  # type: ignore[arg-type]


def test_passing_conditions() -> None:
    """Test rule condition handling.

    This test verifies that the Rule class correctly handles different types of
    conditions provided during instance creation.
    """

    def condition(file: PPath) -> True:
        return True

    assert Rule(condition=condition).condition == [condition]
    assert Rule(condition=[condition, condition]).condition == [
        condition,
        condition,
    ]


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
    next = Rule(action="delete")
    rule = Rule(next, action="copy", destination="copy.txt")

    path = PPath("test.txt")
    path.touch()

    rule.process_file(path)

    assert PPath("copy.txt").exists()
    assert not PPath("test.txt").exists()


def test_next_calling_condition_false(fs: FakeFilesystem) -> None:
    """Test calling next rule when the condition is false.

    This test verifies that the 'next' rule is not called when the condition of
    the current rule is false.
    """
    next = Rule(action="delete")
    rule = Rule(
        next, action="copy", condition=lambda path: False, destination="copy.txt"
    )

    path = PPath("test.txt")
    path.touch()

    rule.process_file(path)

    assert not PPath("copy.txt").exists()
    assert not PPath("test.txt").exists()


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

    rule = Rule(action="delete")
    rule.process(folder)

    assert all(not item.exists() for item in folder.iterdir())


def test_process_empty_dir(fs: FakeFilesystem) -> None:
    folder = PPath("empty_folder/")
    folder.mkdir()

    assert all(not item.exists() for item in folder.iterdir())

    rule = Rule(action="delete")
    rule.process(folder)


# DeleteRule class


def test_apply_delete_rule(fs: FakeFilesystem) -> None:
    """Test apply_rule method for DeleteRule.

    This test checks the behavior of the apply_rule method of the DeleteRule class.
    It verifies that the method correctly deletes the provided path.
    """
    with PPath("test.txt") as path:
        path.touch()

        assert path.exists()

        assert not Rule(action="delete").apply_rule(path)

        assert not path.exists()


def test_process_file_delete_rule(fs: FakeFilesystem) -> None:
    """Test process_file method for DeleteRule.

    This test checks the behavior of the process_file method of the DeleteRule class.
    It verifies that the method deletes the file based on the condition provided.
    """
    path = PPath("test.txt")
    path.touch()

    with Rule(action="delete", condition=lambda x: False) as rule:
        rule.process_file(path)
        assert path.exists()

    with Rule(action="delete", condition=lambda x: True) as rule:
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

    assert Rule(action="copy", destination=destinations).apply_rule(original)

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

    assert not Rule(action="move", destination=destinations).apply_rule(original)

    assert not original.exists()
    for destination in destinations:
        assert (destination / "test.txt").exists()


# CopyByValue class
