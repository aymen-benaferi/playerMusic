from tkinter import filedialog
from tkinter import *
import pygame
import os

root = Tk()
root.title('Player music')
root.geometry("500x400")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
paused = False
volume_level = 0.5


def load_music():
    global current_song
    root.directory = filedialog.askdirectory()

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)

    for song in songs:
        songlist.insert("end", song)

    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]


def play_music():
    global current_song, paused
    pygame.mixer.music.set_volume(volume_level)

    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False


def pause_music():
    global pause
    pygame.mixer.music.pause()
    paused = True


def next_music():
    global current_song, paused

    try:
        songlist.select_clear(0, END)
        songlist.select_set(songs.index(current_song) + 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass


def prev_music():
    global current_song, paused

    try:
        songlist.select_clear(0, END)
        songlist.select_set(songs.index(current_song) - 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass


def volume_up():
    global volume_level
    if volume_level < 1:
        volume_level += 0.1
    pygame.mixer.music.set_volume(volume_level)


def volume_down():
    global volume_level
    if volume_level > 0:
        volume_level -= 0.1
    pygame.mixer.music.set_volume(volume_level)


def toggle_loop():
    if pygame.mixer.music.get_busy():
        if pygame.mixer.music.get_pos() == -1:

            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
            paused = False


def add_song():
    file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file:
        songs.append(file)
        songlist.insert("end", os.path.basename(file))


def remove_song():
    selection = songlist.curselection()
    if selection:
        index = int(selection[0])
        songlist.delete(selection)
        songs.pop(index)


organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
organise_menu.add_command(label='Add File', command=load_music)
organise_menu.add_command(label='Delete File', command=next_music)
menubar.add_cascade(label='Organise', menu=organise_menu)


songlist = Listbox(root, bg="black", fg="white", width=100, height=15)
songlist.pack()

play_btn_image = PhotoImage(file='play.png')
pause_btn_image = PhotoImage(file='pause.png')
next_btn_image = PhotoImage(file='next.png')
prev_btn_image = PhotoImage(file='previous.png')
loop_btn_image = PhotoImage(file='loop.png')
minus_btn_image = PhotoImage(file='minus.png')
plus_btn_image = PhotoImage(file='plus.png')

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_image,
                  borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image,
                   borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_image,
                  borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_btn_image,
                  borderwidth=0, command=prev_music)
loop_btn = Button(control_frame, image=loop_btn_image,
                  borderwidth=0, command=toggle_loop)
minus_btn = Button(control_frame, image=minus_btn_image,
                   borderwidth=0, command=volume_down)
plus_btn = Button(control_frame, image=plus_btn_image,
                  borderwidth=0, command=volume_up)

# Placement des boutons de contrôle du volume
play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)
loop_btn.grid(row=0, column=4, padx=7, pady=10)
minus_btn.grid(row=0, column=5, padx=7, pady=10)
plus_btn.grid(row=0, column=6, padx=7, pady=10)

root.mainloop()
