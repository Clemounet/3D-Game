from ursina import *
from math import sin, cos, radians, degrees, atan2, sqrt
from ursina.prefabs.button import Button
app = Ursina()

ground = Entity(
    model='cube',
    scale=(20, 1, 20),
    color=color.hex('#29914a'),
    collider='box'
)

platforms = [
    Entity(model='cube', scale=(3, .5, 3), position=(4, 1, 0),
           color=color.hex('#848a86'), collider='box'),
    Entity(model='cube', scale=(2, .5, 2), position=(-3, 2, 0),
           color=color.hex('#848a86'), collider='box'),
    Entity(model='cube', scale=(2, .5, 2), position=(0, 4, 0),
           color=color.hex('#848a86'), collider='box')
]

player = Entity(
    model='cube',
    color=color.orange,
    scale=(1, 1, 1),
    position=(0, 5, 0),
    collider='box'
)
from math import sin, cos, radians

camera_angle = 0      
camera_distance = 15  
camera_height = 4.5   

speed = 5
gravity = 20
jump_force = 8
velocity_y = 0
grounded = False
game_started = False

easter_image = Entity(
    parent=camera.ui,
    model='quad',
    texture='easter_egg.png',
    scale=(0.8, 0.8),
    enabled=False
)

def start_game():
    global game_started

    game_started = True

    play_button.disable()
    title.disable()

def show_easter_egg():
    title.disable()
    play_button.disable()
    easter_button.disable()

    easter_image.enable()
    back_button.enable()


def back_to_menu():
    easter_image.disable()
    back_button.disable()

    title.enable()
    play_button.enable()
    easter_button.enable()

title = Text(
    text="My Grosse Bite",
    origin=(0,0),
    scale=3,
    y=.25
)

play_button = Button(
    text="PLAY",
    scale=(0.3,0.1),
    color=color.azure,
    y=-0.1
)

easter_button = Button(
    text='Easter Egg',
    scale=(0.3, 0.1),
    color=color.orange,
    y=-0.25
)

back_button = Button(
    text='Back',
    scale=(0.2, 0.08),
    y=-0.4,
    enabled=False
)

back_button.on_click = back_to_menu
easter_button.on_click = show_easter_egg
play_button.on_click = start_game

def update():
    global velocity_y, grounded, camera_angle
    if not game_started:
        return
    move = Vec3(
        held_keys['d'] - held_keys['a'],
        0,
        held_keys['w'] - held_keys['s']
    )

    if move.length() > 0:
        move = move.normalized()

    player.position += move * speed * time.dt

    velocity_y -= gravity * time.dt
    player.y += velocity_y * time.dt

    grounded = False
    rotation_speed = 90
    for entity in [ground] + platforms:
        if player.intersects(entity).hit:
            grounded = True
            velocity_y = 0
            player.y = entity.world_position.y + entity.scale_y / 2 + player.scale_y / 2
            break

    if held_keys['left arrow']:
        camera_angle -= 100 * time.dt

    if held_keys['right arrow']:
        camera_angle += 100 * time.dt

    angle = radians(camera_angle)

    camera.position = (
        player.x + sin(angle) * camera_distance,
        player.y + camera_height,
        player.z - cos(angle) * camera_distance
    )

    target = player.position + Vec3(0, 1, 0)
    direction = target - camera.position

    yaw = degrees(atan2(direction.x, direction.z))
    pitch = -degrees(atan2(direction.y, sqrt(direction.x**2 + direction.z**2)))

    camera.rotation = (pitch, yaw, 0)
def input(key):
    global velocity_y

    if not game_started:
        return

    if key == 'space' and grounded:
        velocity_y = jump_force


app.run()