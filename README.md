# Home Automation

Set-up instructions for Windows
--------
- (optional) Git Bash (http://git-scm.com/download/win)
- Install Python 2.7.9 
  - Download and Run (https://www.python.org/ftp/python/2.7.9/python-2.7.9.msi)
  - Add python and pip to windows PATH
    - Control Panel - System
    - Open 'Advanced system settings'
    - Click 'Evironment Variables' button on Advanced tab
    - Edit PATH and add `;C:\Python27;C:\Python27\Scripts`
- Install OpenCV
  - Download and Extract from (https://sourceforge.net/projects/opencvlibrary/files/opencv-win/2.4.10/opencv-2.4.10.exe/download)
  - Copy cv2.pyd into your Python Lib folder
    - E.g. `cp ~/Downloads/opencv/build/python/2.7/x86/cv2.pyd C:/Python27/Lib/cv2.pyd`
  - Run `pip install numpy matplotlib`
- Download and Install PyAudio (http://people.csail.mit.edu/hubert/pyaudio/packages/pyaudio-0.2.8.py27.exe)
    
