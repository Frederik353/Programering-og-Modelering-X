import psim
import psim.utils as utils
import psim.physics as physics
import psim.configurations as configurations

from psim.objects import (
    Ball,
    Table,
    Cue,
)

import numpy as np


class Event(object):
    def __init__(self, event_type, agents, tau):
        self.agents = agents
        self.tau = tau
        self.event_type = event_type


class ShotHistory(object):
    """Track the states of balls over time"""

    def __init__(self):

        self.balls = {}
        self.reset_history()

    def reset_history(self):
        self.vectorized = False

        self.history = {
            'balls': {},
            'index': [],
            'time': [],
            'event': [],
        }

        self.n = -1
        self.time = 0

        self.touch_history()

    def touch_history(self):
        """Initializes ball trajectories if they haven't been initialized"""

        for ball_id in self.balls:
            if ball_id not in self.history['balls']:
                self.init_ball_history(ball_id)

    def init_ball_history(self, ball_id):
        """Adds a new ball to the trajectory. Adds nans if self.n > 0"""

        if ball_id not in self.balls:
            raise ValueError(
                f"ShotHistory.init_ball_history :: {ball_id} not in self.balls")

        self.history['balls'][ball_id] = {
            's': [np.nan] * self.n,
            'svw': [np.nan * np.ones((4, 3))] * self.n,
            'euler': [np.nan * np.ones((4, 3))] * self.n,
            'quat': [np.nan * np.ones((4, 4))] * self.n,
        }

    def timestamp(self, dt, event=None):
        # update time
        self.n += 1
        self.time += dt

        # log time
        self.history['time'].append(self.time)
        self.history['index'].append(self.n)

        # log event
        self.history['event'].append(event)

        # log ball states
        for ball_id, ball in self.balls.items():
            self.history['balls'][ball_id]['s'].append(ball.s)
            self.history['balls'][ball_id]['svw'].append(ball.svw)

    def continuize(self, dt=0.05):
        old_n = self.n
        old_history = self.history
        self.reset_history()

        # Set and log balls to the initial state
        self.set_table_state_via_history(index=0, history=old_history)
        self.timestamp(0)

        dt_prime = dt
        for index, event in zip(old_history['index'], old_history['event']):

            if not isinstance(event, Event):
                continue

            if event.tau == np.inf:
                break

            # Evolve in steps of dt up to the event
            event_time = 0
            while event_time < (event.tau - dt_prime):
                self.evolve(dt_prime, log=False)
                self.timestamp(dt, event=None)
                event_time += dt_prime

                dt_prime = dt

            dt_prime = dt - (event.tau - event_time)
            # Set and log balls to the resolved state of the event
            self.set_table_state_via_history(index=index, history=old_history)

        self.vectorize_history()

    def set_table_state_via_history(self, index, history=None):
        if history is None:
            history = self.history

        for ball_id, ball in self.balls.items():
            ball.set(
                history['balls'][ball_id]['svw'][index],
                history['balls'][ball_id]['s'][index],
            )

    def vectorize_history(self):

        self.history['index'] = np.array(self.history['index'])
        self.history['time'] = np.array(self.history['time'])
        for ball in self.history['balls']:
            self.history['balls'][ball]['s'] = np.array(
                self.history['balls'][ball]['s'])
            self.history['balls'][ball]['svw'] = np.array(
                self.history['balls'][ball]['svw'])
            self.history['balls'][ball]['euler'] = np.array(
                self.history['balls'][ball]['euler'])
            self.history['balls'][ball]['quat'] = np.array(
                self.history['balls'][ball]['quat'])

        self.vectorized = True


