# ToggleMinimapOnScroll

If you like the idea of Sublime Text 2's minimap, but don't like the screen real estate it takes up, then this package is for you.

ToggleMinimapOnScroll toggles the minimap on when you're scrolling and toggles it off when you're not scrolling, after a user-configurable duration.

Note that, since the minimap can only be programmatically toggled and the state of the minimap isn't programmatically available, you have to manually toggle the minimap off, before scrolling, for ToggleMinimapOnScroll to have the intended effect.

## Installation

Install via [Sublime Package Control](http://wbond.net/sublime_packages/package_control).

## Usage

Manually toggle the minimap off, before scrolling, for ToggleMinimapOnScroll to have the intended effect.

## Settings

ToggleMinimapOnScroll's settings are accessed via the Preferences->Package Settings->ToggleMinimapOnScroll menu.

ToggleMinimapOnScroll is enabled by default. To disable it by default, set the following variable to false:

    "toggle_minimap_on_scroll_by_default": true

ToggleMinimapOnScroll toggles the minimap off after 2.5 seconds by default. Use the following variable to configure this duration:

    "toggle_minimap_on_scroll_duration_seconds": 2.5

ToggleMinimapOnScroll takes 7.5 samples per second to detect scroll by default. Use the following variable to configure this sampling frequency:

    "viewport_position_samples_per_second": 7.5

ToggleMinimapOnScroll can be configured to be activated on cursor line changes by setting the following variable to true:

    "toggle_minimap_on_cursor_line_changed": false

ToggleMinimapOnScroll can be configured to be activated on view changes by setting the following variable to true:

    "toggle_minimap_on_cursor_line_changed": false

## Commands

ToggleMinimapOnScroll can be disabled/enabled through the command palette.
