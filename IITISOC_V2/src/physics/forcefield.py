"""
Research V2

Forcefield Parameters
"""


class ForceField:

    def __init__(self):

        # -------- LJ / WCA ----------

        self.sigma = 1.0

        self.epsilon = 1.0

        self.cutoff = 2.0 ** (1.0 / 6.0)

        # -------- FENE ----------

        self.K = 30.0

        self.R0 = 1.5

        # -------- Angle ----------

        self.angle_K = 1.5

        self.theta0 = 180.0

        # -------- Dynamics ----------

        self.temperature = 1.0

        self.dt = 0.005
