"""
elements.py
"""

from abc import ABC
from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from itertools import count
from typing import Callable, ClassVar, Any
from typing import TYPE_CHECKING, Annotated, ClassVar
import math
import re
import uuid


FLOAT_REGEX = r"^[+-]?(\d+(\.\d*)?|\.\d+)$"
INT_REGEX = r"^[+-]?\d+$"
LETTERS_REGEX = r"^[A-Za-z]+$"
ALPHANUMERIC_REGEX = r"^[A-Za-z0-9]+$"
RGBA_REGEX = r"^#[0-9a-fA-F]{8}$"
BOOL_REGEX = r"^[01]$"

RGBA = Annotated[str, f"regex:{RGBA_REGEX}"]
MEASURE = Annotated[tuple[float, float], ""]
ANGLE = Annotated[float, "radians", "range: [0, 2π]"]

COLOR_PALETTE_BASE: RGBA = "#000000FF"
COLOR_PALETTE_SECONDARY: RGBA = "#000000FF"
COLOR_PALETTE_ACCENT: RGBA = "#4E4546FF"
COLOR_PALETTE_NEUTRAL: RGBA = "#30384EFF"
COLOR_PALETTE_TEXT: RGBA = "#000000FF"

TRANSPARENT: RGBA = "#00000000"
BLACK: RGBA = "#000000FF"
RED: RGBA = "#FF0000FF"
GREEN: RGBA = "#00FF00FF"
BLUE: RGBA = "#0000FFFF"
YELLOW: RGBA = "#FFFF00FF"
MAGENTA: RGBA = "#FF00FFFF"
CYAN: RGBA = "#00FFFFFF"
WHITE: RGBA = "#FFFFFFFF"

NATIVE_FONT_SIZE: int = 18


"""
Attribute types.
"""


class MeasureType(Enum):
    """
    Represents types of measurement, with possible values ABSOLUTE and
    RELATIVE.
    """

    ABSOLUTE = auto()
    RELATIVE = auto()


class JustifyType(Enum):
    """
    Represents text justification options with three enum members: START,
    CENTER, and END. Use JustifyType to specify alignment in layouts or
    formatting contexts.
    """

    START = auto()
    CENTER = auto()
    END = auto()


class AlignmentType(Enum):
    """
    Represents possible alignment positions, such as TOPLEFT, CENTER, and
    BOTTOMRIGHT, for layout or positioning purposes.
    """

    TOPLEFT = auto()
    MIDTOP = auto()
    TOPRIGHT = auto()
    MIDLEFT = auto()
    CENTER = auto()
    MIDRIGHT = auto()
    BOTTOMLEFT = auto()
    MIDBOTTOM = auto()
    BOTTOMRIGHT = auto()


class TextDecorationTypes(Flag):
    """
    Represents a set of text decoration options using a flag enumeration,
    including NONE, ANTIALIASING, BOLD, ITALIC, STRIKETHROUGH, and
    UNDERLINE. Multiple decorations can be combined using bitwise
    operations.
    """

    NONE = 0
    ANTIALIASING = auto()
    BOLD = auto()
    ITALIC = auto()
    STRIKETHROUGH = auto()
    UNDERLINE = auto()


class OverflowType(Enum):
    """
    Represents the type of overflow handling, with options: CLIP, EXTEND,
    and OVERFLOW.
    """

    CLIP = auto()
    EXTEND = auto()
    OVERFLOW = auto()


"""
Base Element. The class is the foundational building block for all menu components
in the game. It defines the core properties and behaviors that are shared across
different types of UI elements, including positioning, styling, text rendering,
and interaction states. By inheriting from this abstract base class, specific
element types can focus on their unique functionality while leveraging a
consistent interface for layout and appearance customization.
"""


