"""Rules implementation.

Implement classes for all rules in pyfileflow.
"""

import shutil
from types import TracebackType

from typing_extensions import Any, Callable, Literal, Optional, Self, TypeAlias, Union

from . import utils
from .ppath import PathLike, PPath

ValueFunc: TypeAlias = Callable[[PPath], Any]
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
        action (ActionStr):
            The rule type.
    """

    action: ActionStr

    def __init__(
        self,
        next: Optional["Rule"] = None,
        condition: Optional[Union[Condition, list[Condition]]] = None,
    ) -> None:
        """Initialize a Rule instance.

        Args:
            next (Optional[Rule]): The next rule in the processing chain.
            condition (Optional[Union[Condition, list[Condition]]]):
                Conditions to apply the rule. Should return True if you want the
                rule to be applied to files matching the condition, False otherwise.

        Raises:
            TypeError: The next value is not a Rule instance or None
        """
        self.next = next

        if not isinstance(self.next, Optional[Rule]):
            raise TypeError("The next rule must be a Rule instance or None.")

        self.condition: list[Condition] = utils.parse_args(condition)

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
        folder = PPath(folder)

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

    def __eq__(self, other: Any) -> bool:  # pragma: no cover
        """Compare two Rule instances for equality.

        Args:
            other (Any):
                The other Rule instance to compare.

        Returns:
            bool:
                True if the instances are equal, False otherwise. (If the other
                value is not an instance of Rule, will return False.)
        """
        if not isinstance(other, Rule):
            return False

        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:  # pragma: no cover
        """Compute the hash value of the Rule instance.

        Returns:
            int: The hash value.
        """
        return hash(self.__dict__)


class DeleteRule(Rule):
    """A rule for deleting files.

    Attributes:
        action (ActionStr):
            The rule type. (here action = "delete").
    """

    action = "delete"

    def __init__(
        self,
        next: Rule | None = None,
        condition: Condition | list[Condition] | None = None,
    ) -> None:
        """Initialize a DeleteRule instance.

        Args:
            next (Optional[Rule]): The next rule in the processing chain.
            condition (Optional[Union[Condition, list[Condition]]]):
                Conditions to apply the rule. Should return True if you want the
                rule to be applied to files matching the condition, False otherwise.
        """
        super().__init__(next, condition)

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
    """A rule for copying files.

    Attributes:
        action (ActionStr):
            The rule type. (here action = "copy").
    """

    action = "copy"

    def __init__(
        self,
        next: Rule | None = None,
        condition: Condition | list[Condition] | None = None,
        destination: Optional[Union[PathLike, list[PathLike]]] = None,
    ) -> None:
        """Initialize a Rule instance.

        Args:
            next (Optional[Rule]): The next rule in the processing chain.
            condition (Optional[Union[Condition, list[Condition]]]):
                Conditions to apply the rule. Should return True if you want the
                rule to be applied to files matching the condition, False otherwise.
            destination (Optional[Union[PathLike, list[PathLike]]]):
                The destination in which the file should be copied.
        """
        super().__init__(next, condition)

        self.destination: list[PPath] = [
            PPath(path) for path in utils.parse_args(destination)
        ]

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
    """A rule for moving files.

    Attributes:
        action (ActionStr): The rule type. (here action = "move").
    """

    action = "move"

    def __init__(
        self,
        next: Rule | None = None,
        condition: Condition | list[Condition] | None = None,
        destination: Optional[Union[PathLike, list[PathLike]]] = None,
    ) -> None:
        """Initialize a Rule instance.

        Args:
            next (Optional[Rule]): The next rule in the processing chain.
            condition (Optional[Union[Condition, list[Condition]]]):
                Conditions to apply the rule. Should return True if you want the
                rule to be applied to files matching the condition, False otherwise.
            destination (Optional[Union[PathLike, list[PathLike]]]):
                The destination in which the file should be moved.
        """
        super().__init__(next, condition)

        self.destination: list[PPath] = [
            PPath(path) for path in utils.parse_args(destination)
        ]

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

    Attributes:
        action (ActionStr): The rule type. (here action = "copy_by_value").

    This rule is yet to be implemented.
    """

    action = "copy_by_value"

    ...
