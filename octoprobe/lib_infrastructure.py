import dataclasses
import io
import textwrap

from octoprobe.infrastructure_tutorial.config_constants import EnumFut, TentacleType
from octoprobe.lib_tentacle import Tentacle, UsbHub


@dataclasses.dataclass
class Infrastructure:
    tentacles: list[Tentacle]
    hubs: list[UsbHub] = dataclasses.field(default_factory=list)

    def __post_init__(self) -> None:
        assert isinstance(self.tentacles, list)
        assert isinstance(self.hubs, list)

    @property
    def description_short(self) -> str:
        f = io.StringIO()
        f.write("TENTACLES\n")
        for tentacle in self.tentacles:
            f.write(textwrap.indent(tentacle.description_short, prefix="  "))

        if len(self.hubs) > 1:
            f.write("\n\nHUBS\n")
            for hub in self.hubs:
                f.write(textwrap.indent(hub.description_short, prefix="  "))

        return f.getvalue()

    def get_tentacles_for_type(
        self,
        tentacle_type: TentacleType,
        required_futs: list[EnumFut],
    ) -> list[Tentacle]:
        return [
            t
            for t in self.tentacles
            if (t.tentacle_spec.tentacle_type is tentacle_type)
            and (t.has_required_futs(required_futs))
        ]

    def get_tentacle(self, tentacle_type: TentacleType) -> Tentacle:
        assert isinstance(tentacle_type, TentacleType)
        for tentacle in self.tentacles:
            if tentacle.tentacle_spec.tentacle_type is tentacle_type:
                return tentacle
        raise ValueError(f"No tentacle found with type {tentacle_type}!")
