from pyhubctl.known_hubs import rsh_a10, rsh_st07c

from octoprobe.config.config_tentacles import (
    tentacle_type_pyboard,
    tentacle_type_seed_pico,
)

from octoprobe.lib_tentacle import Tentacle, UsbHub
from octoprobe.lib_infrastructure import Infrastructure

hub = UsbHub(
    label="Hub A",
    model=rsh_st07c,
)

tentacle_pyboard = Tentacle(
    infra_rp2_unique_id="E463541647612835",
    tentacle_type=tentacle_type_pyboard,
    plug_infra=hub.get_plug(4),
    plug_dut=hub.get_plug(5),
)
tentacle_seed_pico = Tentacle(
    infra_rp2_unique_id="E463541647173F34",
    tentacle_type=tentacle_type_seed_pico,
    plug_infra=hub.get_plug(6),
    plug_dut=hub.get_plug(7),
)


INFRASTRUCTURE = Infrastructure(
    tentacles=[
        tentacle_pyboard,
        tentacle_seed_pico,
    ],
    hubs=[hub],
)
