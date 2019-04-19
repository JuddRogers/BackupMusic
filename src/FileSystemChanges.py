#
# Use pyinotify to find out when any of the directories containing files to back up change
#
import pyinotify

wm = pyinotify.WatchManager()
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname

    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname


#log.setLevel(10)
notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
notifier.start()

wdd = wm.add_watch('/tmp', mask, rec=True)
wm.rm_watch(wdd.values())
