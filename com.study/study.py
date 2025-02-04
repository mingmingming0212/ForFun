import tkinter as tk
from tkinter import simpledialog, messagebox
import winsound as sd
from datetime import datetime
import os

def beepsound():
    fr = 2000    # range : 37 ~ 32767
    du = 1000     # 1000 ms ==1second
    sd.Beep(fr, du) # winsound.Beep(frequency, duration)
    
def beepsound_long():
    fr = 2000    # range : 37 ~ 32767
    du = 3000     # 1000 ms ==1second
    sd.Beep(fr, du) # winsound.Beep(frequency, duration)
    
def record_time():
    """ Record the current time and return """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Initialize Tkinter (hidden)
root = tk.Tk()
root.withdraw()

# Ask how many study sessions
study_count = simpledialog.askinteger("1", "공부 횟수를 입력하세요:", minvalue=1, maxvalue=100)
if study_count is None:
    exit()
    
def save_values():
    global study_duration, break_duration
    study_input = study_entry.get().strip()
    break_input = break_entry.get().strip()
    
    study_duration = int(study_input) if study_input.isdigit() else 30
    break_duration = int(break_input) if break_input.isdigit() else 15
    
    plan_window.destroy()
    
def use_default():
    global study_duration, break_duration
    study_duration, break_duration = 30, 15
    plan_window.destroy()
    

# Ask about the study plan
plan_window = tk.Toplevel()
plan_window.title("공부계획 설정")
plan_window.geometry("300x200")
plan_window.attributes("-topmost", True)

tk.Label(plan_window, text="직접 공부계획을 설정 하실 수 있습니다.\n(기본 공부시간 30분, 휴식시간 15분)").pack(pady=5)

# Input Window
tk.Label(plan_window, text="공부 시간 (분):").pack(pady=5)
study_entry = tk.Entry(plan_window)
study_entry.pack(pady=5)

tk.Label(plan_window, text="휴식 시간 (분):").pack(pady=5)
break_entry = tk.Entry(plan_window)
break_entry.pack(pady=5)

# Button
button_frame = tk.Frame(plan_window)
button_frame.pack(pady=10)

tk.Button(button_frame, text="확인", command=save_values).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="취소", command=use_default).pack(side=tk.RIGHT, padx=5)

# If terminated, use default
plan_window.protocol("WM_DELETE_WINDOW", use_default)

# Wait for a call from user
plan_window.wait_window()
    
    

# Time Constants
MIN = 60
SECOND = 1  
TIMER_SET = SECOND  # Change to `MIN` for real execution

DEBUG = 1

# DEBUG SETTING
TIME = 1000 * TIMER_SET
# TIME = DEBUG

# Total Study Time Tracker
show_seconds = True
spend_time = 0  
start_time = record_time() # record time

# Create Timer Window (Always on Top)
timer_window = tk.Tk()
timer_window.title("남은 시간")
timer_window.geometry("400x90")
timer_window.attributes("-topmost", True)  # Always keep window on top

def on_close():
    """ Terminate the program when user close the timer """
    study_over()

# If User terminates the timer window, terminate the application
timer_window.protocol("WM_DELETE_WINDOW", on_close)

time_label = tk.Label(timer_window, text="", font=("HY견고딕", 16))
time_label.pack(pady=10)

def toggle_seconds():
    """ 초 표시 여부를 변경하는 함수 """
    global show_seconds
    show_seconds = not show_seconds  # True <-> False 변경

# Toggle 'Seconds' Timer
toggle_button = tk.Button(timer_window, text="초 설정", command=toggle_seconds)
toggle_button.pack(pady=5)

def timer(type, remaining_time, callback):
    """ Timer function that updates UI based on study/break session """
    global spend_time
    if remaining_time > 0:
        if type == "STUDY":
            spend_time += 1  # Track total study time
        
        hours = remaining_time // 3600
        minutes = (remaining_time % 3600) // 60
        seconds = remaining_time % 60

        # 초 숨김 여부에 따라 다르게 표시
        if show_seconds:
            time_label.config(text=f"남은 {'공부' if type == 'STUDY' else '휴식'} 시간: {hours} 시간 {minutes} 분 {seconds} 초")
        else:
            time_label.config(text=f"남은 {'공부' if type == 'STUDY' else '휴식'} 시간: {hours} 시간 {minutes} 분")

        timer_window.after(TIME, lambda: timer(type, remaining_time - 1, callback))  # 1초마다 갱신
    else:
        callback()  # Call next function when time is up


def study_session():
    """ Starts a study session, then asks user if they want to continue. """
    global study_count
    if study_count <= 0:
        return  # Stop if no more sessions left

    beepsound()
    messagebox.showinfo("공부 시작", f"남은 공부 시간: {study_duration} 분")

    # Start study timer
    timer("STUDY", study_duration * 60, study_session_complete)


def study_session_complete():
    beepsound_long()
    
    # top function for popup
    top = tk.Toplevel()
    top.attributes("-topmost", True)
    top.withdraw()  


    """ Called when study session is over. Asks if user wants to continue. """
    global study_count

    end_study = messagebox.askyesno("공부 종료", "공부를 끝내시겠습니까?", parent=top)
    
    top.destroy()  # Clean up the top-level window

    if end_study or study_count <= 1:  # Last session or user chooses to stop
        study_over()
    else:
        break_time()


def break_time():
    
    top = tk.Toplevel()
    top.attributes("-topmost", True)
    top.withdraw()  

    """ Starts a break session and then calls study_session() again """
    global study_count
    messagebox.showinfo("휴식 시간", f"남은 휴식 시간: {break_duration} 분", parent=top)

    # Start break timer
    timer("BREAK", break_duration * 60, break_done)


def break_done():
    """ Called when break is over. Starts the next study session or ends. """
    global study_count
    study_count -= 1
    if study_count > 0:
        study_session()
    else:
        study_over()


def study_over():
    """ When the study is completely finished """
    global end_time
    end_time = record_time()  # Record end time

    total_hours = spend_time // 3600
    total_minutes = (spend_time % 3600) // 60
    total_seconds = spend_time % 60


    print(f"DEBUG: 총 공부 시간 = {total_hours}시간 {total_minutes}분 {total_seconds}초")

    record_study(start_time, end_time, total_hours, total_minutes, total_seconds)

    messagebox.showinfo("총 공부 시간", f"총 공부한 시간: {total_hours} 시간 {total_minutes} 분 {total_seconds} 초")
    
    timer_window.destroy()
    exit()

def record_study(start_time, end_time, hours, minutes, seconds):
    """ Record the total study time and date in txt file """
    log_file = "log.txt"
    log_entry = (
        f"공부 시작 시간: {start_time} | 공부 종료 시간: {end_time}\n"
        f"총 공부 시간: {hours} 시간 {minutes} 분 {seconds} 초\n\n"
    )

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(log_entry)

    
# PROGRAM BEGINS

# Start study session
study_session()

timer_window.mainloop()  # Keep UI running
