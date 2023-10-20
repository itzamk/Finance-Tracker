# autocomplete.py
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

class AutocompleteEntry(ttk.Combobox):

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)  # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())

        _hits = []
        for item in self._completion_list:
            if item.lower().startswith(self.get().lower()):  # Match case-insensitively
                _hits.append(item)

        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits

        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(_hits)

        # now finally perform the auto completion
        if self._hits:
            self._matched_element = _hits[self._hit_index]  # store current matched element
            self._update(_hits[self._hit_index])

    def _update(self, hit):
        user_input = self.get()
        self.delete(0, tk.END)
        self.insert(0, hit)
        self.position = len(user_input)
        self.icursor(self.position)  # Set the cursor position to the end of the user input

    def handle_keyrelease(self, event):
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Shift_R', 'Shift_L', 'Control_R', 'Control_L'):
            return

        if event.keysym == 'Return':
            self._hits = []
            return

        if event.keysym == 'Up':
            self.autocomplete(-1)  # Move up in the list
        elif event.keysym == 'Down':
            self.autocomplete(1)  # Move down in the list
        else:
            self.autocomplete()
