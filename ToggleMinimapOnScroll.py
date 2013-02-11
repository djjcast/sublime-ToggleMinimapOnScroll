import sublime
import sublime_plugin
from threading import Thread
from time import sleep

ignore_events = False
ignore_count = 0
active_view = None
settings = sublime.load_settings("ToggleMinimapOnScroll.sublime-settings")
toggle_minimap_on_scroll_enabled = settings.get("toggle_minimap_on_scroll_by_default", True)


class SampleViewportPosition(sublime_plugin.TextCommand):
    last_viewport_position_sample = None

    def run(self, edit):
        if self.viewport_position_changed():
            self.toggle_minimap_for_duration()

    def viewport_position_changed(self):
        viewport_position_changed = False
        viewport_position_sample = active_view.viewport_position()
        if self.last_viewport_position_sample and viewport_position_sample[1] != self.last_viewport_position_sample[1]:
            viewport_position_changed = True
        self.last_viewport_position_sample = viewport_position_sample
        return viewport_position_changed

    def toggle_minimap_for_duration(self):
        global ignore_events, ignore_count
        if not ignore_events:
            active_view.window().run_command("toggle_minimap")
            ignore_events = True
        else:
            ignore_count += 1
        settings = sublime.load_settings("ToggleMinimapOnScroll.sublime-settings")
        sublime.set_timeout(lambda: active_view.window().run_command("untoggle_minimap_on_timeout"),
                            int(float(settings.get("toggle_minimap_on_scroll_duration_seconds", 2.5)) * 1000))


class ViewportPositionMonitor(Thread):
    sample_period = 0.1

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            if toggle_minimap_on_scroll_enabled:
                sublime.set_timeout(lambda: active_view.run_command("sample_viewport_position"), 0)
            sublime.set_timeout(lambda: self.get_viewport_position_samples_per_second(), 0)
            sleep(self.sample_period)

    def get_viewport_position_samples_per_second(self):
        settings = sublime.load_settings("ToggleMinimapOnScroll.sublime-settings")
        self.sample_period = 1 / float(settings.get("viewport_position_samples_per_second", 10))
if not "viewport_position_monitor" in globals():
    viewport_position_monitor = ViewportPositionMonitor()
    viewport_position_monitor.start()


class UntoggleMinimapOnTimeout(sublime_plugin.WindowCommand):
    def run(self):
        global ignore_events, ignore_count, toggle_minimap_on_scroll_enabled
        if ignore_count:
            ignore_count -= 1
            return
        self.window.run_command("toggle_minimap")
        ignore_events = False


class ToggleMinimapOnScroll(sublime_plugin.EventListener):
    startup_events_finished = False  # ignore startup events
    last_selection_begin_row = None
    last_selection_end_row = None
    last_num_selection = None

    def on_selection_modified(self, view):
        if not view.window():  # ignore startup events
            return
        if not self.startup_events_finished:  # ignore startup events
            self.startup_events_finished = True
            return
        settings = sublime.load_settings("ToggleMinimapOnScroll.sublime-settings")
        if settings.get("toggle_minimap_on_cursor_line_changed", True) and \
           toggle_minimap_on_scroll_enabled and \
           self.cursor_line_changed():
            self.toggle_minimap_for_duration()

    def cursor_line_changed(self):
        cursor_line_changed = False
        selection_begin_row = active_view.rowcol(active_view.sel()[0].begin())[0]
        selection_end_row = active_view.rowcol(active_view.sel()[0].end())[0]
        num_selection = len(active_view.sel())
        if selection_begin_row != self.last_selection_begin_row or \
            selection_end_row != self.last_selection_end_row or \
            num_selection != self.last_num_selection:
            cursor_line_changed = True
        self.last_selection_begin_row = selection_begin_row
        self.last_selection_end_row = selection_end_row
        self.last_num_selection = num_selection
        return cursor_line_changed

    def on_activated(self, view):
        global active_view
        active_view = view
        if not self.startup_events_finished:  # ignore startup events
            return
        settings = sublime.load_settings("ToggleMinimapOnScroll.sublime-settings")
        if settings.get("toggle_minimap_on_view_changed", True) and toggle_minimap_on_scroll_enabled:
            self.toggle_minimap_for_duration()

    def toggle_minimap_for_duration(self):
        global ignore_events, ignore_count
        if not ignore_events:
            active_view.window().run_command("toggle_minimap")
            ignore_events = True
        else:
            ignore_count += 1
        settings = sublime.load_settings("ToggleMinimapOnScroll.sublime-settings")
        sublime.set_timeout(lambda: active_view.window().run_command("untoggle_minimap_on_timeout"),
                            int(float(settings.get("toggle_minimap_on_scroll_duration_seconds", 2.5)) * 1000))


class DisableToggleMinimapOnScroll(sublime_plugin.WindowCommand):
    def run(self):
        global toggle_minimap_on_scroll_enabled
        toggle_minimap_on_scroll_enabled = False

    def is_enabled(self):
        return toggle_minimap_on_scroll_enabled


class EnableToggleMinimapOnScroll(sublime_plugin.WindowCommand):
    def run(self):
        global toggle_minimap_on_scroll_enabled
        toggle_minimap_on_scroll_enabled = True

    def is_enabled(self):
        return not toggle_minimap_on_scroll_enabled
