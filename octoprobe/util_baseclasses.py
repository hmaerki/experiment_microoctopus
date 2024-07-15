import dataclasses


@dataclasses.dataclass(frozen=True)
class PropertyString:
    """
    Example: programmer=picotool,xy=5
    """

    text: str

    def get_tag(self, tag: str) -> None | str:
        """
        Example: get_tag("xy") -> "5"
        """
        for x in self.text.split(","):
            _tag, value = x.split("=")
            if _tag == tag:
                return value
        return None


@dataclasses.dataclass
class TentacleType:
    category: str
    label: str
    doc: str
    tags: str
    octobus: str
    relay_1: str | None = None
    relay_2: str | None = None
    relay_3: str | None = None
    relay_4: str | None = None
    relay_5: str | None = None
    relay_6: str | None = None
