import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
import math
import pygame

pygame.mixer.init()
# clockhand width 23 px
# clockhand height hour 70 px, minute 81 px
# clock center = 175,205

# vars
def_pad = 20
button_height = 50
button_width = 200
button_corner = 26
button_border = 0
img_pad = 50
alarm_hour = 0 #24 hour format
alarm_min = 0
alarm_tone_path = ""

# Appearance (optional but common)
ctk.set_appearance_mode("Dark")   # Light / Dark / System
ctk.set_default_color_theme("blue")

# Main window
app = ctk.CTk()
app.title("Alarming Clock")
app.geometry("800x700")
app.iconbitmap("icon.ico")

# Set Assets
menu_img = ctk.CTkImage(dark_image=Image.open('assets/image/icon-in-menu.png'),size=(300,300))

heading = ctk.CTkFont(size=24,weight='bold')
button_text = ctk.CTkFont(size=16)
normal_text = ctk.CTkFont(size=16)

# clock_frame = ctk.CTkImage(dark_image=Image.open('assets/image/clock-frame.png'),size=(350,350))
clock_frame = Image.open("assets/image/clock-frame.png")


# Create frames for navigation
main_menu_frame = ctk.CTkFrame(app)
alarm_settings_frame = ctk.CTkFrame(app)
toneset_frame = ctk.CTkFrame(app)
alarm_frame = ctk.CTkFrame(app)

def show_frame(frame):
    """Hide all frames and show the selected frame"""
    main_menu_frame.pack_forget()
    alarm_settings_frame.pack_forget()
    toneset_frame.pack_forget()
    alarm_frame.pack_forget()
    frame.pack(fill="both", expand=True)

def go_to_alarm_settings():
    """Navigate to alarm settings window"""
    show_frame(alarm_settings_frame)

def go_to_main_menu():
    """Navigate back to main menu"""
    show_frame(main_menu_frame)

def go_to_toneset():
    show_frame(toneset_frame)

def go_to_alarm():
    show_frame(alarm_frame)

def menu_button():
    button.pack_forget()
    progress_bar.pack(padx=def_pad, pady=def_pad)
    animate_progressbar()

def animate_progressbar():
    value = progress_bar.get() + 0.01  # increase by 1%
    progress_bar.set(value)
    if value < 1.0:
        app.after(2, animate_progressbar)  # repeat until full
    else:
        go_to_alarm_settings()  # Switch to alarm settings immediately
        update_buttons()

def set_alarm():
    global paused    
    paused = True
    update_buttons()
def resume_alarm():
    global paused,clockspeed
    paused = False
    if clockspeed>1:
        clockspeed -= 1 # increases speed :D
    update_buttons()
def confirm_alarm():
    global alarm_hour,alarm_min
    global hour,min
    alarm_hour = hour
    alarm_min = min//1
    # print(alarm_hour,alarm_min,meridiem)
    go_to_toneset()
    

# ===== MAIN MENU FRAME =====
label = ctk.CTkLabel(main_menu_frame, text="Welcome to The Alarming App", font=heading)
label.pack(pady=def_pad, padx=def_pad)

menu_img_label = ctk.CTkLabel(main_menu_frame, image=menu_img, text='')
menu_img_label.pack(padx=def_pad, pady=def_pad)

button = ctk.CTkButton(main_menu_frame, text="Set an Alarm", command=menu_button, width=button_width, height=button_height, corner_radius=button_corner, border_width=button_border)
button.pack(pady=def_pad, padx=def_pad)

progress_bar = ctk.CTkProgressBar(main_menu_frame, orientation='horizontal', height=button_height, width=button_width, corner_radius=button_corner, mode='determinate')
progress_bar.set(0)



# ===== ALARM SETTINGS FRAME =====
settings_label = ctk.CTkLabel(alarm_settings_frame, text="Set Alarm: Stop the clock by pressing the button.", font=heading)
settings_label.pack(pady=def_pad, padx=def_pad)

canvas = tk.Canvas(alarm_settings_frame, width=350, height=350, bg="#2b2b2b", highlightthickness=0)
canvas.pack(pady=20)
bg_image = ImageTk.PhotoImage(clock_frame)


