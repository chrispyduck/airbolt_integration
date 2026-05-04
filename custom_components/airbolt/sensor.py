"""Sensors that add informational properties to tracker devices."""

from typing import TYPE_CHECKING

from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.const import EntityCategory, UnitOfTemperature
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.device_registry import DeviceInfo
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import StateType

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
        new_devices.append(AccelerometerEnabledSensor(tracker))
        new_devices.append(AccelerometerUltraPowerModeSensor(tracker))
        new_devices.append(AccelerometerSendLocationSensor(tracker))
        new_devices.append(AccelerometerSensitivitySensor(tracker))
        new_devices.append(AccelerometerDurationSensor(tracker))
        new_devices.append(SubscriptionStatusSensor(tracker))
        new_devices.append(LastReportTypeSensor(tracker))
        new_devices.append(CellRequestsCountSensor(tracker))
        new_devices.append(ESIMICCIDSensor(tracker))
        new_devices.append(ESIMEIDSensor(tracker))
        new_devices.append(ESIMStatusSensor(tracker))

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
        return self._tracker.build_device_info(parent=False)


class LastSeenTimeSensor(SensorBase):
    """Provides the last seen time for a GPS tracker."""

    _attr_icon = "mdi:clock-check"
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

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:thermometer"
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

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:flash"
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

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:tag"
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

    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:cog"
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

    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:timer"
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

    _attr_icon = "mdi:map-marker"

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

    _attr_icon = "mdi:battery"
    device_class: SensorDeviceClass = SensorDeviceClass.BATTERY
    _attr_unit_of_measurement = "%"

    # these figures are guesses based on observed data
    V0 = 3.65  # 3.7 = 10%
    Vmax = 4.2  # LiPO maximum, corresponds to 100%

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_battery_percent"
        self._attr_name = "Battery Percent"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return min(
            100,
            round(
                ((self._tracker.modem_voltage / 1000) - BatteryPercentSensor.V0)
                / (BatteryPercentSensor.Vmax - BatteryPercentSensor.V0)
                * 100,
                0,
            ),
        )


class AccelerometerEnabledSensor(SensorBase):
    """Provides the accelerometer enabled state for a GPS tracker."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:vibrate"
    device_class: SensorDeviceClass = SensorDeviceClass.ENUM

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_accelerometer_enabled"
        self._attr_name = "Accelerometer Enabled"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return "on" if self._tracker.accelerometer.enable else "off"


class AccelerometerUltraPowerModeSensor(SensorBase):
    """Provides the accelerometer ultra power mode for a GPS tracker."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:power"
    device_class: SensorDeviceClass = SensorDeviceClass.ENUM

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_accelerometer_ultra_power_mode"
        self._attr_name = "Accelerometer Ultra Power Mode"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return "on" if self._tracker.accelerometer.ultra_power_mode else "off"


class AccelerometerSendLocationSensor(SensorBase):
    """Provides the accelerometer send location setting for a GPS tracker."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:crosshairs-gps"
    device_class: SensorDeviceClass = SensorDeviceClass.ENUM

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_accelerometer_send_location"
        self._attr_name = "Accelerometer Send Location"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return "on" if self._tracker.accelerometer.send_location else "off"


class AccelerometerSensitivitySensor(SensorBase):
    """Provides the accelerometer sensitivity for a GPS tracker."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:tune"

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_accelerometer_sensitivity"
        self._attr_name = "Accelerometer Sensitivity"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.accelerometer.sensitivity


class AccelerometerDurationSensor(SensorBase):
    """Provides the accelerometer duration for a GPS tracker."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:clock"
    device_class: SensorDeviceClass = SensorDeviceClass.DURATION
    _attr_unit_of_measurement = "s"

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_accelerometer_duration"
        self._attr_name = "Accelerometer Duration"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.accelerometer.duration


class SubscriptionStatusSensor(SensorBase):
    """Provides the subscription status for a GPS tracker."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:receipt"
    device_class: SensorDeviceClass = SensorDeviceClass.ENUM

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_subscription_status"
        self._attr_name = "Subscription Status"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.subscription_status


class LastReportTypeSensor(SensorBase):
    """Provides the type of last report for a GPS tracker."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:file-document"
    device_class: SensorDeviceClass = SensorDeviceClass.ENUM

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_last_report_type"
        self._attr_name = "Last Report Type"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.last_report_type


class CellRequestsCountSensor(SensorBase):
    """Provides the cell requests count for a GPS tracker."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:tower-cell"

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_cell_requests_count"
        self._attr_name = "Cell Requests Count"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.cell_requests_count

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return extra state attributes."""
        return {
            "reset_on": self._tracker.cell_requests_reset_on.isoformat(),
            "scan_limit": self._tracker.cell_scan_limit,
        }


class ESIMICCIDSensor(SensorBase):
    """Provides the eSIM ICCID for a GPS tracker."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:sim-card"
    _attr_entity_registry_enabled_default = False

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_esim_iccid"
        self._attr_name = "eSIM ICCID"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.esim_iccid

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return extra state attributes."""
        return {
            "updated_at": self._tracker.esim_updated_at.isoformat(),
        }


class ESIMEIDSensor(SensorBase):
    """Provides the eSIM EID for a GPS tracker."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:sim-card"
    _attr_entity_registry_enabled_default = False

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_esim_eid"
        self._attr_name = "eSIM EID"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.esim_eid

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return extra state attributes."""
        return {
            "updated_at": self._tracker.esim_updated_at.isoformat(),
        }


class ESIMStatusSensor(SensorBase):
    """Provides the eSIM status for a GPS tracker."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:sim-card-check"
    device_class: SensorDeviceClass = SensorDeviceClass.ENUM
    _attr_entity_registry_enabled_default = False

    def __init__(self, tracker: Tracker) -> None:
        """Initialize the sensor."""
        self._tracker = tracker
        self._attr_unique_id = f"{tracker.id}_esim_status"
        self._attr_name = "eSIM Status"
        super().__init__(tracker)

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self._tracker.esim_status

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return extra state attributes."""
        return {
            "updated_at": self._tracker.esim_updated_at.isoformat(),
        }
