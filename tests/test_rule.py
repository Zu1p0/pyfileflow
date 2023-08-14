import pytest
from typeguard_ignore import suppress_type_checks

from pyfileflow.path import Path
from pyfileflow.rule import DeleteRule, MoveByValueRule, MoveRule, Rule


# Rule class
def test_rule_instancing() -> None:
    assert isinstance(Rule(action="move"), MoveRule)
    assert isinstance(Rule(action="delete"), DeleteRule)
    assert isinstance(Rule(action="move_by_value"), MoveByValueRule)


@suppress_type_checks
def test_not_implemented_rule_instancing() -> None:
    with pytest.raises(NotImplementedError):
        Rule(action="not existing rule action")  # type: ignore[arg-type]


# DeleteRule class
def test_delete_passing_conditions() -> None:
    def condition(file: Path) -> True:
        return True

    assert Rule(action="delete", condition=condition).condition == [condition]
    assert Rule(action="delete", condition=[condition, condition]).condition == [
        condition,
        condition,
    ]


def test_delete_check_path() -> None:
    assert Rule(action="delete", condition=[lambda x: True, lambda x: True]).check_path(
        Path("")
    )
    assert not Rule(
        action="delete", condition=[lambda x: True, lambda x: False]
    ).check_path(Path(""))
