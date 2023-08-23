import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from typeguard_ignore import suppress_type_checks

from pyfileflow.path import PPath
from pyfileflow.rule import CopyRule, DeleteRule, MoveByValueRule, MoveRule, Rule


# Rule class
def test_rule_context_manager() -> None:
    with Rule() as rule:
        assert rule


def test_rule_instancing() -> None:
    assert isinstance(Rule(action="delete"), DeleteRule)
    assert isinstance(Rule(action="copy"), CopyRule)
    assert isinstance(Rule(action="move"), MoveRule)
    assert isinstance(Rule(action="move_by_value"), MoveByValueRule)


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


# DeleteRule class
def test_apply_delete_rule(fs: FakeFilesystem) -> None:
    with PPath("test.txt") as path:
        path.touch()

        assert path.exists()

        Rule(action="delete").apply_rule(path)

        assert not path.exists()


def test_process_delete_rule(fs: FakeFilesystem) -> None:
    path = PPath("test.txt")
    path.touch()

    with Rule(action="delete", condition=lambda x: False) as rule:
        rule.process_path(path)
        assert path.exists()

    with Rule(action="delete", condition=lambda x: True) as rule:
        rule.process_path(path)
        assert not path.exists()


# CopyRule class
def test_apply_copy_rule(fs: FakeFilesystem) -> None:
    original = PPath("test.txt")
    original.touch()

    destinations = [PPath("destination1"), PPath("destination2")]
    [path.mkdir() for path in destinations]

    Rule(action="copy", destination=destinations).apply_rule(original)

    assert original.exists()
    for destination in destinations:
        assert (destination / "test.txt").exists()


# MoveRule class
def test_apply_move_rule(fs: FakeFilesystem) -> None:
    original = PPath("test.txt")
    original.touch()

    destinations = [PPath("destination1"), PPath("destination2")]
    [path.mkdir() for path in destinations]

    Rule(action="move", destination=destinations).apply_rule(original)

    assert not original.exists()
    for destination in destinations:
        assert (destination / "test.txt").exists()


# MoveByValue class
