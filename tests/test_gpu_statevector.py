"""Independent oracle and fixed GPU study contract; no synthetic measurements."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gpu_statevector',ROOT/'tools/gpu_statevector.py')
gpu=importlib.util.module_from_spec(spec);spec.loader.exec_module(gpu)

class StatevectorOracleTests(unittest.TestCase):
    def test_asymmetric_control_and_most_significant_bit(self):
        ops=[['ry',[0],np.pi],['cx',[0,1],None],['rz',[1],.6]]
        result=gpu.reference(3,ops)
        expected=np.zeros(8,dtype=np.complex128);expected[6]=np.exp(.3j)
        np.testing.assert_allclose(result,expected,atol=1e-14,rtol=0)
        reverse=gpu.reference(3,[['ry',[0],np.pi],['cx',[1,0],None]])
        self.assertAlmostEqual(abs(reverse[4]),1)

    def test_workload_is_fixed_normalized_and_nondegenerate(self):
        ops=gpu.operations(4,4,41)
        self.assertEqual(ops,gpu.operations(4,4,41))
        self.assertNotEqual(ops,gpu.operations(4,4,42))
        state=gpu.reference(4,ops)
        self.assertAlmostEqual(float(np.vdot(state,state).real),1)
        self.assertGreater(np.count_nonzero(abs(state)>1e-5),8)

if __name__=='__main__':unittest.main()