# Add your alarm setting widgets here
# clock_frame_label = ctk.CTkLabel(alarm_settings_frame, image=clock_frame, text='')
# clock_frame_label.pack(pady=def_pad,padx=def_pad)

paused = False
clockspeed = 10  #ms
hour = 0
min = 0
sec = 0
meridiem = 0
def draw_hands():
    global paused
    global hour
    global min
    global sec
    global meridiem

    if not paused:
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=bg_image)

        # curr_time = datetime.now()
        # hour = curr_time.hour%12
        # min = curr_time.minute
        # sec = curr_time.second
        # print(hour,min,sec)
        min += 5
        hour+=min//60
        hour = hour%24
        meridiem = hour//12
        min = min%60

        hour_angle = math.radians((hour%24 + min/60)*30 - 90)
        hour_x = 175 + 70*math.cos(hour_angle)
        hour_y = 205 + 70*math.sin(hour_angle)
        canvas.create_line(175,205,hour_x,hour_y,width=23,fill="#3b8ed0", capstyle="round")

        min_angle = math.radians((min+sec/60)*6 - 90)
        min_x = 175 + 81*math.cos(min_angle)
        min_y = 205 + 81*math.sin(min_angle)
        canvas.create_line(175,205,min_x,min_y,width=23,fill="#3b8ed0", capstyle="round")

    alarm_str = "Alarm will be set to: " + str(hour%12).zfill(2) + " : " + str(min).zfill(2) + " " + ("PM" if meridiem else "AM")
    alarm_text.configure(text=alarm_str)

    canvas.after(clockspeed,draw_hands)


alarm_text = ctk.CTkLabel(alarm_settings_frame, text="",font=normal_text)
alarm_text.pack(padx=10,pady=10)


set_button = ctk.CTkButton(alarm_settings_frame, text="Set Alarm", command=set_alarm, width=button_width,height=button_height, corner_radius=button_corner)
resume_button = ctk.CTkButton(alarm_settings_frame, text="Resume", command=resume_alarm, width=button_width,height=button_height, corner_radius=button_corner)
confirm_button = ctk.CTkButton(alarm_settings_frame, text="Confirm", command=confirm_alarm, width=button_width,height=button_height, corner_radius=button_corner)

def update_buttons():
    # hide everything first
    set_button.pack_forget()
    resume_button.pack_forget()
    confirm_button.pack_forget()

    # show the right one
    if paused:
        resume_button.pack(pady=def_pad, padx=def_pad)
        confirm_button.pack(pady=def_pad, padx=def_pad)
    else:
        set_button.pack(pady=def_pad, padx=def_pad)

draw_hands()


# ===== TONE SET FRAME =====
toneset_heading = ctk.CTkLabel(toneset_frame, text="Set an alarm tone", font=heading)
toneset_heading.pack(padx=def_pad,pady=20)
smalltext = ctk.CTkLabel(toneset_frame,text="Here are some soothing alarm sounds to choose from",font=normal_text)
smalltext.pack(padx=def_pad,pady=0)

radio_frame = ctk.CTkFrame(toneset_frame)
radio_frame.pack(padx=def_pad,pady=def_pad)

def play_and_set():
    global alarm_tone_path
    alarm_tone_path = "assets/tones/" + radio_var.get() + ".mp3"
    # print(alarm_tone_path)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(alarm_tone_path)
    pygame.mixer.music.play(-1)
    
def settone():
    global alarm_tone_path
    if alarm_tone_path != "" and alarm_tone_path != "none":
        pygame.mixer.music.stop()
        go_to_alarm()