@dataclass(kw_only=True)
class Element(ABC):
    """
    Represents an abstract UI element with configurable layout, appearance,
    and interaction properties, including size, alignment, color, border,
    shadow, and visibility. Designed for subclassing to define specific UI
    components.
    """

    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    justify: JustifyType = JustifyType.CENTER
    alignment: AlignmentType = AlignmentType.TOPLEFT
    overflow: OverflowType = OverflowType.EXTEND

    size: MEASURE = (0.0, 0.0)
    anchor: MEASURE = (0.0, 0.0)
    margin: MEASURE = (0.0, 0.0)
    offset: MEASURE = (0.0, 0.0)
    padding: MEASURE = (0.0, 0.0)

    size_measure: MeasureType = MeasureType.ABSOLUTE
    anchor_measure: MeasureType = MeasureType.ABSOLUTE
    margin_measure: MeasureType = MeasureType.ABSOLUTE
    offset_measure: MeasureType = MeasureType.ABSOLUTE
    padding_measure: MeasureType = MeasureType.ABSOLUTE

    background_color: RGBA = WHITE
    background_alpha: int = 0xFF

    border_thickness: int = 0  # Width of border in pixels, 0 is no border
    border_color: RGBA = TRANSPARENT
    border_alpha: int = 0xFF

    shadow_color: RGBA = TRANSPARENT
    shadow_alpha: int = 0x80
    shadow_scale: float = 1.0
    shadow_offset: MEASURE = (3.0, 3.0)
    shadow_offset_measure: MeasureType = MeasureType.ABSOLUTE

    is_selectable: bool = True  # Whether the element can be selected for interaction
    is_visible: bool = True  # Whether the element should be rendered

    _interaction_target: Element | None = None


"""
Non-visual components.
"""


@dataclass(kw_only=True)
class Division(Element):
    """
    Represents a container element that groups multiple Element instances
    with configurable spacing, background, and shadow colors. The Division
    is not directly selectable or expandable.
    """

    elements: list[Element] = field(default_factory=lambda: [])

    gap: MEASURE = (4.0, 4.0)  # Spacing between internal elements
    gap_measure: MeasureType = MeasureType.ABSOLUTE

    background_color: RGBA = TRANSPARENT
    shadow_color: RGBA = TRANSPARENT

    is_selectable: bool = False  # Containers are not directly selectable
    is_expandable: bool = False


@dataclass(kw_only=True)
class HorizontalDivision(Division):
    """
    Represents a horizontal division, inheriting from Division. This class
    is a dataclass with keyword-only initialization and currently does not
    add additional attributes or methods.
    """

    pass


@dataclass(kw_only=True)
class VerticalDivision(Division):
    """
    Represents a specialized Division that models a vertical partition;
    inherits all behavior from Division without adding new attributes or
    methods.
    """

    pass


VerticalDivision()


@dataclass(kw_only=True)
class Gap(Element):
    """
    Represents a layout element with configurable anchor, margin, offset,
    padding, background and shadow colors, and flags for flexibility,
    selectability, and expandability. Inherits from Element.
    """

    anchor: MEASURE = (0.0, 0.0)
    margin: MEASURE = (0.0, 0.0)
    offset: MEASURE = (0.0, 0.0)
    padding: MEASURE = (0.0, 0.0)

    background_color: RGBA = TRANSPARENT
    shadow_color: RGBA = TRANSPARENT

    is_flexible: bool = False
    is_selectable: bool = False
    is_expandable: bool = False


"""
Static elements. Non-interactive components that provide visual structure
and information display within menus. These elements do not respond to user
input but serve important roles in organizing menu layouts and presenting
content. They include dividers for visual separation, text blocks for labels
and descriptions, and images for decorative or illustrative purposes. Static
elements help create clear visual hierarchy and improve the overall user
experience by providing context and organization to interactive components.
"""


@dataclass(kw_only=True)
class Text(Element):
    """
    Represents a text element with customizable content, color, background,
    font, size, decorations, and selection or wrapping options. Inherits
    from Element.
    """
    """"""

    text: str = ""  # Text content to display
    text_color: RGBA = WHITE
    text_background: RGBA = TRANSPARENT  # Highlight color
    text_alpha: int = 0xFF
    text_decorations: TextDecorationTypes = TextDecorationTypes.NONE

    font_path: str = "editundo.ttf"  # Font family filename for text rendering
    font_size: int = 18  # Font size in pixels for text rendering

    background_color: RGBA = TRANSPARENT
    is_selectable: bool = False  # Static labels are not selectable
    is_wrapable: bool = False


