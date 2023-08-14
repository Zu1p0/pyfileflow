from typing_extensions import Callable, Literal, Optional, Type, TypeAlias, Union

from .path import Path

Condition: TypeAlias = Callable[[Path], bool]
ActionStr: TypeAlias = Literal[
    "move",
    "delete",
    "move_by_value",
]


class Rule:
    def __new__(
        cls: Type["Rule"], action: ActionStr = "move", *args, **kwargs
    ) -> "Rule":
        rule_type = ACTION_TO_TYPES.get(action, "UnsupportedAction")

        if rule_type == "UnsupportedAction":
            raise NotImplementedError("Unsupported action: {}".format(action))

        return super(cls, rule_type).__new__(rule_type)

    def __init__(self, action: ActionStr = "move") -> None:
        self.action = action

    def check_path(self, path: Path) -> bool:  # pragma: no cover
        raise NotImplementedError(
            "The original check_path method of the Rule class should not be accessible."
        )


class DeleteRule(Rule):
    def __init__(
        self,
        action: ActionStr,
        condition: Optional[Union[Condition, list[Condition]]] = None,
    ) -> None:
        super().__init__(action="delete")

        if not isinstance(condition, list):
            self.condition = [condition]
        else:
            self.condition = condition

        self.condition = [
            condition for condition in self.condition if condition is not None
        ]

    def check_path(self, path: Path) -> bool:
        return all(condition(path) for condition in self.condition)


class MoveRule(Rule):
    ...


class MoveByValueRule(Rule):
    ...


ACTION_TO_TYPES = {
    "move": MoveRule,
    "delete": DeleteRule,
    "move_by_value": MoveByValueRule,
}
