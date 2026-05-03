"""Config flow for Hello World integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

from .const import (  # pylint:disable=unused-import
    CONFIG_PASSWORD,
    CONFIG_USERNAME,
    DOMAIN,
)
from .hub import Hub

_LOGGER = logging.getLogger(f"{DOMAIN}.config_flow")

# This is the schema that used to display the UI to the user. This simple
# schema has a single required host field, but it could include a number of fields
# such as username, password etc. See other components in the HA core code for
# further examples.
# Note the input displayed to the user will be translated. See the
# translations/<lang>.json file and strings.json. See here for further information:
# https://developers.home-assistant.io/docs/config_entries_config_flow_handler/#translations
# At the time of writing I found the translations created by the scaffold didn't
# quite work as documented and always gave me the "Lokalise key references" string
# (in square brackets), rather than the actual translated value. I did not attempt to
# figure this out or look further into it.
DATA_SCHEMA = vol.Schema(
    {
        (CONFIG_USERNAME): str,
        (CONFIG_PASSWORD): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """
    Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    username = data[CONFIG_USERNAME]
    password = data[CONFIG_PASSWORD]

    hub = Hub(hass)
    await hub.verify_credentials(username, password)

    return {"title": hub.name}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1

    def is_matching(self, _other_flow: config_entries.ConfigFlow) -> bool:
        """Check if the provided input matches this config flow."""
        return True

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        # This goes through the steps to take the user through the setup process.
        # Using this it is possible to update the UI and prompt for additional
        # information. This example provides a single form (built from `DATA_SCHEMA`),
        # and when that has some validated input, it calls `async_create_entry` to
        # actually create the HA config entry. Note the "title" value is returned by
        # `validate_input` above.
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONFIG_USERNAME])
            self._abort_if_unique_id_configured()
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including
        # any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
