"""Sensors that add informational properties to tracker devices."""

from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN
from .hub import Hub, Tracker


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    hub: Hub = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    for device in hub.devices:
        tracker = hub.devices[device]
        new_devices.append(LastSeenTimeSensor(tracker))
        new_devices.append(ModemTemperatureSensor(tracker))
        new_devices.append(ModemVoltageSensor(tracker))
        new_devices.append(DeviceTypeSensor(tracker))
        new_devices.append(OperatingModeSensor(tracker))
        new_devices.append(ReportingIntervalSensor(tracker))
        new_devices.append(ReportedAddressSensor(tracker))
        new_devices.append(BatteryPercentSensor(tracker))

    if new_devices:
        async_add_entities(new_devices)


class SensorBase(Entity):
    """Base class for all sensors in this module."""

    _tracker: Tracker

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._attr_has_entity_name = True
        self._tracker = tracker

    # To link this entity to the cover device, this property must return an
    # identifiers value matching that used in the cover, but no other information such
    # as name. If name is returned, this entity will then also become a device in the
    # HA UI.
    @property
    def device_info(self) -> DeviceInfo:
        """Return information to link this entity with the correct device."""
        return self._tracker.build_device_info(False)


class LastSeenTimeSensor(SensorBase):
    """Provides the last seen time for a GPS tracker."""

    device_class: SensorDeviceClass = SensorDeviceClass.TIMESTAMP

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_last_seen"
        self._attr_name = "Last Seen"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.last_report_time.ctime()


class ModemTemperatureSensor(SensorBase):
    """Provides the last modem temperature for a GPS tracker."""

    device_class: SensorDeviceClass = SensorDeviceClass.TEMPERATURE
    _attr_unit_of_measurement = UnitOfTemperature.FAHRENHEIT

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_modem_temperature"
        self._attr_name = "Modem Temperature"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.modem_temperature


class ModemVoltageSensor(SensorBase):
    """Provides the last modem voltage for a GPS tracker."""

    device_class: SensorDeviceClass = SensorDeviceClass.VOLTAGE
    _attr_unit_of_measurement = "V"

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_modem_voltage"
        self._attr_name = "Modem Voltage"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return (
            self._tracker.modem_voltage / 1000 if self._tracker.modem_voltage else None
        )

class DeviceTypeSensor(SensorBase):
    """Provides the device type for a GPS tracker."""

    device_class: SensorDeviceClass = SensorDeviceClass.ENUM

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_device_type"
        self._attr_name = "Device Type"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.device_type.replace("_", " ").title()

class OperatingModeSensor(SensorBase):
    """Provides the operating mode for a GPS tracker."""

    device_class: SensorDeviceClass = SensorDeviceClass.ENUM

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_operating_mode"
        self._attr_name = "Operating Mode"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.operating_mode.title()

class ReportingIntervalSensor(SensorBase):
    """Provides the reporting interval for a GPS tracker."""

    device_class: SensorDeviceClass = SensorDeviceClass.DURATION
    _attr_unit_of_measurement = "s"

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_reporting_interval"
        self._attr_name = "Reporting Interval"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.reporting_interval

class ReportedAddressSensor(SensorBase):
    """Provides the reported address for a GPS tracker."""

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_reported_address"
        self._attr_name = "Reported Address"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.address


class BatteryPercentSensor(SensorBase):
    """Provides the battery percentage for a GPS tracker."""

    device_class: SensorDeviceClass = SensorDeviceClass.BATTERY
    _attr_unit_of_measurement = "%"

    # these figures are guesses based on observed data
    V0 = 3.65 # 3.7 = 10%
    Vmax = 4.17

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_battery_percent"
        self._attr_name = "Battery Percent"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return round(
            ((self._tracker.modem_voltage / 1000) - BatteryPercentSensor.V0)
            / (BatteryPercentSensor.Vmax - BatteryPercentSensor.V0)
            * 100,
            0,
        )
