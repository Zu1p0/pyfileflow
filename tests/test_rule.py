import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from typeguard_ignore import suppress_type_checks

from pyfileflow.path import PPath
from pyfileflow.rule import CopyByValueRule, CopyRule, DeleteRule, MoveRule, Rule


# Rule class
def test_rule_instancing() -> None:
    assert isinstance(Rule(action="delete"), DeleteRule)
    assert isinstance(Rule(action="copy"), CopyRule)
    assert isinstance(Rule(action="move"), MoveRule)
    assert isinstance(Rule(action="copy_by_value"), CopyByValueRule)


def test_rule_context_manager() -> None:
    with Rule() as rule:
        assert rule


@suppress_type_checks
def test_not_implemented_rule_instancing() -> None:
    with pytest.raises(NotImplementedError):
        Rule(action="not existing rule action")  # type: ignore[arg-type]


def test_passing_conditions() -> None:
    def condition(file: PPath) -> True:
        return True

    assert Rule(condition=condition).condition == [condition]
    assert Rule(condition=[condition, condition]).condition == [
        condition,
        condition,
    ]


def test_check_path() -> None:
    with PPath("") as path:
        assert Rule(condition=[lambda x: True, lambda x: True]).check_path(path)
        assert not Rule(condition=[lambda x: True, lambda x: False]).check_path(path)


def test_next_calling_condition_true(fs: FakeFilesystem) -> None:
    next = Rule(action="delete")
    rule = Rule(next, action="copy", destination="copy.txt")

    path = PPath("test.txt")
    path.touch()

    rule.process_file(path)

    assert PPath("copy.txt").exists()
    assert not PPath("test.txt").exists()


def test_next_calling_condition_false(fs: FakeFilesystem) -> None:
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
    path = PPath("test.txt")
    path.touch()

    with pytest.raises(NotADirectoryError):
        Rule().process(path)


def test_process(fs: FakeFilesystem) -> None:
    folder = PPath("trash_folder/")
    folder.mkdir()

    file1 = PPath("f1.txt")
    file1.touch()

    file2 = PPath("f2.txt")
    file2.touch()

    rule = Rule(action="delete")
    rule.process(folder)

    assert all(folder.iterdir())


# DeleteRule class
def test_apply_delete_rule(fs: FakeFilesystem) -> None:
    with PPath("test.txt") as path:
        path.touch()

        assert path.exists()

        assert not Rule(action="delete").apply_rule(path)

        assert not path.exists()


def test_process_file_delete_rule(fs: FakeFilesystem) -> None:
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
    original = PPath("test.txt")
    original.touch()

    destinations = [PPath("destination1"), PPath("destination2")]
    [path.mkdir() for path in destinations]

    assert not Rule(action="move", destination=destinations).apply_rule(original)

    assert not original.exists()
    for destination in destinations:
        assert (destination / "test.txt").exists()


# CopyByValue class
