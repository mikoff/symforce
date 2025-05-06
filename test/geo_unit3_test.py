# ----------------------------------------------------------------------------
# SymForce - Copyright 2022, Skydio, Inc.
# This source code is under the Apache 2.0 license found in the LICENSE file.
# ----------------------------------------------------------------------------

import numpy as np

import symforce.symbolic as sf
from symforce import typing as T
from symforce.test_util import TestCase
from symforce.test_util.lie_group_ops_test_mixin import LieGroupOpsTestMixin


class GeoUnit3Test(LieGroupOpsTestMixin, TestCase):
    """
    Test the Unit3 geometric class.
    Note the mixin that tests all storage, group and lie group ops.
    """

    MANIFOLD_IS_DEFINED_IN_TERMS_OF_GROUP_OPS = False
    VALID_GROUP = False

    def setUp(self) -> None:
        super().setUp()
        self.test_directions = self.make_test_directions()

    @classmethod
    def element(cls) -> sf.Unit3:
        return sf.Unit3.from_vector(sf.V3(0, 1, 0))

    @staticmethod
    def make_test_directions() -> T.List[sf.V3]:
        """
        Get a list of fixed and random directions for testing
        """
        directions = [
            a.normalized()
            for a in [
                sf.V3(1.0, 0.0, 0.0),
                sf.V3(0.0, 1.0, 0.0),
                sf.V3(0.0, 0.0, 1.0),
                sf.V3(-1.0, 0.0, 0.0),
                sf.V3(0.0, -1.0, 0.0),
                sf.V3(0.0, 0.0, -1.0),
                sf.V3(1.0, 2.0, 3.0),
            ]
        ]

        for _ in range(50):
            a = np.random.uniform(-1.0, 1.0, 3)
            if np.linalg.norm(a) > 1e-4:
                directions.append(sf.V3(a).normalized())

        return directions

    def test_symbolic_substitution(self) -> None:
        """
        Tests:
            Unit3.subs
        """
        u1 = sf.Unit3.symbolic("u_1")
        u2 = sf.Unit3.symbolic("u_2")
        base = sf.Unit3.symbolic("base")
        self.assertEqual(u2, u1.subs(u1, u2))
        self.assertEqual(
            sf.M(base.local_coordinates(u2)), sf.M(base.local_coordinates(u1)).subs(u1, u2)
        )
        self.assertEqual(
            base.retract(sf.M(base.local_coordinates(u2)).to_flat_list()),
            base.retract(sf.M(base.local_coordinates(u1)).subs(u1, u2).to_flat_list()),
        )

    def test_from_vector(self) -> None:
        """
        Tests:
            Unit3.from_vector
        """
        for direction in self.test_directions:
            u3 = sf.Unit3.from_vector(direction, epsilon=self.EPSILON)
            self.assertLieGroupNear(u3.to_unit_vector(), direction, places=5)


if __name__ == "__main__":
    TestCase.main()