@dataclass(kw_only=True)
class NormalText(Text):
    """
    Represents a text element with a default font size of 18, a light gray
    color (#E0E0E0FF), and bold formatting. Inherits from Text.
    """

    font_size: int = 18 * 1
    text_color: RGBA = "#E0E0E0FF"
    text_format: TextDecorationTypes = TextDecorationTypes.BOLD


@dataclass(kw_only=True)
class TitleText(Text):
    """
    Represents a styled text element for titles, extending Text with a
    larger default font_size, customizable text_color, and optional
    text_format decoration.
    """

    font_size: int = 18 * 4
    text_color: RGBA = WHITE
    text_format: TextDecorationTypes = TextDecorationTypes.NONE


@dataclass(kw_only=True)
class SubtitleText(Text):
    """
    Represents styled subtitle text with customizable font_size, text_color,
    text_background, and text_format. Inherits from Text. Default font size
    is 18, with black text on a white background and no text decoration.
    """

    font_size: int = 18
    text_color: RGBA = BLACK
    text_background: RGBA = WHITE
    text_format: TextDecorationTypes = TextDecorationTypes.NONE


@dataclass(kw_only=True)
class HeadingOneText(Text):
    """
    Represents a level-one heading text style with customizable font, size,
    color, shadow, and text decoration options. Inherits from Text.
    """

    font_path: str = "editundo.ttf"
    font_size: int = 18 * 3

    text_color: RGBA = "#F0B443FF"
    shadow_color: RGBA = "#E6A23EFF"
    shadow_offset: MEASURE = (3.0, 3.0)
    text_format: TextDecorationTypes = TextDecorationTypes.NONE


@dataclass(kw_only=True)
class HeadingTwoText(Text):
    """
    Represents a level-two heading text style with customizable font, size,
    color, shadow, and text decoration options. Inherits from Text.
    """

    font_path: str = "editundo.ttf"
    font_size: int = 18 * 2

    text_color: RGBA = "#F0B443FF"
    shadow_color: RGBA = "#E6A23EFF"
    shadow_offset: MEASURE = (2.0, 2.0)
    text_format: TextDecorationTypes = TextDecorationTypes.NONE


@dataclass(kw_only=True)
class HeadingThreeText(Text):
    """
    Represents a level-three heading text style with customizable font,
    size, color, shadow, and text decoration options. Inherits from Text.
    """

    font_path: str = "editundo.ttf"
    font_size: int = NATIVE_FONT_SIZE

    text_color: RGBA = "#F0B443FF"
    shadow_color: RGBA = "#E6A23EFF"
    shadow_offset: MEASURE = (1.0, 1.0)
    text_format: TextDecorationTypes = TextDecorationTypes.NONE


"""
Interactive elements. User-controllable components that enable player
input and decision-making within menus. These elements respond to keyboard
and other input methods, allowing players to navigate, make selections, and
modify settings. They include buttons for triggering actions, toggles for
binary choices, sliders for numeric adjustments, and input fields for text
entry. Each interactive element provides visual feedback and maintains state
to ensure clear communication of available options and current selections.
"""


@dataclass(kw_only=True)
class Button(Element):
    """
    Represents a UI button element with customizable label text, appearance,
    and an associated action callable. The button supports styling options
    such as padding, background color, border, and shadow, and can be
    activated by calling its instance.
    """

    @dataclass(kw_only=True)
    class ButtonText(NormalText):
        """
        Represents styled text for a button, extending NormalText with a larger
        font size, light text color, and horizontal padding. Suitable for button
        labels in a UI.
        """

        font_size: int = int(18 * 1.5)
        text_color: RGBA = "#F0F0F0FF"

    label: Text = field(default_factory=ButtonText)  # Text element used for rendering the button label
    action: Callable[[], None] = field(default=lambda: None)  # Function to call when button is activated

    padding: MEASURE = (10.0, 2.0)
    background_color: RGBA = "#30384eFF"
    border_color: RGBA = "#606060FF"
    border_thickness: int = 1
    shadow_color: RGBA = "#30384eFF"
    shadow_alpha: int = 0xB0
    shadow_scale: float = 1.0

    selected_text_color: RGBA = "#EC4662FF"

    def __call__(self):
        """
        Invokes the button's associated action when the Button instance is
        called like a function.
        """
        self.action()


