import os
import pygame
import tkinter as tk
from tkinter import ttk

class SoundboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Soundboard")
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.sound_folder = os.path.join(script_directory, "sounds")
        pygame.mixer.init()

        # Sound files
        sound_files = [f for f in os.listdir(self.sound_folder) if f.endswith(".mp3")]

        # Styles
        style = ttk.Style()
        style.configure("TButton", padding=(10, 10), font=('Helvetica', 12), background="white")
        style.configure("xbutton.TButton", padding=(10, 10), font=('Helvetica', 15), background="gray")

        self.buttons = []
        self.labels = []
        self.volume_scales = []

        for i, sound_file in enumerate(sound_files, start=1):
            sound_name = os.path.splitext(sound_file)[0]

            # Label
            label = ttk.Label(root, text=str(i))
            label.grid(row=2, column=i - 1, padx=5, pady=5, sticky="nsew")
            self.labels.append(label)

            # Button
            button = ttk.Button(root, text=sound_name, command=lambda sound_file=sound_file: self.play_sound(sound_file, button), style="TButton")
            button.grid(row=0, column=i - 1, padx=5, pady=5, sticky="nsew")  # Added sticky property
            self.buttons.append(button)

            # Volume
            volume_scale = ttk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL, command=lambda value, sound_file=sound_file: self.set_volume(value, sound_file))
            volume_scale.set(1.0)  # Set initial volume to max
            volume_scale.grid(row=1, column=i - 1, padx=5, pady=5, sticky="nsew")
            self.volume_scales.append(volume_scale)

            # Binding buttons
            root.bind(str(i), lambda event, sound_file=sound_file, button=button: self.play_sound(sound_file, button))


        root.grid_columnconfigure(len(sound_files), weight=0)

        for i in range(len(sound_files)):
            root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=0)
        root.grid_rowconfigure(2, weight=0)

        # Preset volume
        self.preset_volume_scale = ttk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL)
        self.preset_volume_scale.set(1.0)
        self.preset_volume_scale.grid(row=3, column=0, columnspan=len(sound_files), padx=5, pady=5, sticky="nsew")

        preset_button = ttk.Button(root, text="Set Preset Volume", command=self.set_preset_volume)
        preset_button.grid(row=4, column=0, columnspan=len(sound_files), padx=5, pady=5, sticky="nsew")

    def play_sound(self, sound_file, button):
        sound_path = os.path.join(self.sound_folder, sound_file)
        pygame.mixer.music.load(sound_path)
        volume_scale = self.volume_scales[self.buttons.index(button)]
        pygame.mixer.music.set_volume(volume_scale.get())
        pygame.mixer.music.play()
        self.change_background(button)

    def set_volume(self, value, sound_file):
        sound_path = os.path.join(self.sound_folder, sound_file)
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(float(value))

    def change_background(self, button):
        for btn in self.buttons:
            btn.configure(style="TButton")
        button.configure(style="xbutton.TButton")

    def set_preset_volume(self):
        preset_value = self.preset_volume_scale.get()
        for volume_scale in self.volume_scales:
            volume_scale.set(preset_value)

if __name__ == "__main__":
    root = tk.Tk()
    app = SoundboardApp(root)
    root.mainloop()
