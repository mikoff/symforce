# ----------------------------------------------------------------------------
# SymForce - Copyright 2022, Skydio, Inc.
# This source code is under the Apache 2.0 license found in the LICENSE file.
# ----------------------------------------------------------------------------

import string
import unittest

import numpy as np

import sym
from symforce import geo
from symforce.test_util import TestCase
from symforce.test_util.lie_group_ops_test_mixin import LieGroupOpsTestMixin
from symforce.values import Values


class OpsSymTest(LieGroupOpsTestMixin, TestCase):
    """
    Test that sym objects function as lie groups

    Note the mixin that tests all storage, group, and lie group ops.

    TODO(aaron): Also test cam classes
    """

    MANIFOLD_IS_DEFINED_IN_TERMS_OF_GROUP_OPS = False

    @classmethod
    def element(cls) -> Values:
        return Values(
            {
                l: (
                    getattr(sym, e.__name__).random()  # Use random() if it exists
                    if hasattr(getattr(sym, e.__name__), "random")  # Check if random() exists
                    else getattr(sym, e.__name__).from_tangent(
                        np.random.random(e.tangent_dim())
                    )  # Fallback to from_tangent()
                )
                for l, e in zip(string.ascii_lowercase, geo.GROUP_GEO_TYPES)
            }
        )

    # This is failing because sym types do not have .symbolic
    test_jacobian = unittest.expectedFailure(LieGroupOpsTestMixin.test_jacobian)

    # This is failing because sym types do not have .storage_D_tangent
    test_storage_D_tangent = unittest.expectedFailure(LieGroupOpsTestMixin.test_storage_D_tangent)

    # This is failing because sym types do not have .symbolic
    test_storage_ops = unittest.expectedFailure(LieGroupOpsTestMixin.test_storage_ops)

    # This is failing because sym types do not have .tangent_D_storage
    test_tangent_D_storage = unittest.expectedFailure(LieGroupOpsTestMixin.test_tangent_D_storage)


class OpsSymTestNonValidGroupTest(LieGroupOpsTestMixin, TestCase):
    """
    Test that sym objects function as valid manifolds.

    Note that this test is currently designed to curtail to the needs of Unit3 limits.
    """

    MANIFOLD_IS_DEFINED_IN_TERMS_OF_GROUP_OPS = False
    VALID_GROUP = False

    @classmethod
    def element(cls) -> Values:
        return Values(
            {
                l: (
                    getattr(sym, e.__name__).random()  # Use random() if it exists
                    if hasattr(getattr(sym, e.__name__), "random")  # Check if random() exists
                    else getattr(sym, e.__name__).from_tangent(
                        np.random.random(e.tangent_dim())
                    )  # Fallback to from_tangent()
                )
                for l, e in zip(string.ascii_lowercase, geo.GEO_TYPES)
            }
        )

    # This is failing because sym types do not have .symbolic
    test_jacobian = unittest.expectedFailure(LieGroupOpsTestMixin.test_jacobian)

    # This is failing because sym types do not have .storage_D_tangent
    test_storage_D_tangent = unittest.expectedFailure(LieGroupOpsTestMixin.test_storage_D_tangent)

    # This is failing because sym types do not have .symbolic
    test_storage_ops = unittest.expectedFailure(LieGroupOpsTestMixin.test_storage_ops)

    # This is failing because sym types do not have .tangent_D_storage
    test_tangent_D_storage = unittest.expectedFailure(LieGroupOpsTestMixin.test_tangent_D_storage)


if __name__ == "__main__":
    TestCase.main()
