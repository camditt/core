"""Fan support for switch entities."""
from __future__ import annotations

from homeassistant.components.fan import FanEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import BaseToggleEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize Fan Switch config entry."""
    registry = er.async_get(hass)
    entity_id = er.async_validate_entity_id(
        registry, config_entry.options[CONF_ENTITY_ID]
    )
    wrapped_switch = registry.async_get(entity_id)
    device_id = wrapped_switch.device_id if wrapped_switch else None

    async_add_entities(
        [
            FanSwitch(
                config_entry.title,
                entity_id,
                config_entry.entry_id,
                device_id,
            )
        ]
    )


class FanSwitch(BaseToggleEntity, FanEntity):
    """Represents a Switch as a Fan."""

    @property
    def is_on(self) -> bool | None:
        """Return true if the entity is on.

        Fan logic uses speed percentage or preset mode to determine
        its it on or off, however, when using a wrapped switch, we
        just use the wrapped switch's state.
        """
        return self._attr_is_on

    # pylint: disable=arguments-differ
    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs,
    ) -> None:
        """Turn on the fan.

        Arguments of the turn_on methods fan entity differ,
        thus we need to override them here.
        """
        await super().async_turn_on()
