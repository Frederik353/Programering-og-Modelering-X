

from solar_system_3d import SolarSystem, Sun, Planet


def main():
    # solar_system = SolarSystem(11 * 1e12, save=False)
    # solar_system = SolarSystem(5 * 1e11, save=False)
    solar_system = SolarSystem(5 * 1e11, save=True)

    suns = (
        Sun(solar_system, position=(1.81899e8, 9.83630e8, -1.58778e7), velocity=(-1.12474e1,
                                                                                 7.54876, 2.68723e1), mass=1.98854e30, radius=6.95500e8, color="yellow", name="Sun"),
    )

    planets = (
        Planet(solar_system, position=(-5.67576e10, -2.73592e10, 2.89173e09), velocity=(1.16497e04, -
                                                                                        4.14793e04, -4.45952e03), mass=3.30200e23, radius=2.44000e06, color="grey", name="Mercury"),
        Planet(solar_system, position=(4.28480e10, 1.00073e11, -1.11872e09), velocity=(-3.22930e04,
                                                                                       1.36960e04, 2.05091e03), mass=4.86850e24, radius=6.05180e06, color="chocolate", name="Venus"),
        Planet(solar_system, position=(-1.43778e11, -4.00067e10, -1.38875e07), velocity=(7.65151e03, -
                                                                                         2.87514e04, 2.08354e00), mass=5.97219e24, radius=6.37101e06, color="mediumaquamarine", name="Earth"),
        Planet(solar_system, position=(-1.438429539096973e11, -4.040159702132421e10, 1.405778659853712e7), velocity=(8.607787839789614e3, -
                                                                                                                     2.894287262169313e4, -4.929441849033722e-00), mass=7.349*10e22, radius=1737.4, color="darkgrey", name="Moon"),
        Planet(solar_system, position=(-1.14746e11, -1.96294e11, -1.32908e09), velocity=(2.18369e04, -
                                                                                         1.01132e04, -7.47957e02), mass=6.41850e23, radius=3.38990e06, color="orangered", name="Mars"),
        Planet(solar_system, position=(-5.66899e11, -5.77495e11, 1.50755e10), velocity=(9.16793e03, -
                                                                                        8.53244e03, -1.69767e02), mass=1.89813e27, radius=6.99110e07, color="peachpuff", name="Jupiter"),
        Planet(solar_system, position=(8.20513e10, -1.50241e12, 2.28565e10), velocity=(9.11312e03,
                                                                                       4.96372e02, -3.71643e02), mass=5.68319e26, radius=5.82320e07, color="bisque", name="Saturn"),
        Planet(solar_system, position=(2.62506e12, 1.40273e12, -2.87982e10), velocity=(-3.25937e03,
                                                                                       5.68878e03, 6.32569e01), mass=8.68103e25, radius=2.53620e07, color="paleturquoise", name="Uranus"),
        Planet(solar_system, position=(4.30300e12, -1.24223e12, -7.35857e10), velocity=(1.47132e03,
                                                                                        5.25363e03, -1.42701e02), mass=1.02410e26, radius=2.46240e07, color="dodgerblue", name="Neptune"),
        Planet(solar_system, position=(1.65554e12, -4.73503e12, 2.77962e10), velocity=(5.24541e03,
                                                                                       6.38510e02, -1.60709e03), mass=1.30700e22, radius=1.19500e06, color="darkred", name="Pluto"),
    )

    solar_system.run()

# BODY PX PY PZ VX VY VZ MASS RADIUS


if __name__ == "__main__":
    main()
