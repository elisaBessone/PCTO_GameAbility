import tobii_research as tr
import time
from tkinter import *

def update_canvas():
    execute(my_eyetracker)
    w.delete("le_eye")
    draw_eye_relative_at(global_gaze_data["left_gaze_point_on_display_area"][0],
                         global_gaze_data["left_gaze_point_on_display_area"][1])
    draw_eye_relative_at(global_gaze_data["right_gaze_point_on_display_area"][0],
                         global_gaze_data["right_gaze_point_on_display_area"][1])
    master.after(100,update_canvas)

found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]
print("Eye Tracker Founded")


'''
Verificar se e qual eye-tracker foi localizado.
print("Address: " + my_eyetracker.address)
print ("Model: " + my_eyetracker.model)
print("Name: " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)
'''

def execute(eyetracker):
    gaze_data(eyetracker)
global_gaze_data = None

def gaze_data_callback(gaze_data):
    global global_gaze_data
    global_gaze_data = gaze_data

def gaze_data(eyetracker):
    global global_gaze_data

    print("Subscribing to gaze data for eye tracker th serial number {0}.".format(eyetracker.serial_number))
    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

    # Wait while some gaze data is collected.
    time.sleep(0.4)

    eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    print("Unsubscribed from gaze data.")
    print("Last received gaze package:")

def draw_eye_relative_at(x, y):
    center_X = canvas_width * x
    center_Y = canvas_height * y
    w.create_oval(center_X-25, center_Y-25, center_X+25, center_Y+25, fill="red",tags="le_eye")

execute(my_eyetracker)

master = Tk()

canvas_width = 980
canvas_height = 640
w = Canvas (master,
            width=canvas_width,
            height=canvas_height)
w.pack()

w.create_rectangle(canvas_width*0.5-300,canvas_height*0.5-150,canvas_width*0.5+300,canvas_height*0.5+150, fill="black")
w.create_line(0,0,canvas_width*0.5-300,canvas_height*0.5-150)
w.create_line(980,0,canvas_width*0.5+300,canvas_height*0.5-150)
w.create_line(0,640,canvas_width*0.5-300,canvas_height*0.5+150)
w.create_line(980,640,canvas_width*0.5+300,canvas_height*0.5+150)

update_canvas()
mainloop()