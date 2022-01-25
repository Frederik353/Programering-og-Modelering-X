
from solar_system_3d import SolarSystem, Sun, Planet

solar_system = SolarSystem(5e11)
# solar_system = SolarSystem(400, projection_2d=False)

suns = (
    Sun(solar_system, 2e30,position=(0, 0, 0), velocity=(0, 0, 0)),
    # Sun(solar_system, position=(-40, -40, 40), velocity=(-6, 0, -6)),
)

planets = (
    Planet( solar_system, 6e24, position=( 0, 1.5e11, 0), velocity=(30000,0,0),radius=1e11),

    # Planet( solar_system, 20, position=(0, 0, 0), velocity=(-11, 11, 0),),
)

solar_system.run()
