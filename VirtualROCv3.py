import os
import csv
import pandas as pd
from typing import Union
from VirtualGPIOPin import VirtualGPIOPin


# This is the virtual ROC class. It creates a virtual reset pin upon construction
# and provides the SWAMP compatible 'write', 'read', and 'reset' functions calls
class VirtualROCv3:
    def __init__(self, path_to_registers_map, path_to_registers_state):
        self.path_to_registers_map = path_to_registers_map
        self.path_to_registers_state = path_to_registers_state
        self.reset_pin = VirtualGPIOPin(self.reset, mode='active_low')
        self.cache = {}
        self._cache = [0, 0, 0]

        # read in source of truth of the ROCv3 configuration
        self.config_table = pd.read_csv(path_to_registers_map)

        if not os.path.isfile(self.path_to_registers_state):
            self.reset()

    def write(self, address: int, value: Union[int, bytearray]) -> None:
        """
        Writes values to file and virtual ROC cache

        :param address: Address of the register to write to
        :param value: Value to write to the register
        """
        self._cache[address] = value
        if address == 2:
            self.cache[(self._cache[0], self._cache[1])] = self._cache[2]
            print(f"Wrote the value {self._cache[2]} to address {self._cache[0], self._cache[1]}")

            register_table = pd.read_csv(self.path_to_registers_state)
            register_table.loc[(register_table.R0 == self._cache[0]) &
                               (register_table.R1 == self._cache[1]), 'R2'] = self._cache[2]
            register_table.to_csv(self.path_to_registers_state)

    def read(self, address: Union[int, bytearray], from_hardware: bool) -> int:
        """
        Reads register values from cache or file

        :param address: Address of the register to write to
        :param from_hardware: Set to skip cache and read directly
            from file
        :return: The value read from register cache/file
        """

        if address == 2:
            if from_hardware:
                register_table = pd.read_csv(self.path_to_registers_state)
                r2 = int(register_table.loc[(register_table.R0 == self._cache[0]) &
                                            (register_table.R1 == self._cache[1]), 'R2'])
                print(f"Read the value {r2} from address {self._cache[0], self._cache[1]}")
                return r2
            else:
                print(f"Read the value {self.cache[(self._cache[0], self._cache[1])]}\
                    from CACHE address {self._cache[0], self._cache[1]}")
                return self.cache[(self._cache[0], self._cache[1])]
        else:
            print(f"Read the value {self._cache[address]} from R{address}")
        return self._cache[address]

    def initialize_cache(self) -> None:
        """
        Initializes the cache with defval from regmap
        """

        # generate the default state for the cache
        keys = self.config_table[['R0', 'R1']].drop_duplicates()
        for _, key in keys.iterrows():
            self.cache[(key['R0'], key['R1'])] = 0

        # turn the bits of the different defval_masks on
        for _, row in self.config_table.iterrows():
            self.cache[(row['R0'], row['R1'])] |= row['defval_mask']

    def write_cache_to_file(self) -> None:
        """
        Writes cached values to file
        """

        with open(self.path_to_registers_state, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["R0", "R1", "R2"])
            for key, value in self.cache.items():
                writer.writerow([str(key[0]), str(key[1]), str(value)])

    def reset(self) -> None:
        """
        Initializes the cache and writes it to file
        """

        self.initialize_cache()
        self.write_cache_to_file()
