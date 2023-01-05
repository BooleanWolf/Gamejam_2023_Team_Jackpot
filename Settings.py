import json


MAX_LEVELS = 3

############################################################# Character ###################################################\
with open("local_variable.json", "r") as openfile:
    json_obj = json.load(openfile)
    print(json_obj)

PLAYER_TYPE = json_obj["PLAYER_TYPE"]
ENEMY_TYPE = "EnemyBorg"


############################################################## Display ####################################################
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

SCROLL_THRESH = 400

ROWS = 16
COLS = 150
LEVEL = 0
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21

########################################################## PHYSICS ###########################################################
GRAVITY = 0.75



######################################################### SCALE ##############################################################
EXPLOSION_SCALE = 1