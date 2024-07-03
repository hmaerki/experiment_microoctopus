import dataclasses
import io
import textwrap

from octoprobe.lib_tentacle import Tentacle, UsbHub


@dataclasses.dataclass
class Infrastructure:
    tentacles: list[Tentacle]
    hubs: list[UsbHub]

    def __post_init__(self) -> None:
        for tentacle in self.tentacles:
            if tentacle.builtin_hub is None:
                continue
            for hub in self.hubs:
                assert hub is not tentacle.builtin_hub
            self.hubs.append(tentacle.builtin_hub)

    @property
    def description_short(self) -> str:
        f = io.StringIO()
        f.write("TENTACLES\n")
        for tentacle in self.tentacles:
            f.write(textwrap.indent(tentacle.description_short, prefix="  "))

        f.write("\n\nHUBS\n")
        for hub in self.hubs:
            f.write(textwrap.indent(hub.description_short, prefix="  "))

        return f.getvalue()
