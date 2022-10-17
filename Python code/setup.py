import cx_Freeze
import sys
import os 
base = None

if sys.platform == 'win32':
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python37\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python37\tcl\tk8.6"


executables = [cx_Freeze.Executable("app.py", base=base, icon="icon.ico")]

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "YTube Downloader",     # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]app.exe",   # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
      'TARGETDIR'               # WkDir
     )
                  
    #("StartupShortcut",        # Shortcut
     #"StartupFolder",          # Directory_
     #"Yt Playlist Downloader",     # Name
   #  "TARGETDIR",              # Component_
  #   "[TARGETDIR]app.exe",   # Target
  #   None,                     # Arguments
 #    None,                     # Description
 #    None,                     # Hotkey
  #   None,                     # Icon
  #   None,                     # IconIndex
  #   None,                     # ShowCmd
  #   'TARGETDIR'               # WkDir
 #    )

    ]

msi_data = {"Shortcut": shortcut_table} 


cx_Freeze.setup(
    name = "YTube Downloader",
    options = {"build_exe": {"packages":["tkinter","turtle","os","pytube","threading","win32clipboard","urllib.error"], "include_files":["images","icon.ico",'tcl86t.dll','tk86t.dll'], "excludes":["captions"]},'bdist_msi': {
            'data': msi_data}},
    version = "2.0",
    description = "Tkinter Application",
    executables = executables
    )