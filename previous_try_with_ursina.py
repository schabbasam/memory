from ursina import *

app = Ursina(title = "Effigies")


island = Entity(
    model=Cylinder(resolution=8),
    scale=(8, 1, 8),
    color=color.green,
    texture="white_cube",
    shader="lit_with_shadows_shader",
    collider='mesh'
)

# Sonnenlicht
sun = DirectionalLight()
sun.look_at(Vec3(1, -2, -1))
sun.shadows = True

# Grundbeleuchtung, damit Schatten nicht komplett schwarz sind
AmbientLight(color=color.rgba(100, 100, 100, 255))

# Maussteuerung aktivieren und Cursor verstecken
mouse.locked = True

# Fluggeschwindigkeit
speed = 4

def update():
    # Bewegung relativ zur Blickrichtung
    movement = Vec3(0, 0, 0)

    if held_keys['space']:
        movement += camera.forward
    if held_keys['w']:
        movement -= camera.forward
    if held_keys['r']:
        movement += camera.right
    if held_keys['e']:
        movement -= camera.right
    if held_keys['d']:
        movement += Vec3(0, 1, 0)
    if held_keys['s']:
        movement -= Vec3(0, 1, 0)

    # Diagonal nicht schneller fliegen
    if movement.length() > 0:
        camera.position += movement.normalized() * speed * time.dt

    camera.rotation_y += mouse.velocity[0] * 100
    camera.rotation_x -= mouse.velocity[1] * 100
    camera.rotation_x = clamp(camera.rotation_x, -89, 89)

def input(key):
    if key == "escape":
        application.quit()

app.run()

