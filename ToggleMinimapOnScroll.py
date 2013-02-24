import sublime
import sublime_plugin
from threading import Thread, Lock
from time import sleep

def get_setting(name):
    settings = sublime.load_settings("ToggleMinimapOnScroll.sublime-settings")
    if name == "toggle_minimap_on_scroll_by_default":
        default = True
    elif name == "toggle_minimap_on_scroll_duration_seconds":
        default = 2.5
    elif name == "viewport_position_samples_per_second":
        default = 7.5
    elif name == "toggle_minimap_on_cursor_line_changed":
        default = False
    elif name == "toggle_minimap_on_view_changed":
        default = False
    return settings.get(name, default)

toggle_minimap_on_scroll_is_enabled = get_setting("toggle_minimap_on_scroll_by_default")
def plugin_loaded():
    global toggle_minimap_on_scroll_is_enabled
    toggle_minimap_on_scroll_is_enabled = get_setting("toggle_minimap_on_scroll_by_default")

ignore_events = False
ignore_count = 0
lock = Lock()

def untoggle_minimap(view):
    with lock:
        global ignore_events, ignore_count
        if ignore_events:
            view.window().run_command("toggle_minimap")
            ignore_count += 1
            ignore_events = False

def untoggle_minimap_on_timeout():
    with lock:
        global ignore_events, ignore_count
        if ignore_count:
            ignore_count -= 1
            return
        sublime.active_window().run_command("toggle_minimap")
        ignore_events = False

def toggle_minimap():
    with lock:
        global ignore_events, ignore_count
        if not ignore_events:
            sublime.active_window().run_command("toggle_minimap")
            ignore_events = True
        else:
            ignore_count += 1
        sublime.set_timeout(untoggle_minimap_on_timeout,
                            int(float(get_setting("toggle_minimap_on_scroll_duration_seconds")) * 1000))

def sample_viewport():
    if viewport_scrolled():
        toggle_minimap()

previous_viewport_position = None
previous_viewport_extent = None
def viewport_scrolled():
    global previous_viewport_position, previous_viewport_extent
    viewport_scrolled = False
    viewport_position = sublime.active_window().active_view().viewport_position()
    viewport_extent = sublime.active_window().active_view().viewport_extent()
    if viewport_position != previous_viewport_position and viewport_extent == previous_viewport_extent:
        viewport_scrolled = True
    previous_viewport_position = viewport_position
    previous_viewport_extent = viewport_extent
    return viewport_scrolled

class ViewportMonitor(Thread):
    sample_period = 1 / 7.5

    def run(self):
        while True:
            if toggle_minimap_on_scroll_is_enabled:
                sublime.set_timeout(sample_viewport, 0)
            sublime.set_timeout(self.get_viewport_position_samples_per_second, 0)
            sleep(self.sample_period)

    def get_viewport_position_samples_per_second(self):
        self.sample_period = 1 / float(get_setting("viewport_position_samples_per_second"))
if not "viewport_monitor" in globals():
    viewport_monitor = ViewportMonitor()
    viewport_monitor.start()

class EventListener(sublime_plugin.EventListener):
    startup_events_completed = False  # ignore startup events (Sublime Text 2)
    previous_selection_begin_row = None
    previous_selection_end_row = None
    previous_num_selection = None

    def on_selection_modified(self, view):
        if not view.window():  # ignore startup events (Sublime Text 2)
            return
        if not self.startup_events_completed:  # ignore startup events (Sublime Text 2)
            self.startup_events_completed = True
            return
        if toggle_minimap_on_scroll_is_enabled and \
           get_setting("toggle_minimap_on_cursor_line_changed") and \
           self.cursor_line_changed(view):
            toggle_minimap()

    def cursor_line_changed(self, view):
        cursor_line_changed = False
        selection_begin_row = view.rowcol(view.sel()[0].begin())[0]
        selection_end_row = view.rowcol(view.sel()[0].end())[0]
        num_selection = len(view.sel())
        if selection_begin_row != self.previous_selection_begin_row or \
            selection_end_row != self.previous_selection_end_row or \
            num_selection != self.previous_num_selection:
            cursor_line_changed = True
        self.previous_selection_begin_row = selection_begin_row
        self.previous_selection_end_row = selection_end_row
        self.previous_num_selection = num_selection
        return cursor_line_changed

    def on_activated(self, view):
        if not self.startup_events_completed:  # ignore startup events (Sublime Text 2)
            return
        if toggle_minimap_on_scroll_is_enabled and get_setting("toggle_minimap_on_view_changed"):
            toggle_minimap()

    def on_deactivated(self, view):
        untoggle_minimap(view)

    def on_close(self, view):
        untoggle_minimap(view)

class DisableToggleMinimapOnScroll(sublime_plugin.WindowCommand):
    def run(self):
        global toggle_minimap_on_scroll_is_enabled
        toggle_minimap_on_scroll_is_enabled = False

    def is_enabled(self):
        return toggle_minimap_on_scroll_is_enabled

class EnableToggleMinimapOnScroll(sublime_plugin.WindowCommand):
    def run(self):
        global toggle_minimap_on_scroll_is_enabled
        toggle_minimap_on_scroll_is_enabled = True

    def is_enabled(self):
        return not toggle_minimap_on_scroll_is_enabled
