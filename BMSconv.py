import subprocess
import os
import shutil
from PIL import Image

if __name__ == '__main__':

    convert_path = "C:/Users/Sinan/Downloads/delta_~20221022_solid.part1" #Folder containing individual BMS song folders
    converter_path = "C:/Users/Sinan/Downloads/raindrop-0.600b/release/convertOM.bat"
    converted_path = "C:/Users/Sinan/Desktop/Stupid/convertsI"

    songs = os.listdir(convert_path)
    song_counter=0

    size_counter = 0
    Title = "Title:δ Table DP Collection 1\n"
    TitleU = "TitleUnicode:Delta Table DP Collection 1\n"
    Title_Counter = 1

    for song in songs:
        song_counter += 1
        title = song.split(' (by ')[0]          #Extract the title and artist from the song's folder name
        artist = song.split(' (by ')[1][:-1]
        audio_name = title + artist + '.ogg'
        songdir = convert_path + '/' + song
        bg = None

        for file in os.listdir(songdir):
            if file[-4:] in ['.bms','.bme','.bml']:
                print("Song " + str(song_counter) + " of 469")
                file_path = songdir + '/' + file

                is_dp = False
                level = None

                with open(file_path,'r',encoding='utf-8',errors='ignore') as f:
                    for line in f.readlines():
                        if '#PLAYER 3' in line:
                            is_dp = True
                        if '#PLAYER 1' in line:
                            break
                        if '#STAGEFILE' in line:
                            if '.' in line:
                                bg = line[11:-1]
                            continue

                if is_dp:
                    subprocess.call([converter_path,file_path])

        if bg is not None:
            im = Image.open(songdir + '/' + bg)                                                                #Do shit
            im = im.convert("RGB")
            bg = bg[:-4] + audio_name + ".jpg"
            im.save(songdir + '/' + bg)

        for file in os.listdir(songdir):
            file_path = songdir + '/' + file
            if file[-4:] == '.osu':

                new_file = ""

                with open(file_path,'r',encoding='utf-8',errors='ignore') as f:
                    eventing = False
                    objecting = False
                    for line in f.readlines():
                        if '[TimingPoints]' in line:
                            eventing = False
                        if eventing:
                            continue
                        if objecting:
                            if ',' in line[:3]:
                                new_file += line[:line.index(':')] + ":0:0:0:\n"
                            elif line[:3] == '272' and ',' not in line[:3]:
                                new_file += '496' + line[3:line.index(':')] + ":0:0:0:\n"
                            elif int(line[:3]) > 300 and ',' not in line[:3]:
                                new_file += str(int(line[:3])-32) + line[3:line.index(':')] + ":0:0:0:\n"
                            else:
                                new_file += line[:line.index(':')] + ":0:0:0:\n"
                            continue
                        if 'AudioFilename:' in line:
                            new_file += f'AudioFilename: {audio_name}\n'
                        elif 'osu file format' in line:
                            new_file += 'osu file format v14'
                        elif 'Creator:' in line:
                            new_file += "Creator:Hugged\n"
                        elif 'Title:' in line:
                            new_file += Title
                        elif 'TitleUnicode:' in line:
                            new_file += TitleU
                        elif 'Artist:' in line:
                            new_file += "Artist:Various Artists\n"
                        elif 'ArtistUnicode:' in line:
                            new_file += "ArtistUnicode:Various Artists\n"
                        elif 'Version:' in line:
                            new_file += "Version:" + artist + ' - ' + title + " | DP " + line[9:]
                        elif 'Source:' in line:
                            new_file += "Source:BMS\n"
                        elif 'Tags:' in line:
                            new_file += "Tags:BMS DP Double Play N+2 scratch 14K2S 14+2K 14K+2\n"
                        elif 'HPDrainRate:' in line:
                            new_file += "HPDrainRate:9\n"
                        elif 'OverallDifficulty:' in line:
                            new_file += "OverallDifficulty:5\n"
                        elif 'ApproachRate:' in line:
                            new_file += "ApproachRate:9\n"
                        elif 'CircleSize:' in line:
                            new_file += "CircleSize:16\n"
                        elif 'SliderMultiplier:' in line:
                            new_file += "SliderMultiplier:1.4\n"
                        elif 'SliderTickRate:' in line:
                            new_file += "SliderTickRate:1\n"
                        elif "[Events]" in line:
                            eventing = True
                            new_file += f'[Events]\n0,0,"{bg}",0,0\n\n' if bg is not None else '[Events]\n0,0,"convertbg.jpg",0,0\n\n'
                        elif "[HitObjects]" in line:
                            objecting = True
                            new_file += "[HitObjects]\n"
                        else:
                            new_file += line

                with open(file_path,'w',encoding='utf-8',errors='ignore') as f:
                    f.write(new_file)

                shutil.move(file_path, converted_path + '/' + file)
                size_counter += os.path.getsize(converted_path + '/' + file)

            if file == 'audio.ogg':
                shutil.copy(file_path, converted_path + '/' + audio_name)
                size_counter += os.path.getsize(converted_path + '/' + audio_name)
            
            if file == bg:
                shutil.copy(file_path, converted_path + '/' + bg)
                size_counter += os.path.getsize(converted_path + '/' + bg)
        
        if size_counter > 95000000:
            size_counter = 0
            converted_path += 'I'
            os.mkdir(converted_path)
            Title = Title[:-2] + str(Title_Counter + 1) + '\n'
            TitleU = TitleU[:-2] + str(Title_Counter + 1) + '\n'
        