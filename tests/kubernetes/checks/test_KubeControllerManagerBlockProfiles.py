import os
import unittest

from checkov.kubernetes.checks.resource.k8s.KubeControllerManagerBlockProfiles import check
from checkov.kubernetes.runner import Runner
from checkov.runner_filter import RunnerFilter


class TestKubeControllerManagerBlockProfiles(unittest.TestCase):

    def test_summary(self):
        runner = Runner()
        current_dir = os.path.dirname(os.path.realpath(__file__))

        test_files_dir = current_dir + "/example_KubeControllerManagerBlockProfiles"
        report = runner.run(root_folder=test_files_dir, runner_filter=RunnerFilter(checks=[check.id]))
        summary = report.get_summary()

        self.assertEqual(1, summary['passed'])
        self.assertEqual(2, summary['failed'])
        self.assertEqual(0, summary['skipped'])
        self.assertEqual(0, summary['parsing_errors'])

        for failed in report.failed_checks:
            self.assertIn("should-fail", failed.resource)
        for passed in report.passed_checks:
            self.assertIn("should-pass", passed.resource)


if __name__ == '__main__':
    unittest.main()
