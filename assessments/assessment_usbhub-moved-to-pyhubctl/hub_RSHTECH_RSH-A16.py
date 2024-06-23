"""
Sequence:
  Create definition of hub
  Query usb and create hub structure
  Find hub definition in hub structure: Create 'hub mount point'.
  Access hub using 'hub mount point'
"""

import dataclasses
from typing import Iterator, Tuple, Union


@dataclasses.dataclass(frozen=True, repr=True, eq=True)
class ProductId:
    vendor: int
    product: int

    @property
    def text(self) -> str:
        return f"{self.vendor:04X}:{self.product:04X}"

    @staticmethod
    def parse(product: str) -> "ProductId":
        """
        Example 'product': "0bda:5411"
        """
        v, p = product.split(":", 2)
        return ProductId(vendor=int(v, base=16), product=int(p, base=16))


@dataclasses.dataclass
class ChipPath:
    """
    A USB hub chip and its downstream path
    """

    product_id: ProductId
    path: Tuple[int, ...]

    def __post_init__(self):
        assert isinstance(self.product_id, ProductId)
        assert isinstance(self.path, tuple)

    @property
    def text(self) -> str:
        return f"{','.join(map(str,self.path))}-{self.product_id.text}"

    def is_top_path(self, sub_path: "ChipPath") -> bool:
        assert isinstance(sub_path, ChipPath)
        assert len(sub_path.path) == 0
        return self.product_id == sub_path.product_id

    def equals(self, solution_path: "ChipPath", path: "ChipPath") -> bool:
        assert isinstance(solution_path, ChipPath)
        assert isinstance(path, ChipPath)
        if self.product_id != path.product_id:
            return False
        full_path = solution_path.path + path.path
        return self.path == full_path


@dataclasses.dataclass
class Structure:
    list_chip_path: List[ChipPath]

    def __post_init__(self):
        self.list_chip_path.sort(key=lambda chip_path: chip_path.path)

    def find_solutions(self, real_usb_structure: "Structure") -> List[ChipPath]:
        """
        'self' is the hub structure.
        'real_usb_structure' is the structure connected to the PC.
        """

        def try_solution(i_candidate: int) -> ChipPath:
            for i, path in enumerate(self.list_chip_path):
                try:
                    candiate = real_usb_structure.list_chip_path[i_candidate + i]
                except IndexError:
                    return None
                if i == 0:
                    if not candiate.is_top_path(path):
                        return None
                    solution_path = candiate
                    continue

                if not candiate.equals(solution_path, path):
                    return None

            return solution_path

        def iter_solution() -> Iterator[ChipPath]:
            for i_candidate in range(len(real_usb_structure.list_chip_path)):
                solution_path = try_solution(i_candidate=i_candidate)
                if solution_path is not None:
                    yield solution_path
                    continue

        return list(iter_solution())


@dataclasses.dataclass
class Chip:
    """
    A USB Hub chip.
    There is exactly one upstream port and typically 4 downstream ports.
    Every downstram port is connected to a downstream usb hub chip or to
    a plug on the 'Hub'.
    """

    product: str
    plug_or_chip: tuple[Union[int, "Chip"], ...]

    product_id: ProductId = None

    def __post_init__(self) -> None:
        self.product_id = ProductId.parse(self.product)
        assert isinstance(self.plug_or_chip, tuple)
        for port in self.plug_or_chip:
            assert isinstance(port, (int, Chip))

    def _register(self, hub: "Hub", path: list[int]) -> None:
        for port_number0, plug_or_chip in enumerate(self.plug_or_chip):
            _path = path + [port_number0 + 1]
            if isinstance(plug_or_chip, int):
                hub._register_plug(Plug(plug=plug_or_chip, path=_path))
                continue

            assert isinstance(plug_or_chip, Chip)
            plug_or_chip._register(hub, _path)


@dataclasses.dataclass
class Plug:
    plug: int
    path: list[int]


