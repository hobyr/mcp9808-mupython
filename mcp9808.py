# MicroPython Driver for the MCP9808 Temperature Sensor
# Datasheet: https://ww1.microchip.com/downloads/en/DeviceDoc/25095A.pdf

from machine import I2C

# Register addresses for configuration and access to readings/values
_MCP9808_TUPPER_REG = 0x02 # Alert Temperature Upper Boundary Trip register
_MCP9808_TLOWER_REG = 0x03 # Alert Temperature Lower Boundary Trip register
_MCP9808_TCRIT_REG  = 0x04 # Critical Temperature Trip register
_MCP9808_TAMB_REG   = 0x05 # Ambient Temperature register (Read-only)
_MCP9808_MAN_ID_REG = 0x06 # Manufacturer ID register
_MCP9808_DEV_ID_REG = 0x07 # Device ID/Revision register
_MCP9808_RESOL_REG  = 0x08 # Resolution register
_MCP9808_SLAVEADDR  = 0x18 # Address of the Sensor for the I2C bus

class MCP9808:
    """Interface to the MCP9808 temperature sensor."""

    def __init__(self, i2c_bus='Y'):
        try:
            self.sensor = I2C(i2c_bus, freq=400000)
            # Verify manufacturer id to ensure the communcation
            # is done to the right device
            manufacturerId = self.sensor.readfrom_mem(_MCP9808_SLAVEADDR, _MCP9808_MAN_ID_REG, 2)
            ok = manufacturerId[0] == 0 and manufacturerId[1] == 0x54

            deviceId = self.sensor.readfrom_mem(_MCP9808_SLAVEADDR, _MCP9808_DEV_ID_REG, 2)
            if not ok or deviceId[0] != 0x04:
                raise ValueError("Unable to find MCP9808 at I2C address 0x{:02X}".format(_MCP9808_SLAVEADDR))
        except:
            print("It seems there's no sensor device connected to the I2C bus!")


    def _getTemperature(self, register):
        """Retrieval of the temperature value in specified register in Celsius. Read-only."""
        data = self.sensor.readfrom_mem(_MCP9808_SLAVEADDR, register, 2)
        MSB = data[0]
        LSB = data[1]

        MSB = MSB & 0x1F   # Clear flags
        if ((MSB & 0x10) == 0x10):
            MSB = MSB & 0x0F    # Clear sign
            return 256 - (MSB * 16 + LSB / 16)
        else:
            return (MSB * 16 + LSB / 16)

    def _setTemperature(self, register, temperature):
        """Setting of the temperature value in specified register in Celsius.

        :register: TODO
        :temperature: TODO
        :returns: TODO

        """
        pass

    @property
    def getAmbientTemperature(self):
        """Current temperature in Celsius. Read-only property."""
        return self._getTemperature(_MCP9808_TAMB_REG)

    @property
    def getUpperTemperatureLimit(self):
        """Upper temperature limit in Celsius. Read-only."""
        return self._getTemperature(_MCP9808_TUPPER_REG)

    @property
    def getLowerTemperatureLimit(self):
        """Lower temperature limit in Celsius. Read-only."""
        return self._getTemperature(_MCP9808_TLOWER_REG)

    @property
    def getCriticalTemperatureLimit(self):
        """Critical temperature limit in Celsius. Read-only."""
        return self._getTemperature(_MCP9808_TCRIT_REG)

    def setUpperTemperatureLimit(self, temperature):
        """Setting of the upper temperature limit alert in Celsius."""
        pass

    def setLowerTemperatureLimit(self, temperature):
        """Setting of the lower temperature limit alert in Celsius."""
        pass

    def setCriticalTemperatureLimit(self, temperature):
        """Setting of the critical temperature limit alert in Celsius."""
        pass

