import shutil
from types import TracebackType

from typing_extensions import Callable, Literal, Optional, Self, Type, TypeAlias, Union

from . import utils
from .path import PathLike, PPath

Condition: TypeAlias = Callable[[PPath], bool]
ActionStr: TypeAlias = Literal[
    "delete",
    "copy",
    "move",
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

    def __init__(
        self,
        action: ActionStr = "move",
        condition: Optional[Union[Condition, list[Condition]]] = None,
        destination: Optional[Union[PathLike, list[PathLike]]] = None,
    ) -> None:
        self.action = action

        self.condition: list[Condition] = utils.parse_args(condition)
        self.destination: list[PPath] = [
            PPath(path) for path in utils.parse_args(destination)
        ]

    def check_path(self, path: PPath) -> bool:
        return all(condition(path) for condition in self.condition)

    def apply_rule(self, path: PPath) -> None:  # pragma: no cover
        ...

    def process_path(self, path: PPath) -> None:
        if self.check_path(path):
            self.apply_rule(path)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        t: type[BaseException] | None,
        v: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        pass

    def __eq__(self, other: "Rule") -> bool:
        raise NotImplementedError # to change I think
        return (
            self.action == other.action
            and self.condition == other.condition
            and self.destination == other.destination
        )


class DeleteRule(Rule):
    def apply_rule(self, path: PPath) -> None:
        path.delete()


class CopyRule(Rule):
    def apply_rule(self, path: PPath) -> None:
        for destination in self.destination:
            shutil.copy(path, destination)


class MoveRule(Rule):
    def apply_rule(self, path: PPath) -> None:
        for destination in self.destination:
            shutil.copy(path, destination / path.name)

        path.delete()


class MoveByValueRule(Rule):
    ...


ACTION_TO_TYPES = {
    "delete": DeleteRule,
    "copy": CopyRule,
    "move": MoveRule,
    "move_by_value": MoveByValueRule,
}
