"""
manager.py
"""

from collections.abc import Iterator
from typing import cast
import pygame

from .types import MenuType
from .elements import Button, InputField


class MenuManager:
    """Manages a push/pop stack of Menu objects and routes input to them."""

    def __init__(self) -> None:
        self._menus: dict[type[MenuType], MenuType] = {}
        self._stack: list[MenuType] = []

    def __len__(self) -> int:
        """Returns the number of menus"""
        return len(self._menus.keys())

    """
    Menu mutations.
    """

    def add_menu(self, menu: MenuType) -> None:
        """"""
        self._menus[type(menu)] = menu

    def drop_menu(self, menu_type: type[MenuType]) -> None:
        """"""
        self._menus.pop(menu_type)

    def set_menu(self, menu: MenuType) -> None:
        """"""
        self._menus[type(menu)] = menu

    def clear_menus(self) -> None:
        """"""
        self._menus.clear()

    """
    Menu queries.
    """

    def get_menu[T: MenuType](self, menu_type: type[T]) -> T | None:
        """"""
        return cast("T | None", self._menus.get(menu_type))

    def has_menu(self, menu_type: type[MenuType]) -> bool:
        """"""
        return menu_type in self._menus

    def all_menus(self) -> Iterator[MenuType]:
        """"""
        return iter(self._menus.values())

    """
    Stack mutations.
    """

    def push_stack(self, menu_type: type[MenuType]) -> None:
        """Push a menu onto the stack by its type."""
        menu = self._menus.get(menu_type)
        if menu is not None:
            self._stack.append(menu)

    def pop_stack(self) -> MenuType | None:
        """Pop the top menu from the stack."""
        if len(self._stack) > 1:
            return self._stack.pop()
        return None

    def clear_stack(self) -> None:
        """Remove all menus from the stack."""
        self._stack.clear()

    """
    Stack queries.
    """

    def top(self) -> MenuType | None:
        """"""
        if len(self._stack) >= 1:
            return self._stack[-1]
        return None

    def in_stack(self, menu_type: type[MenuType]) -> bool:
        """"""
        return menu_type in self._stack

    def depth_stack(self) -> int:
        """"""
        return len(self._stack)

    @property
    def stack(self) -> Iterator[MenuType]:
        return iter(self._stack)


# Module-level singleton
menu_manager: MenuManager = MenuManager()
