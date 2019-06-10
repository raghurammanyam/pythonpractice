# import soundfile as sf



# data, samplerate = sf.read('./existing_file.mp3')
# sf.write('./new_file.wav', data, samplerate)
# import myspsolution as mysp
mysp=__import__("my-voice-analysis")
p="ram" # Audio File title
c='/home/caratred/pythonpractice'
print(mysp.myspgend(p,c))
print(mysp.mysppaus(p,c))