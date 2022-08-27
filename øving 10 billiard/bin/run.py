import psim.engine as engine



config = ["masse", "15_break", "bank"]
current_config = config[1]
continuize = True
continuize_timestep = 0.01


if __name__ == '__main__':
    sim = engine.ShotSimulation()

    sim.setup_test(current_config)

    sim.simulate(name=current_config, time=None)

    if continuize:
        sim.continuize(continuize_timestep)

    from psim.ani.animate2d import AnimateShot

    ani = AnimateShot(sim)
    ani.start()
