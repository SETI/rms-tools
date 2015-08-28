#!/usr/bin/python
################################################################################
# gravity.py
#
# Classes and methods to deal with gravity fields of oblate planets.
#
# Mark R. Showalter, SETI Institute, March 2010
# Revised October 2011.
# Revised December 2, 2011 (BSW) - add unit tests
#                                - change solve_a() to handle arrays
# Revised December 3, 2011 (MRS)
#   - Fixed errors that made poor initial guesses in solve_a(). Reduced default
#     number of iterations to 5.
#   - Added unit tests giving array arguments to solve_a().
#
# Revised February 18, 2012 (MRS)
#   - Added gravity fields of more bodies as class constants.
################################################################################
import numpy as np
import unittest

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
        if factors[0] != 0:
            omega2_jsum = Gravity._jseries(self.omega_jn, ratio2)
            omega2 = gm_over_a3 * (1. + omega2_jsum)
            omega  = np.sqrt(omega2)

            sum_factors += factors[0]
            sum_values  += factors[0] * omega

        # kappa term
        if factors[1] != 0:
            kappa2_jsum = Gravity._jseries(self.kappa_jn, ratio2)
            kappa2 = gm_over_a3 * (1. + kappa2_jsum)
            kappa  = np.sqrt(kappa2)

            sum_factors += factors[1]
            sum_values  += factors[1] * kappa

        # nu term
        if factors[2] != 0:
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

        if factors[0] != 0:
            omega_diff = gm_over_a3 * omega2_jsum / (omega + sqrt_gm_over_a3)
            sum_values += factors[0] * omega_diff

        if factors[1] != 0:
            kappa_diff = gm_over_a3 * kappa2_jsum / (kappa + sqrt_gm_over_a3)
            sum_values += factors[1] * kappa_diff

        if factors[2] != 0:
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

    def solve_a(self, freq, factors=(1,0,0), iters=5):
        """Solves for the semimajor axis at which the frequency is equal to the
        given combination of factors on omega, kappa and nu. Solution is via
        Newton's method."""

        # Find an initial guess
        sum_factors = np.sum(factors)

        # No first-order cancellation:
        #   freq(a) ~ sum[factors] * sqrt(GM/a^3)
        #
        #   a^3 ~ GM * (sum[factors] / freq)^2

        if sum_factors != 0:
            a = (self.gm * (sum_factors/freq)**2)**(1./3.)

        # No second-order cancellation:
        #   freq(a) ~ 1/2 * sum[factor*term] * sqrt(GM/a^3) * Rp^2 / a^2
        #
        #   a^7 ~ GM * (sum[factor*term]/2 / freq)^2 Rp^4

        elif factors[1] != factors[2]:
            term = (factors[0] * self.omega_jn[0] +
                    factors[1] * self.kappa_jn[0] +
                    factors[2] * self.nu_jn[0]) / 2.
            a = (self.gm * (term * self.r2 / freq)**2)**(1/7.)

        # Second-order cancellation:
        #   freq(a) ~ -1/8 * sum[factor*term^2] * sqrt(GM/a^3) * Rp^4 / a^4
        #
        #   a^11 ~ GM * (-sum[factor*term^2]/8 / freq)^2 Rp^8

        else:
            term = (factors[0] * self.omega_jn[0]**2 +
                    factors[1] * self.kappa_jn[0]**2 +
                    factors[2] * self.nu_jn[0]**2) / (-8.)
            a = (self.gm * (term * self.r2 * self.r2 / freq)**2)**(1/11.)

        # Iterate using Newton's method
        for iter in range(iters):
            # a step in Newton's method: x(i+1) = x(i) - f(xi) / fp(xi)
            # our f(x) = self.combo() - freq
            #     fp(x) = self.dcombo()

            a -= ((self.combo(a, factors) - freq) / self.dcombo_da(a, factors))

        return a

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
        to combo(a, (1,-1,0)).
        """

        return self.combo(a, (1,-1,0))

    def dnode_dt(self, a):
        """Returns the nodal regression rate (negative) at semimajor axis a.
        Identical to combo(a, (1,0,-1)).
        """

        return self.combo(a, (1,0,-1))

    def d_dmean_dt_da(self, a):
        """Returns the radial derivative of the mean motion at semimajor axis a. 
        Identical to domega_da(a).
        """

        return self.domega_da(a)

    def d_dperi_dt_da(self, a):
        """Returns the radial derivative of the pericenter precession rate at
        semimajor axis a. Identical to dcombo_da(a, (1,-1,0)).
        """

        return self.dcombo_da(a, (1,-1,0))

    def d_dnode_dt_da(self, a):
        """Returns the radial derivative of the nodal regression rate (negative)
        at semimajor axis a. Identical to dcombo_da(a, (1,0,-1)).
        """

        return self.dcombo_da(a, (1,0,-1))

    def olr_pattern(self, n, m, p=1):
        """Returns the pattern speed of the m:m+p outer Lindblad resonance,
        given the mean motion n of the perturber.
        """

        a = self.solve_a(n, (1,0,0))
        return (n + self.kappa(a) * p/m)

    def ilr_pattern(self, n, m, p=1):
        """Returns the pattern speed of the m:m-p inner Lindblad resonance,
        given the mean motion n of the perturber.
        """

        return olr_pattern(self, n, m, -p)

# Planetary gravity fields defined...

# From http://ssd.jpl.nasa.gov/?planet_phys_par
G_MKS = 6.67428e-11     # m^3 kg^-1 s^-2
G_CGS = 6.67428e-08     # cm^3 g^-1 s^-2

G_PER_KG = G_MKS / 1.e9
G_PER_G  = G_CGS / 1.e15

# From http://ssd.jpl.nasa.gov/?planet_phys_par
SUN = Gravity(132712440018., [], 695500.)

# From http://ssd.jpl.nasa.gov/?planet_phys_par
MERCURY = Gravity(0.330104e24 * G_PER_KG, [], 2439.7 )
VENUS   = Gravity( 4.86732e24 * G_PER_KG, [], 6051.8 )
EARTH   = Gravity( 5.97219e24 * G_PER_KG, [], 6378.14)
MARS    = Gravity(0.641693e24 * G_PER_KG, [], 3396.19)

# From http://ssd.jpl.nasa.gov/?gravity_fields_op
JUPITER = Gravity(126686535., [14696.43e-06, -587.14e-06, 34.25e-06], 71492.)
#SATURN  = Gravity( 37931208.,  [16290.71e-06, -935.83e-06, 86.14e-06], 60330.)
SATURN  = Gravity( 37931207.7, [16290.71e-06, -936.83e-06, 86.14e-06, -10.e-06], 60330.)
URANUS  = Gravity(  5793964., [ 3341.29e-06,  -30.44e-06           ], 26200.)
NEPTUNE = Gravity(  6835100., [ 3408.43e-06,  -33.40e-06           ], 25225.)

# From http://arxiv.org/abs/0712.1261
PLUTO_ONLY = Gravity(870.3, [], 1151.)
PLUTO = PLUTO_ONLY

# From http://ssd.jpl.nasa.gov/?sat_phys_par
MOON      = Gravity(4902.801, [], 1737.5)

IO        = Gravity(5959.916, [], 1821.6)
EUROPA    = Gravity(3202.739, [], 1560.8)
GANYMEDE  = Gravity(9887.834, [], 2631.2)
CALLISTO  = Gravity(7179.289, [], 2410.3)

MIMAS     = Gravity(   2.5026, [],  198.20)
ENCELADUS = Gravity(   7.2027, [],  252.10)
TETHYS    = Gravity(  41.2067, [],  533.00)
DIONE     = Gravity(  73.1146, [],  561.70)
RHEA      = Gravity( 153.9426, [],  764.30)
TITAN     = Gravity(8978.1382, [], 2574.73)
HYPERION  = Gravity(   0.3727, [],  135.00)
IAPETUS   = Gravity( 120.5038, [],  735.60)
PHOEBE    = Gravity(   0.5532, [],  106.50)

MIRANDA   = Gravity(   4.4, [], 235.8)
ARIEL     = Gravity(  86.4, [], 578.9)
UMBRIEL   = Gravity(  81.5, [], 584.7)
TITANIA   = Gravity( 228.2, [], 788.9)
OBERON    = Gravity( 192.4, [], 761.4)

TRITON    = Gravity(1427.6, [], 1353.4)
NEREID    = Gravity(  2.06, [],  170.)

CHARON    = Gravity(103.2, [], 603.6)

# Sets with relatively large mass ratios
SUN_JUPITER = Gravity(SUN.gm + JUPITER.gm, [], SUN.rp)

JUPITER_GALS = Gravity(JUPITER.gm + IO.gm + EUROPA.gm + GANYMEDE.gm +
                       CALLISTO.gm, JUPITER.jn, JUPITER.rp)

SATURN_TITAN = Gravity(SATURN.gm + TITAN.gm, SATURN.jn, SATURN.rp)

PLUTO_CHARON = Gravity(PLUTO_ONLY.gm + CHARON.gm, [], PLUTO_ONLY.rp)

PLUTO_A  = 2035.                    # km
CHARON_A = 19573. - 2035.           # km
ratio2 = (PLUTO_A / CHARON_A)**2
gm1 = PLUTO_ONLY.gm
gm2 = CHARON.gm
PLUTO_CHARON_AS_RINGS = Gravity(gm1 + gm2,
        [ 1/2.    * (gm1 * ratio2    + gm2) / (gm1 + gm2),
         -3/8.    * (gm1 * ratio2**2 + gm2) / (gm1 + gm2),
          5/16.   * (gm1 * ratio2**3 + gm2) / (gm1 + gm2),
         -35/128. * (gm1 * ratio2**4 + gm2) / (gm1 + gm2),
          63/256. * (gm1 * ratio2**5 + gm2) / (gm1 + gm2)], CHARON_A)
LOOKUP = {
    "SUN": SUN,
    "MERCURY": MERCURY,
    "VENUS": VENUS,
    "EARTH": EARTH,
    "MARS": MARS,
    "JUPITER": JUPITER,
    "SATURN": SATURN,
    "URANUS": URANUS,
    "NEPTUNE": NEPTUNE,
    "PLUTO_ONLY": PLUTO_ONLY,
    "PLUTO": PLUTO_ONLY,
    "MOON": MOON,
    "IO": IO,
    "EUROPA": EUROPA,
    "GANYMEDE": GANYMEDE,
    "CALLISTO": CALLISTO,
    "MIMAS": MIMAS,
    "ENCELADUS": ENCELADUS,
    "TETHYS": TETHYS,
    "DIONE": DIONE,
    "RHEA": RHEA,
    "TITAN": TITAN,
    "HYPERION": HYPERION,
    "IAPETUS": IAPETUS,
    "PHOEBE": PHOEBE,
    "MIRANDA": MIRANDA,
    "ARIEL": ARIEL,
    "UMBRIEL": UMBRIEL,
    "TITANIA": TITANIA,
    "OBERON": OBERON,
    "TRITON": TRITON,
    "NEREID": NEREID,
    "CHARON": CHARON,
    "SUN_JUPITER": SUN_JUPITER,
    "JUPITER_GALS": JUPITER_GALS,
    "SATURN_TITAN": SATURN_TITAN,
    "PLUTO_CHARON": PLUTO_CHARON,
    "SOLAR SYSTEM BARYCENTER": SUN_JUPITER,
    "SSB": SUN_JUPITER,
    "JUPITER BARYCENTER": JUPITER_GALS,
    "SATURN BARYCENTER": SATURN_TITAN,
    "URANUS BARYCENTER": URANUS,
    "NEPTUNE BARYCENTER": NEPTUNE,
    "PLUTO BARYCENTER": PLUTO_CHARON
}

########################################
# UNIT TESTS
########################################

ERROR_TOLERANCE = 1.e-15

class Test_Gravity(unittest.TestCase):

    def test_uncombo(self):

        # Testing scalars in a loop...
        tests = 100
        planets = [JUPITER, SATURN, URANUS, NEPTUNE, PLUTO_CHARON]
        factors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

        for test in range(tests):
          for obj in planets:
            a = obj.rp * 10. ** (np.random.rand() * 2.)
            for f in factors:
                b = obj.solve_a(obj.combo(a, f), f)
                c = abs((b - a) / a)
                self.assertTrue(c < ERROR_TOLERANCE)

        # Testing a 100x100 array
        for obj in planets:
            a = obj.rp * 10. ** (np.random.rand(100,100) * 2.)
            for f in factors:
                b = obj.solve_a(obj.combo(a, f), f)
                c = abs((b - a) / a)
                self.assertTrue(np.all(c < ERROR_TOLERANCE))

        # Testing with first-order cancellation
        factors = [(1, -1, 0), (1, 0, -1), (0, 1, -1)]
        planets = [JUPITER, SATURN, URANUS, NEPTUNE]

        for obj in planets:
            a = obj.rp * 10. ** (np.random.rand(100,100) * 2.)
            for f in factors:
                b = obj.solve_a(obj.combo(a, f), f)
                c = abs((b - a) / a)
                self.assertTrue(np.all(c < ERROR_TOLERANCE))

        # Testing with second-order cancellation
        factors = [(2, -1, -1)]
        planets = [JUPITER, SATURN, URANUS, NEPTUNE]

        for obj in planets:
            a = obj.rp * 10. ** (np.random.rand(100,100) * 2.)
            for f in factors:
                b = obj.solve_a(obj.combo(a, f), f)
                c = abs((b - a) / a)
                self.assertTrue(np.all(c < ERROR_TOLERANCE))

if __name__ == '__main__':
    unittest.main()

################################################################################
# End of file
################################################################################
