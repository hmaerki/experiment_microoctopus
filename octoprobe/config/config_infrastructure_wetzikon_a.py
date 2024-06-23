from usbhubctl.known_hubs import octohub4

from octoprobe.config.config_tentacles import (
    tentacle_type_pyboard,
    tentacle_type_seed_pico,
)
from octoprobe.lib_infrastructure import Infrastructure
from octoprobe.lib_tentacle import Tentacle, UsbHub

hub = UsbHub(
    label="Hub A",
    model=octohub4,
    model=rsh_a10,
)

tentacle_pyboard = Tentacle(
    infra_rp2_unique_id="E463541647612835",
    tentacle_type=tentacle_type_pyboard,
    plug_infra=hub.get_plug(1),
    plug_dut=hub.get_plug(2),
)
tentacle_seed_pico = Tentacle(
    infra_rp2_unique_id="E463541647173F34",
    tentacle_type=tentacle_type_seed_pico,
    plug_infra=hub.get_plug(3),
    plug_dut=hub.get_plug(4),
)


INFRASTRUCTURE = Infrastructure(
    tentacles=[
        tentacle_seed_pico,
        tentacle_pyboard,
    ],
    hubs=[hub],
)
