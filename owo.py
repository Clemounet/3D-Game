from ursina import *

app = Ursina()

ground = Entity(
    model='cube',
    scale=(20, 1, 20),
    color=color.green,
    collider='box'
)

platforms = [
    Entity(model='cube', scale=(3, .5, 3), position=(4, 1, 0),
           color=color.gray, collider='box'),
    Entity(model='cube', scale=(2, .5, 2), position=(-3, 2, 0),
           color=color.gray, collider='box'),
    Entity(model='cube', scale=(2, .5, 2), position=(0, 4, 0),
           color=color.gray, collider='box')
]

player = Entity(
    model='cube',
    color=color.orange,
    scale=(1, 1, 1),
    position=(0, 5, 0),
    collider='box'
)

camera.parent = player
camera.position = (0, 5, -12)
camera.rotation_x = 20

speed = 5
gravity = 20
jump_force = 8

velocity_y = 0
grounded = False


def update():
    global velocity_y, grounded

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
    for entity in [ground] + platforms:
        if player.intersects(entity).hit:
            grounded = True
            velocity_y = 0
            player.y = entity.world_position.y + entity.scale_y / 2 + player.scale_y / 2
            break


def input(key):
    global velocity_y

    if key == 'space' and grounded:
        velocity_y = jump_force


app.run()