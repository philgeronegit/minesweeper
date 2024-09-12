from dataclasses import dataclass


@dataclass
class Widget:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0


class VerticalLayout:
    def __init__(
        self, left_margin: int = 20, space_between: int = 5, top_margin: int = 20
    ) -> None:
        self.widgets: list[Widget] = []
        self.left_margin = left_margin
        self.space_between = space_between
        self.top_margin = top_margin

    def add(self, widget: Widget):
        widget.x = self.left_margin
        widget.y = self.compute_height()
        self.widgets.append(widget)

    def compute_height(self) -> int:
        if len(self.widgets) == 0:
            return self.top_margin
        return sum(widget.height for widget in self.widgets) + self.space_between * (
            len(self.widgets) - 1
        )
