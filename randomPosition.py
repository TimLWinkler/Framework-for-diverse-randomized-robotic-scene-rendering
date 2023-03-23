import nvisii as nv

# just a test to check the coordinates (x=red, y=green, z=blue)

nv.initialize(headless=True)

camera = nv.entity.create(
    name='camera',
    transform=nv.transform.create('camera'),
    camera=nv.camera.create_from_fov(
        name='camera',
        field_of_view=0.78,
        aspect=1
    )
)

nv.set_camera_entity(camera)

camera.get_transform().look_at(
    at=[0, 0, 0],
    up=[0, 0, 1],
    eye=[5, 5, 5]
)

light = nv.entity.create(
    name="light",
    light=nv.light.create('light'),
    transform=nv.transform.create(
        name="light",
        position=[1, 3, 1]
    )
)
light_light = nv.light.get('light')
light_light.set_temperature(1000)
light_light.set_intensity(5)


lineX = nv.entity.create(name="LX")
lineX.set_mesh(
    nv.mesh.create_line("LX", nv.vec3(0, 0, 0), nv.vec3(3, 0, 0), 0.03)
)
lineX.set_transform(
    nv.transform.create('LX')
)
lineX.set_material(
    nv.material.create('LX')
)
lineX_material = nv.material.get('LX')
lineX_material.set_base_color([1, 0, 0])

lineY = nv.entity.create(name="LY")
lineY.set_mesh(
    nv.mesh.create_line("LY", nv.vec3(0, 0, 0), nv.vec3(0, 3, 0), 0.03)
)
lineY.set_transform(
    nv.transform.create('LY')
)
lineY.set_material(
    nv.material.create('LY')
)
lineY_material = nv.material.get('LY')
lineY_material.set_base_color([0, 1, 0])

lineZ = nv.entity.create(name="LZ")
lineZ.set_mesh(
    nv.mesh.create_line("LZ", nv.vec3(0, 0, 0), nv.vec3(0, 0, 3), 0.03)
)
lineZ.set_transform(
    nv.transform.create('LZ')
)
lineZ.set_material(
    nv.material.create('LZ')
)
lineZ_material = nv.material.get('LZ')
lineZ_material.set_base_color([0, 0, 1])

nv.enable_denoiser()
#
# TODO: use forLoop to render
#

nv.render_to_file(
    width=500,
    height=500,
    samples_per_pixel=10,
    file_path="randomCam/coordinates0.png"
)

camera.get_transform().look_at(
    at=[0, 0, 0],
    up=[0, 0, 1],
    eye=[-5,5,5]
)
nv.render_to_file(
    width=500,
    height=500,
    samples_per_pixel=10,
    file_path="randomCam/coordinates1.png"
)

camera.get_transform().look_at(
    at=[0, 0, 0],
    up=[0, 0, 1],
    eye=[-5,-5,5]
)
nv.render_to_file(
    width=500,
    height=500,
    samples_per_pixel=20,
    file_path="randomCam/coordinates2.png"
)

camera.get_transform().look_at(
    at=[0, 0, 0],
    up=[0, 0, 1],
    eye=[5,-5,5]
)
nv.render_to_file(
    width=500,
    height=500,
    samples_per_pixel=10,
    file_path="randomCam/coordinates3.png"
)

nv.deinitialize()