radio_var = ctk.StringVar(value="none")
nuke_rad = ctk.CTkRadioButton(radio_frame,text="Nuclear Alarm", command=play_and_set, value="nuclear-alarm",variable=radio_var)
nuke_rad.grid(row=0, column=0, sticky="w", pady=10,padx=50)
samsung = ctk.CTkRadioButton(radio_frame,text="Samsung (Maybe idk)", command=play_and_set, value="samsung",variable=radio_var)
samsung.grid(row=1, column=0, sticky="w", pady=10,padx=50)
witch = ctk.CTkRadioButton(radio_frame,text="Witch Laugh", command=play_and_set, value="witch-laugh",variable=radio_var)
witch.grid(row=2, column=0, sticky="w", pady=10,padx=50)
arthur = ctk.CTkRadioButton(radio_frame,text="Arthur Morgan", command=play_and_set, value="arthur",variable=radio_var)
arthur.grid(row=3, column=0, sticky="w", pady=10,padx=50)
siren = ctk.CTkRadioButton(radio_frame,text="Annoying Siren", command=play_and_set, value="annoying-siren",variable=radio_var)
siren.grid(row=4, column=0, sticky="w", pady=10,padx=50)
danger = ctk.CTkRadioButton(radio_frame,text="DANGER DANGER", command=play_and_set, value="danger",variable=radio_var)
danger.grid(row=5, column=0, sticky="w", pady=10,padx=50)
minion = ctk.CTkRadioButton(radio_frame,text="Minions", command=play_and_set, value="nonono",variable=radio_var)
minion.grid(row=6, column=0, sticky="w", pady=10,padx=50)


tone_button = ctk.CTkButton(toneset_frame, text="Set Tone", command=settone, width=button_width,height=button_height, corner_radius=button_corner)
tone_button.pack(padx=def_pad,pady=def_pad)


# ===== ALARM FRAME =====

alarm_msg = ctk.CTkLabel(alarm_frame, text="This text is not supposed to be seen, report bug", font=heading)
alarm_msg.pack(pady=def_pad,padx=def_pad)
alarm_img_label = ctk.CTkLabel(alarm_frame, image=menu_img, text="")
alarm_img_label.pack(padx=def_pad,pady=def_pad)
disclaimer = ctk.CTkLabel(alarm_frame, text="If you are reading this, there is a bug", font=normal_text)
disclaimer.pack(pady=def_pad,padx=def_pad)

def time_left():
    now = datetime.now()
    alarm = now.replace(hour=alarm_hour, minute=alarm_min, second=0)

    if alarm <= now:
        alarm = alarm.replace(day=now.day + 1)

    delta = alarm - now
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    return hours, minutes

alarm_triggered = False
def check_alarm():
    global alarm_triggered
    # global alarm_hour,alarm_min 
    now = datetime.now()
    
    # alarm_hour = now.hour
    # alarm_min = (now.minute + 1)

    if not alarm_triggered and now.hour == alarm_hour and now.minute == alarm_min:
        alarm_triggered = True
        show_alarm_ui()
        return
    else:
        h, m = time_left()
        alarm_msg.configure(text=f"Alarm will ring after {h} hour(s) {m} minute(s)")
        disclaimer.configure(text="The app needs to run in background to trigger alarm.")
    app.after(1000, check_alarm)

def show_alarm_ui():
    global alarm_tone_path
    show_frame(alarm_frame)
    
    app.protocol('WM_DELETE_WINDOW',lambda:None)    # dangerous line 

    # disclaimer.pack_forget()
    alarm_msg.configure(text="⏰ WAKE UP!")
    disclaimer.configure(text="These buttons do not work, smashing your PC is probably the only option :)")
    pygame.mixer.music.load(alarm_tone_path)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)
    
    img_path = "assets/image/" + radio_var.get() + ".jpeg"
    alarm_img = ctk.CTkImage(dark_image=Image.open(img_path),size=(300,300))
    alarm_img_label.configure(image=alarm_img)
    alarm_img_label.image = alarm_img  # KEEP REFERENCE

    snooze = ctk.CTkButton(alarm_frame, text="SNOOZE", width=button_width,height=button_height, corner_radius=button_corner)
    stop = ctk.CTkButton(alarm_frame, text="STOP", width=button_width,height=button_height, corner_radius=button_corner)
    snooze.pack(padx=def_pad,pady=10)
    stop.pack(padx=def_pad,pady=10)

    # important_msg = ctk.CTkLabel(alarm_frame, text="These buttons do not work, smashing your PC is probably the only option :)", font=normal_text)
    # important_msg.pack(padx=def_pad,pady=def_pad)



# show_frame(alarm_frame)
check_alarm()


# Show main menu initially
show_frame(main_menu_frame)

# app.protocol('WM_DELETE_WINDOW',lambda:None)    # dangerous line 
app.mainloop()
