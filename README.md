# Dungeon-Crusader
Start modules/main.py to play

This repo is not maintained any more. The project is getting refactored and is moved to:
https://github.com/MattR0se/DungeonCrusaderV03

or


```shell
pip3 install -r requirements.txt 
python3 modules/main.py
```


![image](https://github.com/humbertodias/pygame-dungeon-crusader/assets/9255997/5be6593b-b4d2-4681-8b3d-cd858b325a78)


Required modules: pygame (https://www.pygame.org/wiki/GettingStarted)

Requires python 3.x

### Controls:
| key | action|
|-----|-------|
| ARROW KEYS| move the player|
| Z (Y on QWERTZ keyboard)| Item A |
| X | Item B |
| ENTER | Interact (Doors, Chest etc.) |
| ESC | open inventory |
| F6 | quicksave (might crash the game!)|
| F9| quickload |
| H | debug mode |

### Controls in debug mode:
| key | action|
|-----|-------|
|F4 | slow motion mode (5 FPS)|
|PAGEUP/PAGEDOWN | add/remove items|
|F12 | save dungeon image as png (freezes the game) |
| V | Display/hide enemy aggro radius|
| K | kill all enemies on the screen |




Format
```
pip3 install yapf
yapf -i game.py
```

# Tools

[Tiled](https://www.mapeditor.org)
