"""Rules implementation.

Implement classes for all rules in pyfileflow.
"""

import shutil
from types import TracebackType

from typing_extensions import Callable, Literal, Optional, Self, Type, TypeAlias, Union

from . import utils
from .ppath import PathLike, PPath

Condition: TypeAlias = Callable[[PPath], bool]
ActionStr: TypeAlias = Literal[
    "delete",
    "copy",
    "move",
    "copy_by_value",
]


class Rule:
    """Base class representing a rule for processing files in a directory.

    Attributes:
        next (Optional[Rule]):
            The next rule in the processing chain.
        action (ActionStr):
            The action to be taken for files matching the conditions.
        condition (list[Condition]):
            List of conditions that files must satisfy to apply the rule.
        destination (list[PPath]):
            List of destinations for the processed files. (For related rules)
    """

    def __new__(
        cls: Type["Rule"],
        next: Optional["Rule"] = None,
        action: ActionStr = "move",
        *args,
        **kwargs
    ) -> "Rule":
        """Create a new Rule instance.

        Args:
            next (Optional[Rule]): The next rule in the processing chain.
            action (ActionStr):
                The action to be taken for files matching the conditions.
            args:
                Variable-length argument list.
            kwargs:
                Arbitrary keyword arguments.

        Returns:
            Rule:
                An instance of the Rule class or its derived class based on the action.

        Raises:
            NotImplementedError: If the specified action is not supported.
        """
        rule_type = ACTION_TO_TYPES.get(action, "UnsupportedAction")

        if rule_type == "UnsupportedAction":
            raise NotImplementedError("Unsupported action: {}".format(action))

        return super(cls, rule_type).__new__(rule_type)

    def __init__(
        self,
        next: Optional["Rule"] = None,
        action: ActionStr = "move",
        condition: Optional[Union[Condition, list[Condition]]] = None,
        destination: Optional[Union[PathLike, list[PathLike]]] = None,
    ) -> None:
        """Initialize a Rule instance.

        Args:
            next (Optional[Rule]): The next rule in the processing chain.
            action (ActionStr):
                The action to be taken for files matching the conditions.
            condition (Optional[Union[Condition, list[Condition]]]):
                Conditions to apply the rule.
            destination (Optional[Union[PathLike, list[PathLike]]]):
                Destinations for processed files.
        """
        self.next = next
        self.action = action
        self.condition: list[Condition] = utils.parse_args(condition)
        self.destination: list[PPath] = [
            PPath(path) for path in utils.parse_args(destination)
        ]

    def check_path(self, path: PPath) -> bool:
        """Check if a file path satisfies all conditions of the rule.

        Args:
            path (PPath): The path of the file to be checked.

        Returns:
            bool: True if the file path satisfies the conditions, False otherwise.
        """
        return all(condition(path) for condition in self.condition)

    def apply_rule(self, path: PPath) -> bool:  # pragma: no cover
        """Apply the rule to a file.

        Args:
            path (PPath): The path of the file to apply the rule to.

        Returns:
            bool: True if the rule has not been deleted, False otherwise.
        """
        return True

    def process_file(self, path: PathLike) -> None:
        """Process a file using the rule and call the next rule.

        Args:
            path (PathLike): The path of the file to be processed.
        """
        path = PPath(path)

        if self.check_path(path):
            if self.apply_rule(path):
                self.next.process_file(path) if self.next is not None else None
        else:
            self.next.process_file(path) if self.next is not None else None

    def process(self, folder: PathLike) -> None:
        """Process all files in a folder using all rules.

        Args:
            folder (PathLike): The folder containing the files to be processed.

        Raises:
            NotADirectoryError: If the provided path is not a directory.
        """
        if not folder.is_dir():
            raise NotADirectoryError("The path to process must be a directory.")

        for path in folder.iterdir():
            self.process_file(path)

    def __enter__(self) -> Self:
        """Context manager entry point.

        Returns:
            Rule: The Rule instance.
        """
        return self

    def __exit__(
        self,
        t: type[BaseException] | None,
        v: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Context manager exit point.

        Args:
            t (type[BaseException] | None): Type of the exception raised, if any.
            v (BaseException | None): The exception instance, if raised.
            tb (TracebackType | None): Traceback information.
        """

    def __eq__(self, other: "Rule") -> bool:  # pragma: no cover
        """Compare two Rule instances for equality.

        Args:
            other (Rule): The other Rule instance to compare.

        Returns:
            bool: True if the instances are equal, False otherwise.

        Raises:
            TypeError: If the other object is not a Rule instance.
        """
        if isinstance(other, Rule):
            return (
                self.action == other.action
                and self.condition == other.condition
                and self.destination == other.destination
            )
        raise TypeError("Cannot compare with non-Rule object")

    def __hash__(self) -> int:  # pragma: no cover
        """Compute the hash value of the Rule instance.

        Returns:
            int: The hash value.
        """
        return hash(self.action, self.condition, self.destination)


class DeleteRule(Rule):
    """A rule for deleting files."""

    def apply_rule(self, path: PPath) -> bool:
        """Apply the delete rule to a file.

        Args:
            path (PPath): The path of the file to apply the rule to.

        Returns:
            bool: Always returns False after deleting the file.
        """
        path.delete()
        return False


class CopyRule(Rule):
    """A rule for copying files."""

    def apply_rule(self, path: PPath) -> bool:
        """Apply the copy rule to a file.

        Args:
            path (PPath): The path of the file to apply the rule to.

        Returns:
            bool: Always returns True after copying the file.
        """
        for destination in self.destination:
            shutil.copy(path, destination)
        return True  # pragma: no cover


class MoveRule(Rule):
    """A rule for moving files."""

    def apply_rule(self, path: PPath) -> bool:
        """Apply the move rule to a file.

        Args:
            path (PPath): The path of the file to apply the rule to.

        Returns:
            bool: Always returns False after moving the file.
        """
        for destination in self.destination:
            shutil.copy(path, destination / path.name)

        path.delete()
        return False


class CopyByValueRule(Rule):
    """A rule for copying files in different folders depending by value.

    This rule is yet to be implemented.
    """

    ...


ACTION_TO_TYPES = {
    "delete": DeleteRule,
    "copy": CopyRule,
    "move": MoveRule,
    "copy_by_value": CopyByValueRule,
}
