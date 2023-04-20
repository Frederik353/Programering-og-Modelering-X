import sim.engine as engine



config = ["masseskudd", "åpningsskudd", "veggskudd"]
current_config = config[0]
continuize = True
continuize_tidstep = 0.01


if __name__ == '__main__':
    sim = engine.SkuddSimulasjon()

    sim.setup_test(current_config)

    sim.simuler(name=current_config, tid=None)

    if continuize:
        sim.continuize(continuize_tidstep)

    from sim.animering.animer import AnimerSkudd

    ani = AnimerSkudd(sim)
    ani.start()
