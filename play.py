from tkinter import *
from collections import deque
import pysrt
import time


def convert_to_seconds(h, m, s):
    return h*3600 + m*60 + s


subs = pysrt.open('EB.srt', encoding='utf-8')
# subs = pysrt.open('ParanoidPark.srt', encoding='iso-8859-1')


subs_dic = {}
for i in subs:
    start_seconds = convert_to_seconds(i.start.hours, i.start.minutes, i.start.seconds)
    end_seconds = convert_to_seconds(i.end.hours, i.end.minutes, i.end.seconds)
    text = i.text.replace('\n', '').replace('<i>', '').replace('</i>', '')
    subs_dic[start_seconds] = [text, end_seconds - start_seconds]

subs_start_time = deque(subs_dic.keys())


class Player:

    def __init__(self, master):
        self.master = master

        master.title('')
        master.geometry('800x25')

        self.var = StringVar()
        self.var.set('')

        self.sub = Label(master, textvariable=self.var)
        self.sub.config(anchor=CENTER)
        self.sub.pack()

        self.duration = 0
        self.duration_start = 0
        self.duration_end = 0

        self.next_duration = 0

        self.length = 0
        
        self.current_sub = '***'
        self.current_sub_timing = 0

        self.cancel_id = None
        self.stopped = False

    def play(self, duration, length):

        if self.stopped:
            start1 = time.time()
            self.var.set(self.current_sub)
            self.master.update()
            self.stopped = False
            end1 = time.time()
            if self.duration:
                self.duration -= (end1-start1)
        else:
            if self.current_sub:
                self.current_sub = ""

                start2 = time.time()
                self.var.set(self.current_sub)
                self.master.update()
                end2 = time.time()

                self.current_sub_timing = subs_start_time.popleft()

                duration_waiting = self.current_sub_timing-length

                self.length += duration_waiting

                self.duration = 0 if duration_waiting-(end2-start2) < 0 else duration_waiting-(end2-start2)
                self.next_duration = subs_dic[self.current_sub_timing][1]
            else:
                self.current_sub = subs_dic[self.current_sub_timing][0]

                start3 = time.time()
                self.var.set(self.current_sub)
                self.master.update()
                end3 = time.time()

                self.duration = 0 if (duration-(end3-start3)) < 0 else (duration-(end3-start3))
                self.length += duration

                self.next_duration = 0

        self.duration_start = time.time()
        self.cancel_id = self.master.after(int(round(self.duration, 3)*1000),
                                           self.play, self.next_duration, self.length)

    def action(self, event=None):
        if self.stopped or not self.length:
            self.start()
        else:
            self.stop()

    def start(self):
        self.play(self.next_duration, self.length)

    def stop(self):
        if self.cancel_id:
            self.stopped = True

            self.duration_end = time.time()

            self.duration -= (self.duration_end-self.duration_start)

            self.master.after_cancel(self.cancel_id)
            self.cancel_id = None

            self.var.set("*Paused*")
            self.master.update()


root = Tk()
test = Player(root)

root.bind("<space>", test.action)

root.mainloop()
