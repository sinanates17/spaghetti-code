import os
import pykakasi

#The other script forgot to set a preview point and clean the difficulty names from unicode, so this does that.

if __name__ == '__main__':
    dir = "C:/Users/Sinan/AppData/Local/osu!/Songs/beatmap-638305163321443923-virtual/"
    kk = pykakasi.kakasi()
    kk.setMode("H","a")
    kk.setMode("K","a")
    kk.setMode("J","a")
    kk.setMode("r","Hepburn")
    kk.setMode("s", True)
    kk.setMode("C", True)
    conv = kk.getConverter()
    for file in os.listdir(dir):
        if file.endswith(".osu"):
            with open(dir+file,"r",encoding="utf-8") as f:
                newfile = ""
                for line in f.readlines():
                    if 'PreviewTime' in line:
                        newfile += 'PreviewTime: 30000\n'
                    elif 'Version' in line:
                        newfile += ''.join(char for char in conv.do(line) if ord(char) < 128)
                    else:
                        newfile += line

            with open(dir+file,"w",encoding="utf-8") as f:
                f.write(newfile)
