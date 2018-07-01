import os
import subprocess
from datetime import datetime


ffprobe = r"ffprobe\ffprobe.exe"
filename = r"TestFiles\shifted.mkv"
subfile = r"TestFiles\shifted.ass"

ffprobe = os.path.join(os.path.dirname(os.path.abspath(__file__)), ffprobe)
filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
subfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), subfile)

def shift(sub_path, video_path, amount):
    fps = find_fps(video_path)
    if fps == -1:
        print("Couldn't find fps. Check that the video_path is correct.")
        return

    shift_amount = 0
    if amount.endswith("ms"):
        shift_amount = int(amount[:-2])
    elif amount.endswith("f"):
        frames = amount[:-1]
        shift_amount = float(frames) / float(fps) * 1000
        shift_amount = int(round(shift_amount, 0))
    else:
        print("Invalid shift time.")
        return

    with open(sub_path + "-temp", 'w', encoding='UTF-8') as newfile:
        with open(sub_path, 'r',encoding='UTF-8') as sub:
            events = False
            for line in sub:
                if "[Events]" in line:
                    events = True
                
                if events and line.startswith("Dialogue"):
                    line = shift_line(line, shift_amount)
                
                newfile.write(line)
    os.remove(sub_path)
    os.rename(sub_path + "-temp", sub_path)


def shift_line(line, amount):
    line = line.split(',')
    start_time = to_ms(line[1])
    end_time = to_ms(line[2])

    start_time = start_time + amount
    end_time = end_time + amount

    line[1] = to_time(start_time)
    line[2] = to_time(end_time)
    line = ','.join(line)
    return line

def to_ms(timestamp):
    h, m, s = timestamp.split(':')
    s, ms = s.split('.')
    ms = int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)
    return int(ms)

def to_time(ms):
    ms = int(ms)
    
    s = (ms / 1000)%60
    s = int(s)
    m = (ms / (1000*60))%60
    m = int(m)
    h = (ms / (1000 * 60 * 60))%24
    h = int(h)

    ms = ms % 1000
    '''
    ms = int(ms)
    h = ms // 3600000
    rest = ms % 3600000
    m = rest // 60000
    rest = rest % 60000
    s = rest // 1000
    ms = rest % 1000'''
    return "{0}:{1}:{2}.{3}".format(h, format(m,'02d'), format(s,'02d'), format(ms,'02d')[:2])


def find_fps(video_path):
    cmd = [ffprobe, "-v", "0", "-of", "csv=p=0", "-select_streams", "0", "-show_entries", "stream=r_frame_rate", video_path]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err =  p.communicate()
    if err:
        print ("========= error ========")
        print(err)
        return -1
    out = out.decode("utf-8")
    out = out.rstrip()
    fps = out.split('/')
    fps = float(fps[0]) / float(fps[1])
    return fps

#shift(subfile, filename, "998ms")