class ShotSimulation(ShotHistory):
    def __init__(self, g=None):
        self.g = g or psim.g

        self.cue = None
        self.table = None

        ShotHistory.__init__(self)

    def simulate(self, time=None, name='NA'):
        self.touch_history()

        event = Event(event_type=None, agents=tuple(), tau=0)

        self.timestamp(0, event)
        while event.tau < np.inf:
            event = self.get_next_event()
            self.evolve(dt=event.tau, event=event)

            if time is not None and self.time >= time:
                break

        self.vectorize_history()

    def set_cue(self, cue):
        self.cue = cue

    def set_table(self, table):
        self.table = table

    def set_balls(self, balls):
        self.balls = balls

    def evolve(self, dt, log=True, event=None):
        for ball_id, ball in self.balls.items():
            svw, s = physics.evolve_ball_motion(
                state=ball.s,
                svw=ball.svw,
                R=ball.R,
                m=ball.m,
                u_g=self.table.u_g,
                u_sp=self.table.u_sp,
                u_r=self.table.u_r,
                g=self.g,
                t=dt,
            )
            ball.set(svw, s)

        if event is not None:
            self.resolve(event)

        if log:
            self.timestamp(dt, event=event)

    def resolve(self, event):
        if not event.event_type:
            return

        if event.event_type == 'ball-ball':
            ball_id1, ball_id2 = event.agents

            svw1 = self.balls[ball_id1].svw
            svw2 = self.balls[ball_id2].svw

            svw1, svw2 = physics.resolve_ball_ball_collision(svw1, svw2)
            s1, s2 = psim.glidende, psim.glidende

            self.balls[ball_id1].set(svw1, s1)
            self.balls[ball_id2].set(svw2, s2)

        elif event.event_type == 'ball-rail':
            ball_id, rail_id = event.agents

            ball = self.balls[ball_id]
            rail = self.table.rails[rail_id]

            svw = self.balls[ball_id].svw
            normal = self.table.rails[rail_id].normal

            svw = physics.resolve_ball_rail_collision(
                svw=ball.svw,
                normal=rail.normal,
                R=ball.R,
                m=ball.m,
                h=rail.height,
            )
            s = psim.glidende

            self.balls[ball_id].set(svw, s)

    def get_next_event(self):
        tau_min = np.inf
        agents = tuple()
        event_type = None

        tau, ids, e = self.get_min_motion_event_time()
        if tau < tau_min:
            tau_min = tau
            event_type = e
            agents = ids

        tau, ids = self.get_min_ball_ball_event_time()
        if tau < tau_min:
            tau_min = tau
            event_type = 'ball-ball'
            agents = ids

        tau, ids = self.get_min_ball_rail_event_time()
        if tau < tau_min:
            tau_min = tau
            event_type = 'ball-rail'
            agents = ids

        return Event(event_type, agents, tau_min)

    def get_min_motion_event_time(self):
        """Returns minimum until next ball motion transition"""

        tau_min = np.inf
        ball_id = None
        event_type_min = None

        for ball in self.balls.values():
            if ball.s == psim.stille:
                continue
            elif ball.s == psim.rullende:
                tau = physics.get_roll_time(ball.svw, self.table.u_r, self.g)
                event_type = 'end-roll'
            elif ball.s == psim.glidende:
                tau = physics.get_slide_time(
                    ball.svw, ball.R, self.table.u_g, self.g)
                event_type = 'end-slide'
            elif ball.s == psim.spinnende:
                tau = physics.get_spin_time(
                    ball.svw, ball.R, self.table.u_sp, self.g)
                event_type = 'end-spin'

            if tau < tau_min:
                tau_min = tau
                ball_id = ball.id
                event_type_min = event_type

        return tau_min, (ball_id, ), event_type_min

    def get_min_ball_ball_event_time(self):
        """Returns minimum time until next ball-ball collision"""

        tau_min = np.inf
        ball_ids = tuple()

        for i, ball1 in enumerate(self.balls.values()):
            for j, ball2 in enumerate(self.balls.values()):
                if i >= j:
                    continue

                if ball1.s == psim.stille and ball2.s == psim.stille:
                    continue

                tau = physics.get_ball_ball_collision_time(
                    svw1=ball1.svw,
                    svw2=ball2.svw,
                    s1=ball1.s,
                    s2=ball2.s,
                    mu1=(self.table.u_g if ball1.s ==
                         psim.glidende else self.table.u_r),
                    mu2=(self.table.u_g if ball2.s ==
                         psim.glidende else self.table.u_r),
                    m1=ball1.m,
                    m2=ball2.m,
                    g=self.g,
                    R=ball1.R
                )

                if tau < tau_min:
                    ball_ids = (ball1.id, ball2.id)
                    tau_min = tau

        return tau_min, ball_ids

    def get_min_ball_rail_event_time(self):
        """Returns minimum time until next ball-rail collision"""

        tau_min = np.inf
        agent_ids = (None, None)

        for ball in self.balls.values():
            if ball.s == psim.stille:
                continue

            for rail in self.table.rails.values():
                tau = physics.get_ball_rail_collision_time(
                    svw=ball.svw,
                    s=ball.s,
                    lx=rail.lx,
                    ly=rail.ly,
                    l0=rail.l0,
                    mu=(self.table.u_g if ball.s ==
                        psim.glidende else self.table.u_r),
                    m=ball.m,
                    g=self.g,
                    R=ball.R
                )

                if tau < tau_min:
                    agent_ids = (ball.id, rail.id)
                    tau_min = tau

        return tau_min, agent_ids

    def setup_test(self, setup='masse'):
        self.cue = Cue()
        self.balls = {}

        if setup == 'masse':
            self.table = Table()
            self.balls['cue'] = Ball('cue')
            self.balls['cue'].svw[0] = [
                self.table.center[0], self.table.B+0.33, 0]

            self.balls['8'] = Ball('8')
            self.balls['8'].svw[0] = [self.table.center[0], 1.6, 0]

            self.balls['3'] = Ball('3')
            self.balls['3'].svw[0] = [self.table.center[0]*0.70, 1.6, 0]

            self.cue.strike(
                ball=self.balls['cue'],
                V0=2.9,
                phi=80.746,
                theta=80,
                a=0.2,
                b=0.0,
            )
        elif setup == 'bank':
            self.table = Table()
            self.balls['cue'] = Ball('cue')
            self.balls['cue'].svw[0] = [
                self.table.center[0], self.table.T-0.6, 0]

            self.cue.strike(
                ball=self.balls['cue'],
                V0=0.6,
                phi=90,
                a=0.7,
                b=0.7,
                theta=0,
            )

        elif setup == '15_break':
            self.table = Table()

            self.balls['1'] = Ball('1')
            self.balls['2'] = Ball('2')
            self.balls['3'] = Ball('3')
            self.balls['4'] = Ball('4')
            self.balls['5'] = Ball('5')
            self.balls['6'] = Ball('6')
            self.balls['7'] = Ball('7')
            self.balls['8'] = Ball('8')
            self.balls['9'] = Ball('9')
            self.balls['10'] = Ball('10')
            self.balls['11'] = Ball('11')
            self.balls['12'] = Ball('12')
            self.balls['13'] = Ball('13')
            self.balls['14'] = Ball('14')
            self.balls['15'] = Ball('15')

            c = configurations.FifteenBallRack(list(self.balls.values()),
                                               spacing_factor=1e-6,
                                               ordered=True
                                               )

            c.arrange()
            c.center_by_table(self.table)

            self.balls['cue'] = Ball('cue')
            self.balls['cue'].svw[0] = [self.table.center[0], self.table.T*2/8, 0]

            self.cue.strike_object(
                ball=self.balls['cue'],
                obj=self.balls['1'],
                offset=0,
                V0=8.50001,
                a=0.05,
                b=0.05,
                theta=0,
            )
