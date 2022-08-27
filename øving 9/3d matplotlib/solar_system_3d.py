import numpy as np

from vectors import Vector
from displayMatplotlib import displayMatplotlib
from displayPygame import displayPygame
from rk4 import RK4_integrator


class SolarSystem:
    running = True
    paused = False

    def __init__(
        self,
        displaySizeMeters,
        iterPerFrame=10,
        timestepSec=8.64e4,
        timeDivisor=1,
        timeUnit="Days",
        euler=False,
        rk4=False,
        displayWithMatplotlib=False,
        displayWithPygame=False,
        save=False,
        saveAs=r"./animation.gif",
    ):

        self.size = displaySizeMeters  # størrelse på universet
        # ved numerisk løsning antall iterasjoner per frame, viktig for matplotlib siden treg i forhold til simulasjon men kan simulere f.eks hver time og plotte hver dag for mer nøyaktighet
        self.iterPerFrame = iterPerFrame
        self.euler = euler  # bruk euler metoden for integrasjon
        self.rk4 = rk4  # bruk runge kutta 4 for integrasjon
        self.displayWithMatplotlib = (
            displayWithMatplotlib  # vis simulasjon med matpltlib
        )
        self.displayWithPygame = displayWithPygame  # vis animasjon med pygame
        self.save = save  # lagre som gif
        self.saveAs = saveAs
        # siden matplotlib bruker en egen iterator for å kjøre funksjonene sine)
        self.iterator = 0
        self.timestepSec = timestepSec
        self.timeUnit = timeUnit
        self.timeDivisor = timeDivisor

        self.bodies = []

        if displayWithMatplotlib:
            self.plot = displayMatplotlib(
                self,
                self.size,
                self.save,
                self.saveAs,
            )
        if displayWithPygame:
            self.pygame = displayPygame(
                self,
                self.size,
            )
        if self.rk4:
            self.rk4 = RK4_integrator(self.timestepSec, self.bodies)

    def add_body(self, body):
        self.bodies.append(body)

    def calculate_all_body_interactions(self):
        # looper over alle legemene og regner ut akselerasjonen mellom dem samt summerer med resultat fra de andre legemene
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                first.accelerate_due_to_gravity(second)
        for int, body in enumerate(self.bodies):
            body.move(int)

    def run(self):
        self.framenum = 0
        if self.displayWithMatplotlib:
            self.plot.run()
        elif self.displayWithPygame:
            self.clock()

    def clock(self):
        while self.running:
            if not self.paused:
                self.framenum += 1
                self.update()
            self.pygame.updatePygame(self.framenum)

    def update(self):
        if self.rk4:
            for i in range(self.iterPerFrame):
                self.calculate_all_body_interactions()
                self.rk4.compute_gravity_step()
                for body in self.bodies:
                    body.posarr[0].append(body.position[0])
                    body.posarr[1].append(body.position[1])
        else:
            for i in range(self.iterPerFrame):
                self.calculate_all_body_interactions()
                for body in self.bodies:
                    body.posarr[0].append(body.position[0])
                    body.posarr[1].append(body.position[1])


class SolarSystemBody:
    def __init__(
        self,
        solar_system,
        mass=1e20,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        radius=1e10,
        color="magenta",
        name="Unknown",
    ):

        self.solar_system = solar_system
        self.mass = mass  # massen til legeme
        self.position = position  # nåverende possisjon til legeme
        self.velocity = Vector(velocity)  # nåverende farst vektor
        self.color = color  # farge for display
        self.name = name
        self.radius = radius  # opprinnelig radius, må ofte forstørres

        self.timestepSec = (
            self.solar_system.timestepSec
        )  # antall sek i en dag, extrapolerer vektoren for det neste sekundet i simulasjonen til den neste dagen, ikke helt nøyaktig men nødvending, påvirker planetene med minst bane mest som F.eks månen

        if solar_system.displayWithMatplotlib:
            displayMatplotlib.init_objects(
                self.solar_system.plot, self, len(self.solar_system.bodies)
            )
        if solar_system.displayWithPygame:
            displayPygame.init_objects(
                self.solar_system.pygame, self, len(self.solar_system.bodies)
            )
        self.posarr = [[], [], []]
        # lagrer en verdi fra start for å hindre bane tegnigen i å krasje
        self.posarr[0].append(self.position[0])
        self.posarr[1].append(self.position[1])

        # legger til seg selv i solsytemet
        self.solar_system.add_body(self)

    def move(self, index):
        self.position = (
            self.position[0] + self.velocity[0] * self.timestepSec,
            self.position[1] + self.velocity[1] * self.timestepSec,
            self.position[2] + self.velocity[2] * self.timestepSec,
        )

    def accelerate_due_to_gravity(self, other):
        # finner akselerasjon mellom to legemer
        # viktig å huske at mange av variablene brukt her er instanser av vektor klassen jeg laget med såkalte magic operatorer som vil si at variablene egentlig er arrayer og f.eks + vil gi vektor summen i stedet for den vanlige summen mellom to tall

        # få en vektor som peker fra det ene til det andre legemet siden dette vil retningen akselerasjonen virker i
        distance = Vector(other.position) - Vector(self.position)
        distance_mag = distance.get_magnitude()

        G = 6.67408e-11  # m**3 kg**-1 s**-2,  gravitasjonskonstanten

        # finner magnituden på kraftvektoren mellom legemene
        force_mag = G * (self.mass * other.mass / (distance_mag**2))
        # normaliserer vektorene for å få en retningsvektor med lengde 1 og ganger dette med keaftvektor lengden for å få kraftvektoren
        force = (distance.normalize() * force_mag)

        reverse = 1
        for body in self, other:
            acceleration = force / body.mass  # finner akselerasjon ved formel
            # extrapolerer akselerasjon til en dag og gjør legger til på farten samt reverserer akselerasjonen for det andre legemet
            body.velocity += acceleration * (reverse * self.timestepSec)
            reverse = -1


# hvis man kjører denne filen vil den automatisk finne config filen og kjøre den i stedet, gjort for enkelhet så jeg sliper å bytte fil men kan heller bruke en vim shortcut jeg har laget for å kjøre filen som er åpen
if __name__ == "__main__":
    import config

    config.main()
