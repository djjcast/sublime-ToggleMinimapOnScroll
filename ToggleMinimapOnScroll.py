import sublime
import sublime_plugin
from threading import Thread, Lock
from time import sleep

default_settings = {
    "toggle_minimap_on_scroll_enabled_by_default": True,
    "toggle_minimap_on_scroll_duration_in_seconds": 2.5,
    "toggle_minimap_on_scroll_samples_per_second": 7.5,
    "toggle_minimap_on_cursor_line_changed": False,
    "toggle_minimap_on_view_changed": False
}
def get_setting(name):
    settings = sublime.load_settings("ToggleMinimapOnScroll.sublime-settings")
    return settings.get(name, default_settings[name])

toggle_minimap_on_scroll_is_enabled = get_setting("toggle_minimap_on_scroll_enabled_by_default")
def plugin_loaded():
    global toggle_minimap_on_scroll_is_enabled
    toggle_minimap_on_scroll_is_enabled = get_setting("toggle_minimap_on_scroll_enabled_by_default")

lock = Lock()
ignore_events = False
ignore_count = 0
prev_wrap_widths = {}

def unset_fixed_wrap_width():
    for window in sublime.windows():
        for view in window.views():
            view_id = view.id()
            if view_id in prev_wrap_widths:
                view_settings = view.settings()
                view_settings.set("wrap_width", prev_wrap_widths[view_id])

def set_fixed_wrap_width():
    global prev_wrap_widths
    curr_wrap_widths = {}
    for window in sublime.windows():
        for view in window.views():
            view_id = view.id()
            view_settings = view.settings()
            view_wrap_width = view_settings.get("wrap_width", 0)
            if not view_wrap_width:
                view_settings.set("wrap_width", view.viewport_extent()[0] / view.em_width())
            curr_wrap_widths[view_id] = view_wrap_width
    prev_wrap_widths = curr_wrap_widths

def toggle_minimap_all_windows():
    for window in sublime.windows():
        window.run_command("toggle_minimap")

def untoggle_minimap():
    with lock:
        global ignore_events, ignore_count
        if ignore_events:
            toggle_minimap_all_windows()
            unset_fixed_wrap_width()
            ignore_events = False
            ignore_count += 1

def untoggle_minimap_on_timeout():
    with lock:
        global ignore_events, ignore_count
        if ignore_count:
            ignore_count -= 1
            return
        toggle_minimap_all_windows()
        unset_fixed_wrap_width()
        ignore_events = False

def toggle_minimap():
    with lock:
        global ignore_events, ignore_count
        if not ignore_events:
            set_fixed_wrap_width()
            toggle_minimap_all_windows()
            ignore_events = True
        else:
            ignore_count += 1
        sublime.set_timeout(untoggle_minimap_on_timeout, int(float(get_setting("toggle_minimap_on_scroll_duration_in_seconds")) * 1000))

prev_active_view_id = None
prev_viewport_states = {}
def viewport_scrolled():
    global prev_active_view_id, prev_viewport_states
    viewport_scrolled = False
    curr_active_view_id = sublime.active_window().active_view().id()
    curr_viewport_states = {}
    for window in sublime.windows():
        for view in window.views():
            view_id = view.id()
            viewport_position = view.viewport_position()
            viewport_extent = view.viewport_extent()
            if prev_active_view_id == curr_active_view_id and \
               view_id in prev_viewport_states and \
               prev_viewport_states[view_id]['viewport_position'] != viewport_position and \
               prev_viewport_states[view_id]['viewport_extent'] == viewport_extent:
                viewport_scrolled = True
            curr_viewport_states[view_id] = {'viewport_position': viewport_position,
                                             'viewport_extent': viewport_extent}
    prev_active_view_id = curr_active_view_id
    prev_viewport_states = curr_viewport_states
    return viewport_scrolled

def sample_viewport():
    try:
        if viewport_scrolled():
            toggle_minimap()
    except AttributeError:
        pass  # suppress ignorable error message (window and/or view does not exist)

class ViewportMonitor(Thread):
    sample_period = 1 / default_settings["toggle_minimap_on_scroll_samples_per_second"]

    def run(self):
        while True:
            if toggle_minimap_on_scroll_is_enabled:
                sublime.set_timeout(sample_viewport, 0)
            sublime.set_timeout(self.update_sample_period, 0)
            sleep(self.sample_period)

    def update_sample_period(self):
        self.sample_period = 1 / float(get_setting("toggle_minimap_on_scroll_samples_per_second"))
if not "viewport_monitor" in globals():
    viewport_monitor = ViewportMonitor()
    viewport_monitor.start()

class EventListener(sublime_plugin.EventListener):
    startup_events_triggered = False  # ignore startup events (Sublime Text 2)
    prev_sel_begin_row = None
    prev_sel_end_row = None
    prev_num_sel = None

    def cursor_line_changed(self, view):
        cursor_line_changed = False
        curr_sel_begin_row = view.rowcol(view.sel()[0].begin())[0]
        curr_sel_end_row = view.rowcol(view.sel()[0].end())[0]
        curr_num_sel = len(view.sel())
        if curr_sel_begin_row != self.prev_sel_begin_row or curr_sel_end_row != self.prev_sel_end_row or curr_num_sel != self.prev_num_sel:
            cursor_line_changed = True
        self.prev_sel_begin_row = curr_sel_begin_row
        self.prev_sel_end_row = curr_sel_end_row
        self.prev_num_sel = curr_num_sel
        return cursor_line_changed

    def on_selection_modified(self, view):
        if not view.window():  # ignore startup events (Sublime Text 2)
            return
        if not self.startup_events_triggered:  # ignore startup events (Sublime Text 2)
            self.startup_events_triggered = True
            return
        if toggle_minimap_on_scroll_is_enabled and get_setting("toggle_minimap_on_cursor_line_changed") and self.cursor_line_changed(view):
            toggle_minimap()

    def on_activated(self, view):
        if not self.startup_events_triggered:  # ignore startup events (Sublime Text 2)
            return
        if toggle_minimap_on_scroll_is_enabled and get_setting("toggle_minimap_on_view_changed"):
            toggle_minimap()

    def on_deactivated(self, view):
        if toggle_minimap_on_scroll_is_enabled:
            untoggle_minimap()

    def on_close(self, view):
        if toggle_minimap_on_scroll_is_enabled:
            try:
                untoggle_minimap()
            except AttributeError:
                pass  # suppress ignorable error message (window does not exist)

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
