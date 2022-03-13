import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class displayMatplotlib:
    # punkter hvor parameter fremstillingen for en kule skal regnes ut for å skape planetene
    m1, m2 = np.mgrid[0 : 2 * np.pi : 20j, 0 : np.pi : 10j]
    ax = []  # array for akser for lett hondtering
    axViewborder = [
        5e8 / 2,
        12e12 / 2,
        5e11 / 2,
    ]  # bestemmer hvor mye av solsystemet man skal se i hver akse

    focus = [3, 0, 0]
    # renderFilter = [["Earth", "Moon"], ["Sun", "Mercury","Venus","Earth", "Moon", "Mars", ], None] # None = no filter = render all
    renderFilter = [
        [3, 4],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0, 1, 2, 3, 4, 5],
    ]  # None = no filter = render all

    def __init__(
        self,
        solar_system,
        displaySizeMeters,
        save=False,
        saveAs=r"./animation.gif",
    ):

        self.solar_system = solar_system
        self.size = displaySizeMeters  # størrelse på universet
        # ved numerisk løsning antall iterasjoner per frame, viktig for matplotlib siden treg i forhold til simulasjon men kan simulere f.eks hver time og plotte hver dag
        self.save_gif = save  # lagre som gif
        self.saveAs = saveAs

        # initialiserer og styler matplotlib plot
        self.fig = plt.figure(figsize=(13, 8))
        plt.style.use("dark_background")
        self.fig.patch.set_facecolor("black")
        plt.rcParams["grid.color"] = (1, 1, 1, 0.1)
        self.fig.tight_layout()
        grid = self.fig.add_gridspec(2, 3)
        # plasserer aksene på et grid med definert posisjon og størrelse
        self.ax.append(self.fig.add_subplot(grid[0, 0:1], projection="3d"))
        self.ax.append(self.fig.add_subplot(grid[1:, 0:1], projection="3d"))
        self.ax.append(self.fig.add_subplot(grid[0:2, 1:3], projection="3d"))

        # 2d tekst for å plassere tekst i forhold til akse isteden for i 3d rom
        self.sim_time_label = self.ax[2].text2D(
            0, 0.95, "", transform=self.ax[2].transAxes
        )

        for i, axis in enumerate(self.ax):
            self.init_plots(
                i,
                -self.axViewborder[i],
                self.axViewborder[i],
                -self.axViewborder[i],
                self.axViewborder[i],
                -self.axViewborder[i],
                self.axViewborder[i],
                "Distance: (m)",
                "Distance: (m)",
                "Distance: (m)",
                "title",
                (0, 0, 0),
                45,
                45,
            )  # limits fixed later

    def init_plots(
        self,
        plot,
        xmin,
        xmax,
        ymin,
        ymax,
        zmin,
        zmax,
        xlabel,
        ylabel,
        zlabel,
        title,
        bgcolor,
        elevation,
        azimuth,
    ):
        # gjør repetetiv setup av akse
        self.ax[plot].set_xlim((xmin, xmax))
        self.ax[plot].set_ylim((ymin, ymax))
        self.ax[plot].set_zlim((zmin, zmax))
        self.ax[plot].set_xlabel(xlabel)
        self.ax[plot].set_ylabel(ylabel)
        self.ax[plot].set_zlabel(zlabel)
        self.ax[plot].w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0))
        self.ax[plot].w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0))
        self.ax[plot].w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0))
        # ax[plotx, ploty].grid()
        # ax[plotx,ploty].legend()
        self.ax[plot].set_title(title)
        self.ax[plot].view_init(elevation, azimuth)

    def init_objects(plot, body, index):
        body.sphere = []
        body.trace = []

        body.text = []

        # trenger en posisjonsarray for å se banene og trenger en per plot på grunn av offsett gjort for å få jorden i sentrum
        body.posarr = [[[], [], []], [[], [], []], [[], [], []]]

        foo = 2 * 1e8
        for plot, axis in enumerate(plot.ax):
            body.trace.append(
                axis.plot3D([], [], [], linewidth=1, color=body.color, label=body.name)
            )

            if index not in displayMatplotlib.renderFilter[plot]:
                body.sphere.append("empty")
                body.text.append("empty")
                continue
            x = np.cos(displayMatplotlib.m1) * np.sin(displayMatplotlib.m2)
            y = np.sin(displayMatplotlib.m1) * np.sin(displayMatplotlib.m2)
            z = np.cos(displayMatplotlib.m2)

            body.sphere.append(
                axis.plot_wireframe(
                    x,
                    y,
                    z,
                    rstride=1,
                    cstride=1,
                    color=body.color,
                    linewidth=0.25,
                    label=body.name,
                )
            )
            body.text.append(axis.text(*np.add(body.position, foo * 1e-2), body.name))

    def run(self):
        # kjører animasjon i matplotlib
        self.ax[2].legend(loc=1, fontsize="small")
        self.ani = animation.FuncAnimation(
            self.fig,
            self.updateMatplotlib,
            fargs=(),
            interval=1,
            save_count=1_00,
            frames=1_000,
            blit=True,
        )

        if self.save_gif:
            self.save()
        plt.show()

    def save(self):
        # set output file
        f = self.saveAs
        writer = animation.FFMpegWriter(fps=60, bitrate=18_000)
        self.ani.save(f)

    def updatePosArray(self, body, index):
        for i, axis in enumerate(self.ax):
            if index in self.renderFilter[i]:
                if self.focus[i] != None:  # hvis fokus på spesefikk planet

                    # print(self.solar_system.bodies[self.focus[i]].name)
                    if (
                        body is self.solar_system.bodies[self.focus[i]]
                    ):  # sjekker om minne addresse er lik altså samme objekt
                        position = [0, 0, 0]
                    # finner differanse fra jorden for de andre planetene
                    else:
                        position = [
                            body.position[0]
                            - self.solar_system.bodies[self.focus[i]].position[
                                0
                            ],
                            body.position[1]
                            - self.solar_system.bodies[self.focus[i]].position[
                                1
                            ],
                            body.position[2]
                            - self.solar_system.bodies[self.focus[i]].position[
                                2
                            ],
                        ]
                else:
                    position = body.position

                body.posarr[i][0].append(position[0])
                body.posarr[i][1].append(position[1])
                body.posarr[i][2].append(position[2])



    def updateMatplotlib(self, framenum):
        self.solar_system.iterator = framenum
        self.solar_system.update()

        # earth orbit seems to be about 367 days in model
        self.sim_time_label.set_text(f"{self.solar_system.timeUnit}: {framenum}")

        for int, body in enumerate(self.solar_system.bodies):
            self.updatePosArray(body, int) # brukes til å lage banen men opdateres bare per frame ikke per utregning
            for plot, axis in enumerate(self.ax):

                if int in self.renderFilter[plot]:
                    position= [body.posarr[plot][0][-1], body.posarr[plot][1][-1],body.posarr[plot][2][-1]]

                    # blitting i 3d plot ser ikke ut til å være støttet av matplotlib så må fjerne det forige kule meshet og plotte det på nytt som skader ytelsen
                    axis.collections.remove(body.sphere[plot])

                    radiusadder = [
                        2e7,
                        2e11,
                        1.2e10,
                    ]  # avhenging av hvilke planeter som er synelig og distansen fra disse planetene må de forstørres for å være mulig å see, valgte å addere en spesifisert mengde til radiusen i stedet for å multiplisere siden på denne måten minker differansen mellom de største og de minste planetene i stedet for at f.eks solen sluker alle planetene mens månen fortsatt er mindre en en piksel

                    # parameter fremsitilling av en kule
                    x = position[0] + (
                        (body.radius + radiusadder[plot])
                        * np.cos(self.m1)
                        * np.sin(self.m2)
                    )
                    y = position[1] + (
                        (body.radius + radiusadder[plot])
                        * np.sin(self.m1)
                        * np.sin(self.m2)
                    )
                    z = position[2] + (
                        (body.radius + radiusadder[plot]) * np.cos(self.m2)
                    )
                    # ploter mesh som wireframe
                    body.sphere[plot] = axis.plot_wireframe(
                        x,
                        y,
                        z,
                        rstride=1,
                        cstride=1,
                        color="b",
                        linewidth=0.25,
                        facecolor=body.color,
                        antialiased=True,
                    )

                    # ploter banen planeten har dratt siden starten av simulasjonen
                    body.trace[plot][0].set(
                        data_3d=(
                            body.posarr[plot][0],
                            body.posarr[plot][1],
                            body.posarr[plot][2],
                        ),
                        color=body.color,
                    )

                    textOffset = [1e8, 7e11, 7e11]

                    # blitting ikke mulig
                    axis.texts.remove(body.text[plot])
                    body.text[plot] = axis.text(
                        *np.add(body.position, textOffset[plot] * 1e-1), body.name
                    )

        return self.ax


if __name__ == "__main__":
    import config

    config.main()
