# ToggleMinimapOnScroll

If you like the idea of Sublime Text's minimap, but don't like the screen real estate it takes up, then this package is for you.

ToggleMinimapOnScroll toggles the minimap on when you're scrolling and toggles it off when you're not scrolling, after a user-configurable duration.

Note that, since the minimap can only be programmatically toggled and the state of the minimap isn't programmatically available, you have to manually toggle the minimap off, before scrolling, for ToggleMinimapOnScroll to have the intended effect.

## Installation

Install via [Sublime Package Control](http://wbond.net/sublime_packages/package_control).

## Usage

Manually toggle the minimap off, before scrolling, for ToggleMinimapOnScroll to have the intended effect.

The following pseudocode outlines the behavior states:

    if ToggleMinimapOnScroll is enabled:
        if minimap is shown:
            minimap is hidden when scrolling
        if minimap is hidden:
            minimap is shown when scrolling
    if ToggleMinimapOnScroll is disabled:
        minimap has default behavior

## Commands

ToggleMinimapOnScroll can be disabled/enabled via the command palette.

Use the following command to disable ToggleMinimapOnScroll:

    View: Disable ToggleMinimapOnScroll

Use the following command to enable ToggleMinimapOnScroll:

    View: Enable ToggleMinimapOnScroll

## Settings

ToggleMinimapOnScroll's settings can be accessed via the Preferences->Package Settings->ToggleMinimapOnScroll menu.

ToggleMinimapOnScroll is enabled by default. To disable it by default, set the following variable to false:

    "toggle_minimap_on_scroll_enabled_by_default": true

ToggleMinimapOnScroll toggles the minimap off after 2.5 seconds by default. Use the following variable to configure this duration:

    "toggle_minimap_on_scroll_duration_in_seconds": 2.5

ToggleMinimapOnScroll takes 7.5 samples per second to detect scrolling by default. Use the following variable to configure this sampling frequency:

    "toggle_minimap_on_scroll_samples_per_second": 7.5

ToggleMinimapOnScroll can be configured to be activated on vertical scroll only by setting the following variable to true:

    "toggle_minimap_on_vertical_scroll_only": false

ToggleMinimapOnScroll can be configured to be activated on cursor line changes by setting the following variable to true:

    "toggle_minimap_on_cursor_line_changed": false

ToggleMinimapOnScroll can be configured to be activated on view changes by setting the following variable to true:

    "toggle_minimap_on_view_changed": false

## Contact

Maintainer: Jerome Castaneda &lt;djjcast@gmail.com&gt;

URL: https://github.com/djjcast/sublime-ToggleMinimapOnScroll

## License

The MIT License (MIT)

Copyright (c) 2013 Jerome Castaneda &lt;djjcast@gmail.com&gt;

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
