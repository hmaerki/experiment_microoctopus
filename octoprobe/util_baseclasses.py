import dataclasses

from octoprobe.infrastructure_tutorial.config_constants import EnumFut, TentacleType


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
class TentacleSpec[T]:
    tentacle_type: TentacleType
    futs: list[EnumFut]
    category: str
    label: str
    doc: str
    tags: str
    relays_closed: dict[EnumFut, list[int]]
    mcu_config: T | None = None

    def get_property(self, tag: str) -> str | None:
        return PropertyString(self.tags).get_tag(tag)
