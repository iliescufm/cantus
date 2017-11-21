#!/usr/bin/python

#   Cantus - music player developed in python by Mihai Iliescu
#   version: v0.1
#   date:   21 November 2017
#   (c) 2017, s.c. Info-Logica Silverlie s.r.l.
#   www.infologica.ro

#   usage:
#       python cantus.py path_to_music_folder
#   


import sys,  os, magic, pygame

pygame.init()
pygame.display.set_caption('Cantus')

sx = 500
sy = 20

screen = pygame.display.set_mode((sx, sy), pygame.RESIZABLE)
screen.fill((30, 200, 250))

path = ''
cwd = os.getcwd()

if  len(sys.argv)>1: path = sys.argv[1]
else: path = cwd

_songs = []

for root, subdirs, files in os.walk(path):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        file_type = magic.from_file(file_path)
        if 'Audio' in file_type:
            _songs.append(file_path)

print _songs

SONG_END = pygame.USEREVENT + 1

mu = pygame.mixer
mu.music.set_endevent(SONG_END)
mu.init()

done = False
_pause = False

clock = pygame.time.Clock()
font = pygame.font.SysFont("Ubuntu", 18)

def displayCenterText(txt):
    text = font.render(txt, True, (0, 228, 220))
    screen.fill((55, 55, 55))
    tx = text.get_width()
    ty = text.get_height()
    screen.blit(text, ((sx-tx)//2, (sy-ty)//2))
    pygame.display.flip()

displayCenterText("Cantus v0.0.1")

def stopPlaying(mu):
    mu.music.stop()
    return True
    
def pausePlaying(mu):
    global _pause
    if not _pause: 
        mu.music.pause()
        _pause = True
    else:
        mu.music.unpause()
        _pause = False
    return True

def playSong(mx, s):
    mu.music.stop()
    mx.music.load(s)
    mx.music.play()
    displayCenterText(os.path.basename(s))


def playPreviousSong(mx):
    global _songs
    _songs = [_songs[-1]] + _songs[:-1]
    playSong(mx, _songs[0])
    return True
    
def playNextSong(mx):
    global _songs
    _songs = _songs[1:] + [_songs[0]]
    playSong(mx, _songs[0])
    return True

playNextSong(mu)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            stopPlaying(mu)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pausePlaying(mu)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            playPreviousSong(mu)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            playNextSong(mu)
        if event.type == SONG_END:
            playNextSong(mu)            
        if event.type ==  pygame.VIDEORESIZE:
            sx,  sy = event.size
            pygame.display.set_mode((sx, sy), pygame.RESIZABLE)
            displayCenterText(os.path.basename(_songs[0]))
            

    

    #clock.tick(60)    
