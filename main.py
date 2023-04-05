from ROCv3 import ROCv3
from VirtualROCv3 import VirtualROCv3
from utils import *

# Create a virtual ROC and then pass it to the SWAMP roc as transport and pass the
# virtual reset pin to the swamp object as reset pin
virtual_roc = VirtualROCv3('HGCROC3_I2C_params_regmap.csv', 'virtualROCv3_register_state.csv')

swamp_roc = ROCv3(transport=virtual_roc,
                  base_address=0,
                  name='test_roc',
                  reset_pin=virtual_roc.reset_pin,
                  path_to_file=virtual_roc.path_to_registers_map)


# To be able to use it we need a configuration that can be written to our 'virtual ROC'.
configuration = load_yaml('roc_test_config.yml')

swamp_roc.reset()

swamp_roc.read(configuration, from_hardware=True)

# swamp_roc.configure(configuration)

# swamp_roc.read(configuration, from_hardware=True)
