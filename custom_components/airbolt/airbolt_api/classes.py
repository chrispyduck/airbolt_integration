"""Datatypes used in Airbolt API responses."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


UpdateType = Literal["Motion", "SOS", "Schedule", "Location", "CMD"]


class UserInfo(BaseModel):
    """Information about a user."""

    id: str = Field(alias="_id")
    username: str
    time_created: datetime = Field(alias="timeCreated")
    name: str
    email: str
    roles: list[str]
    failed_login_attempts: int = Field(alias="failedLoginAttempts")
    two_factor_enabled: bool = Field(alias="twoFactorEnabled")
    profile_picture: str = Field(alias="profilePicture")
    blocked_until: str | None = Field(alias="blockedUntil")
    country: str
    currency: str
    timezone: str
    deleted: bool
    cell_scan_limit: int = Field(alias="cellScanLimit")


class SessionInfo(BaseModel):
    """Information about the current API session."""

    id: str = Field(alias="_id")
    user_id: str = Field(alias="userId")
    key: str
    time: datetime
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    v: int = Field(alias="__v")


class LoginResult(UserInfo):
    """The result of a login call."""

    session: SessionInfo
    auth_header: str = Field(alias="authHeader")


class TemperatureConfiguration(BaseModel):
    """Configuration of a tracker's temperature reporting and alerting."""

    enable: bool
    send_location: bool = Field(alias="sendLocation")
    realert_duration: int = Field(alias="reAlertDuration")
    condition: Literal["lessOrEqual"]
    level: int
    unit: Literal["f", "c"]


class AccelerometerConfiguration(BaseModel):
    """Configuration of a tracker's accelerometer reporting and alerting."""

    enable: bool
    ultra_power_mode: bool = Field(alias="ultraPowerMode")
    send_location: bool = Field(alias="sendLocation")
    sensitivity: int
    """Sensitivity value from 1-10, where 1 is the most sensitive and 10 is the least"""
    duration: int


class WaterAlarmConfiguration(BaseModel):
    """Configuration of a tracker's water alarm reporting and alerting."""

    enable: bool
    send_location: bool = Field(alias="sendLocation")
    realert_duration: int = Field(alias="reAlertDuration")


class ESIM(BaseModel):
    """Read-only information about the tracker's eSIM."""

    id: str = Field(alias="_id")
    iccid: str
    eid: str
    status: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class DeviceSubscription(BaseModel):
    """Subscription information for a tracker."""

    status: str


class FoundDevice(BaseModel):
    """A device reported by the API."""

    accelerometer: AccelerometerConfiguration
    alarm: bool
    alert_level: int = Field(alias="alertLevel")
    color: str | None
    deleted: bool
    device_type: Literal["shield_gps"] = Field(
        alias="deviceType"
    )  # TODO: figure out other types
    id: str = Field(alias="_id")
    last_history_time: datetime = Field(alias="lastHistoryTime")
    latitude: float  # unused?
    longitude: float  # unused?
    mark_as_lost: int = Field(alias="markAsLost")
    modem_state: int
    modem_temperature_f: int
    modem_voltage: int
    operating_mode: Literal["batteryLife", "responsiveness"] = Field(
        alias="operatingMode"
    )
    schedule_report: list[Literal["gps", "temp", "cell"]] = Field(
        alias="scheduleReport"
    )
    schedule_report_interval: int = Field(alias="scheduleReportInterval")
    temperature: TemperatureConfiguration
    tone: int
    tsa_accessible: bool = Field(alias="tsaAccessible")
    water_alarm: WaterAlarmConfiguration = Field(alias="waterAlarm")

    location_report_mode: str = Field(
        alias="locationReportMode"
    )  # should be enum? found 'once'
    led_flash: bool = Field(alias="ledFlash")
    push_notification: bool = Field(alias="pushNotification")
    email_alerts: bool = Field(alias="emailAlerts")
    location_update_notification: bool = Field(alias="locationUpdateNotification")
    sos_alert_notification: bool = Field(alias="sosAlertNotification")

    notification_emails: list[str] = Field(alias="notificationEmails")
    emergency_mode: bool = Field(alias="emergencyMode")
    proximity: str  # found: 'medium'
    device_uuid: str = Field(alias="deviceUUID")
    device_picture: str = Field(alias="devicePicture")
    name: str
    time_created: datetime = Field(alias="timeCreated")
    last_seen_time: datetime = Field(alias="lastSeenTime")
    last_report_type: UpdateType = Field(alias="lastReportType")  # water?
    esim: ESIM
    imei: str
    iccid: str
    psm_active_time: int
    """Power Save Mode active time in seconds(?)"""
    psm_tau: int
    """Power Save Mode Tracking Area Update"""
    edrx_ptw: int
    """eDRX (extended discontinuous reception) Paging Time Window"""
    edrx_value: int
    """eDRX offline time multiplier?"""
    # unused fields:
    # {
    isTrialAvailed: bool
    rai_value: bool
    listenToLock: bool
    subscriptionRemindOn: datetime | None
    userId: str
    passcode: str
    markedByUsername: str
    markedByEmail: str
    masterKey: str
    outOfRangeTimeout: int | None
    subscriptionRemindCount: int | None
    cellRequestsCount: int
    cellRequestsResetOn: datetime
    continuousReportReset: datetime | None
    privilege: int
    sharedUserCount: int
    share_count: int
    subscription: DeviceSubscription
    cellScanLimit: int


class FoundDeviceList(BaseModel):
    """A list of devices reported by the API."""

    __root__: list[FoundDevice]


class HistoryEntry(BaseModel):
    """A data point representing a single update from a GPS tracker."""

    id: str = Field(alias="_id")
    device_uuid: str = Field(alias="deviceUUID")
    modem_voltage: int | None
    modem_temperature: int | None
    type: Literal["gps", "mcell", "scell"]
    time_created: datetime = Field(alias="timeCreated")
    latitude: float
    longitude: float
    accuracy: float
    location_changed: bool = Field(alias="locationChanged")
    duration: int
    alert_type: UpdateType = Field(alias="alertType")
    address: str
    last_seen_on: datetime = Field(alias="lastSeenOn")


class Pagination(BaseModel):
    """Pagination information for paged endpoints."""

    total: int
    """Total number of records"""

    total_pages: int = Field(alias="totalPages")
    """Total number of pages"""

    next: int
    """Next page number"""
    has_next: bool = Field(alias="hasNext")
    """Whether there's a next page"""

    prev: int
    """Previous page number"""
    has_prev: bool = Field(alias="hasPrev")
    """Whether there's a previous page"""

    per_page: int = Field(alias="perPage")
    """Page size"""

    current: int
    """Current page number"""


class DeviceHistoryPage(BaseModel):
    """A single page of the request history endpoint."""

    success: bool
    data: list[HistoryEntry]
    pagination: Pagination