@dataclass(kw_only=True)
class InputField(Element):

    @dataclass(kw_only=True)
    class InputHintText(NormalText):
        """
        Represents a styled hint text for input fields, with customizable text,
        font_size, text_color, and text_decorations. Inherits from NormalText
        and defaults to displaying "[RETURN]" in italic with antialiasing.
        """

        text: str = "[RETURN]"
        font_size: int = int(18 * 1.5)
        text_color: RGBA = "#30384EFF"
        text_decorations: TextDecorationTypes = TextDecorationTypes.ITALIC | TextDecorationTypes.ANTIALIASING

    @dataclass(kw_only=True)
    class InputValueText(NormalText):
        """
        Represents a styled text input value with a customizable font_size and
        text_color, inheriting from NormalText. Designed for use where input
        text appearance needs to be specified.
        """

        font_size: int = int(18 * 1.5)
        text_color: RGBA = "#F0F0F0FF"

    label: Text = field(default_factory=InputHintText)  # Current committed text value
    hint: Text = field(default_factory=InputHintText)  # Current committed text value
    value: Text = field(default_factory=InputValueText)  # Current committed text value
    action: Callable[[str], None] = field(default=lambda v: None)  # Function called with new value when committed
    authenticator: Callable[[str], bool] = field(default=lambda s: bool(re.fullmatch(ALPHANUMERIC_REGEX, s)))

    size: MEASURE = (64.0, 25.0)
    padding: MEASURE = (4.0, 2.0)
    background_color: RGBA = "#0C0E14FF"
    border_color: RGBA = "#E0E0E0FF"
    border_thickness: int = 1
    shadow_color: RGBA = "#30384eFF"
    shadow_alpha: int = 0xB0
    shadow_scale: float = 1.0

    selected_border_color: RGBA = "#EC4662FF"
    inauthentic_text_color: RGBA = "#EC4662FF"
    open_cursor_color: RGBA = "#EC4662FF"

    is_flexible: bool = False

    _is_editing: bool = field(default=False, init=False, repr=False)  # Internal flag indicating edit mode
    _buffer_text: str = field(default="", init=False, repr=False)  # Internal buffer for text being edited

    _frames = ["_", ""]
    _frame_duration: float = 0.5
    _current_frame: int = 0

    def __call__(self):
        if not self.is_open:
            self.open()

    @property
    def is_open(self) -> bool:
        """Return True if the input field is currently in edit mode."""
        return self._is_editing

    def authenticate(self) -> bool:
        """"""
        return self.authenticator(self.get_field())

    def get_field(self) -> str:
        """Buffer while editing, or the committed value otherwise."""
        return self._buffer_text if self._is_editing else self.value.text

    def get_cursor(self) -> str:
        """"""
        if not self._is_editing:
            return ""
        from config import FPS

        repeats = max(1, round(self._frame_duration * FPS))
        stretched_frames = [f for f in self._frames for _ in range(repeats)]
        frame = stretched_frames[self._current_frame % len(stretched_frames)]
        self._current_frame = (self._current_frame + 1) % len(stretched_frames)
        return frame

    """
    Change value. Provide functionality for modifying the input field's text 
    content when the input is open. Until the input is closed, the new version
    of the text is stored in a buffer.
    """

    def open(self) -> None:
        """Enter edit mode, copying the current value to the edit buffer."""
        self._is_editing = True
        self._buffer_text = self.value.text
        self._current_frame = 0

    def append(self, character: str) -> None:
        """Add a character to the edit buffer if currently editing."""
        if self._is_editing:
            self._buffer_text += character.upper()
        self._current_frame = 0

    def truncate(self) -> None:
        """Remove the last character from the edit buffer if currently editing."""
        if self._is_editing and self._buffer_text:
            self._buffer_text = self._buffer_text[:-1]
        self._current_frame = 0

    def close(self) -> None:
        """Commit the edit buffer as the new value and exit edit mode."""
        if self._is_editing and self.authenticate():
            self.value.text = self._buffer_text
            self._is_editing = False
            self.action(self.value.text)

    def cancel(self) -> None:
        """Discard the edit buffer and exit edit mode without saving."""
        self._is_editing = False
        self._buffer_text = ""
