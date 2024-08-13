"""
Summary: this implementation is not ready to read sr files.

"""

import configparser
import pathlib
from sigrokdecode import srzip


class SrZipInputHans(srzip.SrZipInput):
    def get_logic_values(self, samplenum):
        metadata = configparser.ConfigParser()
        metadata.read_string(self.zip.read("metadata").decode("ascii"))
        total_logic = int(metadata.get("device 1", "total probes", fallback="0"))
        total_analog = int(metadata.get("device 1", "total analog", fallback="0"))

        self._logic_data = []
        for c in range(total_logic):
            self._logic_data.append(self.zip.read(f"logic-1-{c+1}"))

        self._logic_offset = 0
        self._logic_chunk_len = len(self._analog_data[0]) // 4
        if samplenum >= (self._logic_offset + self._logic_chunk_len):
            self._logic_offset += self._logic_chunk_len
            self._analog_file_index += 1
            self._analog_data = []
            total_logic = len(self.logic_channels)
            total_analog = len(self.analog_channels)
            for c in range(total_logic + 1, total_logic + 1 + total_analog):
                self._analog_data.append(
                    self.zip.read(f"analog-1-{c}-{self._analog_file_index}")
                )
            self._logic_chunk_len = len(self._analog_data[0]) // 4

        values = []
        for data in self._analog_data:
            values.append(
                struct.unpack_from("f", data, (samplenum - self._logic_offset) * 4)[0]
            )

        return values


DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent
FILENAME_SR = DIRECTORY_OF_THIS_FILE / "specific_dump" / "2xds18b20.sr"
sr = SrZipInputHans(FILENAME_SR)
print(f"{sr.samplenum=}")
print(f"{sr.samplerate=}")
print(f"{sr.unitsize=}")
print(f"{sr.typecode=}")
print(f"{sr.logic_channels=}")
print(f"{sr.analog_channels=}")
print(f"{sr.bit_mapping=}")
print(f"{sr.data=}")

sr.get_logic_values(samplenum=100)
