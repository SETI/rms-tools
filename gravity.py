#!/usr/bin/python
################################################################################
# gravity.py
#
# Classes and methods to deal with gravity fields of oblate planets.
#
# Mark R. Showalter, SETI Institute, March 2010
# Revised October 2011.
################################################################################
import numpy as np

PRECISION = 1.e-15      # Minimum allowed precision in semimajor axis solution
SOLVE_A_MAXITERS = 100  # Maximum allowed iterations in solve_a(). Should never
                        # be reached.

# Useful unit conversions
DPR = 180. / np.pi      # Converts radians to degrees
DPD = DPR * 86400.      # Converts radians per second to degrees per day 

class Gravity():
    """A class describing the gravity field of a planet."""

    def __init__(self, gm, jlist=[], radius=1.):
        """The constructor for a Gravity object.

        Input:
            gm          The body's GM in units of km^3/s^2
            jlist       optional list of even gravity harmonics: [jJ2, J4, ...].
            radius      body radius for associated J-values.
        """

        self.gm = gm
        self.jn = jlist
        self.rp = radius
        self.r2 = radius * radius

        # Evaluate coefficients for frequencies
        n = 0
        pn_zero = 1.
        omega_jn = []
        kappa_jn = []
        nu_jn    = []
        domega_jn = []
        dkappa_jn = []
        dnu_jn    = []
        for i in range(len(jlist)):
            n += 2          # i == 0 corresponds to J2; i == 1 to J4; etc.
            pn_zero = -(n-1.)/n * pn_zero

            omega_jn.append(      -(n+1) * pn_zero * jlist[i])
            kappa_jn.append( (n-1)*(n+1) * pn_zero * jlist[i])
            nu_jn.append(   -(n+1)*(n+1) * pn_zero * jlist[i])

            domega_jn.append(-(n+3) * omega_jn[i])
            dkappa_jn.append(-(n+3) * kappa_jn[i])
            dnu_jn.append(   -(n+3) * nu_jn[i])

        self.omega_jn  = np.array(omega_jn)
        self.kappa_jn  = np.array(kappa_jn)
        self.nu_jn     = np.array(nu_jn)
        self.domega_jn = np.array(domega_jn)
        self.dkappa_jn = np.array(dkappa_jn)
        self.dnu_jn    = np.array(dnu_jn)

    @staticmethod
    def _jseries(coefficients, ratio2):
        """Internal method to evaluate a series of the form:
                coefficients[0] * ratio2 + coefficients[1] * ratio2^2 ..."""

        return ratio2 * np.polyval(coefficients[::-1], ratio2)

    def omega(self, a):
        """Returns the mean motion (radians/s) at semimajor axis a."""

        a2 = a * a
        omega2 = self.gm/(a*a2) * (1. +
                                   Gravity._jseries(self.omega_jn, self.r2/a2))
        return np.sqrt(omega2)

    def kappa(self, a):
        """Returns the radial oscillation frequency (radians/s) at semimajor
        axis a."""

        a2 = a * a
        kappa2 = self.gm/(a*a2) * (1. +
                                   Gravity._jseries(self.kappa_jn, self.r2/a2))
        return np.sqrt(kappa2)

    def nu(self, a):
        """Returns the vertical oscillation frequency (radians/s) at semimajor
        axis a."""

        a2 = a * a
        nu2 = self.gm/(a*a2) * (1. +
                                Gravity._jseries(self.nu_jn, self.r2/a2))
        return np.sqrt(nu2)

    def domega_da(self, a):
        """Returns the radial derivative of the mean motion (radians/s/km) at
        semimajor axis a."""

        a2 = a * a
        domega2 = self.gm/(a2*a2) * (-3. +
                                   Gravity._jseries(self.domega_jn, self.r2/a2))
        return domega2 / (2. * self.omega(a))

    def dkappa_da(self, a):
        """Returns the radial derivative of the radial oscillation frequency
        (radians/s/km) at semimajor axis a."""

        a2 = a * a
        dkappa2 = self.gm/(a2*a2) * (-3. +
                                   Gravity._jseries(self.dkappa_jn, self.r2/a2))
        return dkappa2 / (2. * self.kappa(a))

    def dnu_da(self, a):
        """Returns the radial derivative of the vertical oscillation frequency
        (radians/s/km) at semimajor axis a."""

        a2 = a * a
        dnu2 = self.gm/(a2*a2) * (-3. +
                                  Gravity._jseries(self.dnu_jn, self.r2/a2))
        return dnu2 / (2. * self.nu(a))

    def combo(self, a, factors):
        """Returns a frequency combination, based on given coefficients for
        omega, kappa and nu. Full numeric precision is preserved in the limit
        of first- or second-order cancellation of the coefficients."""

        a2 = a * a
        ratio2 = self.r2 / a2
        gm_over_a3 = self.gm / (a * a2)

        sum_factors = 0
        sum_values = 0.

        # omega term
        if factors[0]:
            omega2_jsum = Gravity._jseries(self.omega_jn, ratio2)
            omega2 = gm_over_a3 * (1. + omega2_jsum)
            omega  = np.sqrt(omega2)

            sum_factors += factors[0]
            sum_values  += factors[0] * omega

        # kappa term
        if factors[1]:
            kappa2_jsum = Gravity._jseries(self.kappa_jn, ratio2)
            kappa2 = gm_over_a3 * (1. + kappa2_jsum)
            kappa  = np.sqrt(kappa2)

            sum_factors += factors[1]
            sum_values  += factors[1] * kappa

        # nu term
        if factors[2]:
            nu2_jsum = Gravity._jseries(self.nu_jn, ratio2)
            nu2 = gm_over_a3 * (1. + nu2_jsum)
            nu  = np.sqrt(nu2)

            sum_factors += factors[2]
            sum_values  += factors[2] * nu

        if sum_factors != 0: return sum_values

        # In the special cause where sum_factors = 0, we get cancellation to
        # leading order. We employ the following trick to improve accuracy.
        #
        # Because
        #   omega^2 - GM/a^3 = GM/a^3 * Jsum
        # we have
        #   [omega - sqrt(GM/a^3)] [omega + sqrt(GM/a^3)] = GM/a^3 * Jsum
        # or
        #   omega - sqrt(GM/a^3) = GM/a^3 * Jsum / [omega + sqrt(GM/a^3)]
        #
        # Similarly for kappa and nu. Our solution is to sum the quantities
        # (omega - sqrt(GM/a^3)), (kappa - sqrt(GM/a^3)) and (nu - sqrt(GM/a^3))
        # instead.

        sqrt_gm_over_a3 = np.sqrt(gm_over_a3)
        sum_values = 0.

        if factors[0]:
            omega_diff = gm_over_a3 * omega2_jsum / (omega + sqrt_gm_over_a3)
            sum_values += factors[0] * omega_diff

        if factors[1]:
            kappa_diff = gm_over_a3 * kappa2_jsum / (kappa + sqrt_gm_over_a3)
            sum_values += factors[1] * kappa_diff

        if factors[2]:
            nu_diff = gm_over_a3 * nu2_jsum / (nu + sqrt_gm_over_a3)
            sum_values += factors[2] * nu_diff

        if factors[1] != factors[2]: return sum_values

        # In the final special case where
        #   factors[1] = factors[2] = -factors[0]/2
        # we get still higher-order cancellation. We employ another trick. The
        # expression becomes
        #   -factors[1] (2 omega - kappa - nu)
        # 
        # Note that
        #   (2 omega - kappa - nu) (omega + kappa)
        #       = 2 omega^2 + omega kappa - omega nu - kappa^2 - kappa nu
        # Because
        #   2 omega^2 - kappa^2 = nu^2,
        # we get
        #   (2 omega - kappa - nu) (omega + kappa)
        #       = nu^2 + omega kappa - omega nu - kappa nu
        #       = (nu - omega) (nu - kappa)
        # Thus,
        #   2 omega - kappa - nu = (nu - omega) (nu - kappa) / (omega + kappa)

        if factors[1] == 0: return 0

        sum_values = -factors[1] * ((nu_diff - omega_diff)
                                 *  (nu_diff - kappa_diff)
                                 /  (omega + kappa))

        return sum_values

    def dcombo_da(self, a, factors):
        """Returns the radial derivative of a frequency combination, based on
        given coefficients for omega, kappa and nu. Unlike method combo(), this
        one does not guarantee full precision if the coefficients cancel to
        first or second order."""

        sum_values = 0.

        if factors[0]: sum_values += factors[0] * self.domega_da(a)
        if factors[1]: sum_values += factors[1] * self.dkappa_da(a)
        if factors[2]: sum_values += factors[2] * self.dnu_da(a)

        return sum_values

    def solve_a(self, freq, factors):
        """Solves for the semimajor axis at which the frequency is equal to the
        given combination of factors on omega, kappa and nu. Solution is via
        Newton's method."""

        # Find an initial guess
        sum_factors = np.sum(factors)

        # No first-order cancellation:
        #   freq(a) ~ sum[factors] * sqrt(GM/a^3)
        #
        #   a^3 ~ GM * (sum_factors/freq)^2

        if sum_factors != 0:
            a = (self.gm * (sum_factors/freq)**2)**(1./3.)

        # No second-order cancellation:
        #   freq(a) ~ term * sqrt(GM/a^3) * Rp^2 / a^2
        #
        #   a^7 ~ GM * (term/freq)^2 Rp^4

        elif factors[1] != factors[2]:
            term = (factors[0] * self.omega_jn[0] +
                    factors[1] * self.kappa_jn[0] +
                    factors[2] * self.nu_jn[0])
            a = (self.gm * (term * self.r2 / freq)**2)**(1/7.)

        # Second-order cancellation:
        #   freq(a) ~ term * sqrt(GM/a^3) * Rp^4 / a^4
        #
        #   a^11 ~ GM * (term/freq)^2 Rp^8

        else:
            term = (factors[0] * self.omega_jn[1] +
                    factors[1] * self.kappa_jn[1] +
                    factors[2] * self.nu_jn[1])
            a = (self.gm * (term * self.r2 * self.r2 / freq)**2)**(1/11.)

        # Iterate using Newton's method
        da = a      # Initial value for da just needs to be large
        for iter in range(SOLVE_A_MAXITERS):

            # Save previous values
            prev_a  = a
            prev_da = da

            # Take a step with Newton's method
            da = (self.combo(a, factors) - freq) / self.dcombo_da(a, factors)
            a = prev_a - da
            # print "newton: a=%s, da=%s, f(x)=%s"%(a, da, self.combo(a,factors))

            # Stop on exact convergence
            if a == prev_a: return a

            # Stop if we're close and convergence has stopped
            # This prevents infinite alternation between two nearby solutions
            da = abs(da)
            if da < a * PRECISION and da >= prev_da: return a

    # Useful alternative names...
    def n(self, a):
        """Returns the mean motion at semimajor axis a. Identical to omega(a).
        """

        return self.omega(a)

    def dmean_dt(self, a):
        """Returns the mean motion at semimajor axis a. Identical to omega(a).
        """

        return self.omega(a)

    def dperi_dt(self, a):
        """Returns the pericenter precession rate at semimajor axis a. Identical
        to combo(a, (1,-1,0))."""

        return self.combo(a, (1,-1,0))

    def dnode_dt(self, a):
        """Returns the nodal regression rate (negative) at semimajor axis a.
        Identical to combo(a, (1,0,-1))."""

        return self.combo(a, (1,0,-1))

    def d_dmean_dt_da(self, a):
        """Returns the radial derivative of the mean motion at semimajor axis a. 
        Identical to domega_da(a)."""

        return self.domega_da(a)

    def d_dperi_dt_da(self, a):
        """Returns the radial derivative of the pericenter precession rate at
        semimajor axis a. Identical to dcombo_da(a, (1,-1,0))."""

        return self.dcombo_da(a, (1,-1,0))

    def d_dnode_dt_da(self, a):
        """Returns the radial derivative of the nodal regression rate (negative)
        at semimajor axis a. Identical to dcombo_da(a, (1,0,-1))."""

        return self.dcombo_da(a, (1,0,-1))

# Planetary gravity fields defined...

G_MKS = 6.67428e-11     # m^3 kg^-1 s^-2
G_CGS = 6.67428e-08     # cm^3 g^-1 s^-2

JUPITER = Gravity(126686535., [14696.43e-06, -587.14e-06, 34.25e-06], 71492. )
SATURN  = Gravity( 37931208., [16290.71e-06, -935.83e-06, 86.14e-06], 60330. )
URANUS  = Gravity(  5793964., [ 3341.29e-06,  -30.44e-06           ], 26200. )
NEPTUNE = Gravity(  6835100., [ 3408.43e-06,  -33.40e-06           ], 25225. )
PLUTO_ONLY   = Gravity(870.3, [], 1151.)
PLUTO_CHARON = Gravity(870.3 + 101.4, [], 1151.)
# from http://arxiv.org/abs/0712.1261

################################################################################
# End of file
################################################################################
