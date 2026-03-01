import unittest
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tools import code_lookup, cms_coverage, npi_lookup, payer_policy

class TestTools(unittest.TestCase):
    def test_code_lookup(self):
        desc = code_lookup.lookup_cpt("27447")
        self.assertIn("Total Knee Replacement", desc)
        
        valid = code_lookup.validate_procedure_code("27447")
        self.assertTrue(valid)

    def test_cms_coverage_lookup(self):
        policy = cms_coverage.lookup_cms_policy("27447")
        self.assertIsNotNone(policy)
        self.assertEqual(policy["policy_id"], "NCD-150.6")

    def test_payer_policy_lookup(self):
        policy = payer_policy.lookup_payer_policy("UnitedHealthcare", "27447")
        self.assertIsNotNone(policy)
        self.assertEqual(policy["payer_id"], "UHC001")

    # Skipping NPI lookup live test for now as it makes external call
    # In CI/CD we would mock this.

if __name__ == "__main__":
    unittest.main()
