# Driver for the MCP9808 Temperature Sensor
from machine import I2C

_MCP9808_TUPPER_REG = 0x02
_MCP9808_TLOWER_REG = 0x03
_MCP9808_TCRIT_REG  = 0x04
_MCP9808_TAMB_REG   = 0x05
_MCP9808_MAN_ID_REG = 0x06
_MCP9808_DEV_ID_REG = 0x07
_MCP9808_SLAVEADDR  = 0x18

class MCP9808:
    def __init__(self, i2c_bus='X'):
        try:
            self.sensor = I2C(i2c_bus, freq=400000)
            # Verify manufacturer id to ensure the communcation
            # is done to the right device
            manufacturerId = self.sensor.readfrom_mem(_MCP9808_SLAVEADDR, _MCP9808_MAN_ID_REG, 2)
            ok = manufacturerId[0] == 0 and manufacturerId[1] == 0x54

            deviceId = self.sensor.readfrom_mem(_MCP9808_SLAVEADDR,
                                                _MCP9808_DEV_ID_REG, 2)
            if not ok or deviceId[0] != 0x04:
                raise ValueError("Unable to find MCP9808 at I2C address 0x{:02X}".format(_MCP9808_SLAVEADDR))
        except:
            print("It seems there's no sensor device connected to the I2C bus!")

    def getAmbientTemperature(self):
        data = self.sensor.readfrom_mem(_MCP9808_SLAVEADDR, _MCP9808_TAMB_REG, 2)
        MSB = data[0]
        LSB = data[1]

        MSB = MSB & 0x1F        # Clear flags
        if ((MSB & 0x10) == 0x10):
            MSB = MSB & 0x0F    # Clear sign
            temperature = 256 - (MSB * 16 + LSB / 16)
        else:
            temperature = (MSB * 16 + LSB / 16)
        return temperature

    def getUpperTemperatureLimit(self):
        data = self.sensor.readfrom_mem(_MCP9808_SLAVEADDR, _MCP9808_TUPPER_REG, 2)
        MSB = data[0]
        LSB = data[1]

        if ((MSB & 0x10) == 0x10):
            MSB = MSB & 0x0F    # Clear sign
            temperature = 256 - (MSB * 16 + LSB / 16)
        else:
            temperature = (MSB * 16 + LSB / 16)
        return temperature
