import tkinter as tk
from tkinter import simpledialog, messagebox
import winsound as sd
import os
from datetime import datetime

def beepsound():
    fr = 2000    # range : 37 ~ 32767
    du = 1000     # 1000 ms ==1second
    sd.Beep(fr, du) # winsound.Beep(frequency, duration)
    
def beepsound_long():
    fr = 2000    # range : 37 ~ 32767
    du = 3000     # 1000 ms ==1second
    sd.Beep(fr, du) # winsound.Beep(frequency, duration)

# Initialize Tkinter (hidden)
root = tk.Tk()
root.withdraw()

# Ask how many study sessions
study_count = simpledialog.askinteger("공부 횟수 입력", "공부 횟수를 입력하세요:", minvalue=1, maxvalue=100)
if study_count is None:
    exit()

# Time Constants
MIN = 60
SECOND = 1  # Debugging Modepi
TIMER_SET = SECOND  # Change to `MIN` for real execution
STUDYTIME = 30  # Minutes
BREAKTIME = 15  # Minutes

# Total Study Time Tracker
spend_time = 0  

# Create Timer Window (Always on Top)
timer_window = tk.Tk()
timer_window.title("남은 시간")
timer_window.geometry("300x70")
timer_window.attributes("-topmost", True)  # 🔥 Always keep window on top

time_label = tk.Label(timer_window, text="", font=("Arial", 16))
time_label.pack(pady=20)

def timer(type, remaining_time, callback):
    """ Timer function that updates UI based on study/break session """
    global spend_time
    if remaining_time > 0:
        if type == "STUDY":
            spend_time += 1  # Track total study time
        hours = remaining_time // 60
        minutes = remaining_time % 60
        time_label.config(text=f"남은 {'공부' if type == 'STUDY' else '휴식'} 시간: {hours} 시간 {minutes} 분")

        timer_window.after(1000 * TIMER_SET, lambda: timer(type, remaining_time - 1, callback))
    else:
        callback()  # Call next function when time is up

def study_session():
    """ Starts a study session, then asks user if they want to continue. """
    global study_count
    if study_count <= 0:
        return  # Stop if no more sessions left

    beepsound()
    messagebox.showinfo("공부 시작", f"남은 공부 시간: {STUDYTIME} 분")

    # Start study timer
    timer("STUDY", STUDYTIME, study_done)

def study_done():
    beepsound_long()

    """ Called when study session is over. Asks if user wants to continue. """
    global study_count

    # 🔥 Ensure MessageBox appears on top
    top = tk.Toplevel()
    top.attributes("-topmost", True)  # Always on top
    top.withdraw()  # Hide the window, only use it as a parent for MessageBox

    end_study = messagebox.askyesno("공부 종료", "공부를 끝내시겠습니까?", parent=top)
    
    top.destroy()  # Clean up the top-level window

    if end_study or study_count <= 1:  # Last session or user chooses to stop
        show_total_time()
    else:
        break_time()


def break_time():
    """ Starts a break session and then calls study_session() again """
    global study_count
    messagebox.showinfo("휴식 시간", f"남은 휴식 시간: {BREAKTIME} 분")

    # Start break timer
    timer("BREAK", BREAKTIME, break_done)

def break_done():
    """ Called when break is over. Starts the next study session or ends. """
    global study_count
    study_count -= 1
    if study_count > 0:
        study_session()
    else:
        show_total_time()

def show_total_time():
    """ Show total study time at the end """
    messagebox.showinfo("총 공부 시간", f"총 공부한 시간: {spend_time // 60} 시간 {spend_time % 60} 분")
    timer_window.destroy()
    
def record_time():
    """ Record the current time and return """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

def record_study(start_time, end_time):
    """ Record the total study time and date in txt file """
    log_file = "log.txt"
    log_entry = f"공부 시작 시간: {start_time} | 공부 종료 시간: {end_time}\n 총 공부 시간: {spend_time // 60} 시간 {spend_time % 60} 분\n"
    
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(log_entry)
    
    
# PROGRAM BEGINS
start_time = record_time() # record time

# Start study session
study_session()
end_time = record_time() # record time

record_study(start_time, end_time)
exit()


timer_window.mainloop()  # Keep UI running