@dataclasses.dataclass
class Hub:
    """
    A Hub consists of one more more 'Chips'.
    """

    manufacturer: str
    model: str
    plug_count: int
    chip: Chip

    _dict_plugs: Dict[int, Plug] = dataclasses.field(default_factory=dict)
    """
    The key is the plug number (starting from 1).
    """

    def __post_init__(self) -> None:
        assert isinstance(self.manufacturer, str)
        assert isinstance(self.model, str)
        assert isinstance(self.plug_count, int)
        assert isinstance(self.chip, Chip)

        self.chip._register(self, path=[])

        sorted_ports = sorted(self._dict_plugs.keys())
        if len(sorted_ports) != self.plug_count:
            raise ValueError(
                f"Expected {self.plug_count} plugs, but only {len(sorted_ports)} plugs have been defined: {sorted_ports}"
            )

        for port0, port in enumerate(sorted_ports):
            if port0 + 1 != port:
                raise ValueError(
                    f"Not all ports from 1 to {self.plug_count} have been defined: {sorted_ports}"
                )

    def _register_plug(self, plug: Plug) -> None:
        assert plug.plug not in self._dict_plugs
        self._dict_plugs[plug.plug] = plug

    def get_plug(self, plug_number: int) -> Plug:
        return self._dict_plugs[plug_number]

    @property
    def hub_tree(self) -> Structure:
        list_chip_path: list[ChipPath] = []

        def downstream(chip: "Chip", path: tuple[int, ...]) -> None:
            list_chip_path.append(ChipPath(product_id=chip.product_id, path=path))
            for port_number0, plug_or_chip in enumerate(chip.plug_or_chip):
                if isinstance(plug_or_chip, Chip):
                    _path = path + (port_number0 + 1,)
                    downstream(plug_or_chip, _path)

        downstream(self.chip, path=())

        return Structure(list_chip_path)

    @property
    def hub_tree2(self) -> list[str]:
        return [chip_path.text for chip_path in self.hub_tree.list_chip_path]

    def __repr__(self) -> str:
        return f"USB Hub '{self.model}' with {self.plug_count} plugs"


hub_rsh_a11pd = Hub(
    manufacturer="RSHTECH",
    model="RSH-A11PD",
    plug_count=16,
    chip=Chip(
        "0bda:5411",
        plug_or_chip=(
            1,
            2,
            Chip(
                "0bda:5411",
                plug_or_chip=(
                    7,
                    8,
                    Chip("0bda:5411", plug_or_chip=(9, 10, 11, 12)),
                    Chip("0bda:5411", plug_or_chip=(13, 14, 15, 16)),
                ),
            ),
            Chip("0bda:5411", plug_or_chip=(3, 4, 5, 6)),
        ),
    ),
)


y = (
    ("", "0bda:5411"),
    ("3", "0bda:5411"),
    ("3,3", "0bda:5411"),
    ("3,4", "0bda:5411"),
    ("4", "0bda:5411"),
)


print(hub_rsh_a11pd)
print(hub_rsh_a11pd.get_plug(14))  # 3,4,2
print(hub_rsh_a11pd.get_plug(3))  # 4,1
print(hub_rsh_a11pd.hub_tree2)

effective_structure = Structure(
    [
        ChipPath(ProductId.parse("05E3:0626"), (3,)),
        ChipPath(ProductId.parse("0BDA:0411"), (3, 1)),
        ChipPath(ProductId.parse("0BDA:0411"), (3, 1, 3)),
        ChipPath(ProductId.parse("0BDA:0411"), (3, 1, 3, 3)),
        ChipPath(ProductId.parse("0BDA:0411"), (3, 1, 3, 4)),
        ChipPath(ProductId.parse("0BDA:0411"), (3, 1, 4)),
        ChipPath(ProductId.parse("05E3:0610"), (6,)),
        ChipPath(ProductId.parse("0BDA:5411"), (6, 1)),
        ChipPath(ProductId.parse("0BDA:5411"), (6, 1, 3)),
        ChipPath(ProductId.parse("0BDA:5411"), (6, 1, 3, 3)),
        ChipPath(ProductId.parse("0BDA:5411"), (6, 1, 3, 4)),
        ChipPath(ProductId.parse("0BDA:5411"), (6, 1, 4)),
    ]
)

connected_hubs = hub_rsh_a11pd.hub_tree.find_solutions(effective_structure)
print(connected_hubs)
