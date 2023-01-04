import json


############################################################# Character ###################################################\
with open("local_variable.json", "r") as openfile:
    json_obj = json.load(openfile)
    print(json_obj)

PLAYER_TYPE = json_obj["PLAYER_TYPE"]
ENEMY_TYPE = "EnemyBorg"


############################################################## Display ####################################################
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
FPS = 60

ROWS = 16
COLS = 150
LEVEL = 1
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21

########################################################## PHYSICS ###########################################################
GRAVITY = 0.75



######################################################### SCALE ##############################################################
EXPLOSION_SCALE = 1