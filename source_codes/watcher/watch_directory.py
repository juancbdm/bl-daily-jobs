# -*- Coding: UTF-8 -*-
# coding: utf-8
from __future__ import generators
import os
import sys
import Queue
import threading
import time

import win32file
import win32con

ACTIONS = {
  1 : "Novo",
  2 : "Deletado",
  3 : "Atualizado",
  4 : "Renomeado para",
  5 : "Renomeado para"
}

def watch_path (path_to_watch, include_subdirectories=False):
  FILE_LIST_DIRECTORY = 0x0001
  hDir = win32file.CreateFile (
    path_to_watch,
    FILE_LIST_DIRECTORY,
    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
    None,
    win32con.OPEN_EXISTING,
    win32con.FILE_FLAG_BACKUP_SEMANTICS,
    None
  )
  while 1:
    results = win32file.ReadDirectoryChangesW (
      hDir,
      1024,
      include_subdirectories,
      win32con.FILE_NOTIFY_CHANGE_FILE_NAME | 
       win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
       win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
       win32con.FILE_NOTIFY_CHANGE_SIZE |
       win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
       win32con.FILE_NOTIFY_CHANGE_SECURITY,
      None,
      None
    )
    for action, file in results:
      full_filename = os.path.join (path_to_watch, file)
      if not os.path.exists (full_filename):
        file_type = "<deleted>"
      elif os.path.isdir (full_filename):
        file_type = 'folder'
      else:
        file_type = 'file'
      yield (file_type, full_filename, ACTIONS.get (action, "Unknown"))

class Watcher (threading.Thread):

  def __init__ (self, path_to_watch, results_queue, **kwds):
    threading.Thread.__init__ (self, **kwds)
    self.setDaemon (1)
    self.path_to_watch = path_to_watch
    self.results_queue = results_queue
    self.start ()

  def run (self):
    for result in watch_path (self.path_to_watch):
      self.results_queue.put (result)

if __name__ == '__main__':
  PATH_TO_WATCH = ["."]
  try: path_to_watch = sys.argv[1].split (",") or PATH_TO_WATCH
  except: path_to_watch = PATH_TO_WATCH
  path_to_watch = [os.path.abspath (p) for p in path_to_watch]

  print "Watching %s at %s" % (", ".join (path_to_watch), time.asctime ())
  files_changed = Queue.Queue ()
  
  for p in path_to_watch:
    Watcher (p, files_changed)

  while 1:
    try:
      file_type, filename, action = files_changed.get_nowait ()
      print file_type, filename, action
    except Queue.Empty:
      pass
    time.sleep (1)
