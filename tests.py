import unittest
from main import ProjectPlan

class TestStringMethods(unittest.TestCase):
    def test_all_good(self):
        a = ProjectPlan('yaml/test_jobs.yaml')
        value = a.run()
        should_be = [['job_a', 'job_c_2', 'job_d', 'foo'], ['job_b'], ['job_c', 'job_e']]
        self.assertEqual(value, should_be)

    def test_unmet_dependency(self):
        a = ProjectPlan('yaml/test_jobs_unmet_dependency.yaml')
        with self.assertRaises(RuntimeError) as e:
            value = a.run()
        self.assertEqual(e.exception.args[0], "\033[41mThe following jobs have unmet or mutual dependencies : ['job_c']\033[0m")
        
    def test_mutual_dependency(self):
        a = ProjectPlan('yaml/test_jobs_mutual_dependency.yaml')
        with self.assertRaises(RuntimeError) as e:
            value = a.run()
        self.assertEqual(e.exception.args[0], "\033[41mThe following jobs have unmet or mutual dependencies : ['job_b', 'job_c', 'job_e']\033[0m")
        
    def test_yaml_problem1(self):
        a = ProjectPlan('yaml/test_jobs_invalid_yaml.yaml')
        with self.assertRaises(RuntimeError) as e:
            value = a.run()
        self.assertEqual(e.exception.args[0], "\033[41mError Occured while processing the following job : job_b - Please check your yaml file\033[0m")
        
    def test_yaml_problem2(self):
        # although this one is because of messing with the yaml file generating a wrong parsed_data
        # the parser managed to read the yaml file with what it thinks is correct - job_b is messed up
        # following jobs cannot have met dependency since job_b problematic
        # only way to do better is not relying on the yaml parsing library and writting my own parser tailor made for this exercise ( having more thorough validation of the yaml file )
        # IMPORTANT : the program still raises an exception instead of providing a result inadequate hence I kept it this way
        a = ProjectPlan('yaml/test_jobs_invalid_yaml2.yaml')
        with self.assertRaises(RuntimeError) as e:
            value = a.run()
        self.assertEqual(e.exception.args[0], "\033[41mThe following jobs have unmet or mutual dependencies : ['job_b', 'job_c', 'job_e']\033[0m")
        
    def test_yaml_problem3(self):
        a = ProjectPlan('yaml/test_jobs_invalid_yaml3.yaml')
        with self.assertRaises(RuntimeError) as e:
            value = a.run()
        #print(e.exception.args[0])
        self.assertEqual(e.exception.args[0], "\033[41mFailed to parse the following yaml file : yaml/test_jobs_invalid_yaml3.yaml - Please check if path provided is valid and if the yaml file itself is valid\033[0m")
        
    def test_missing_definitions(self):
        a = ProjectPlan('yaml/test_jobs_missing_definitions.yaml')
        with self.assertRaises(RuntimeError) as e:
            value = a.run()
        self.assertEqual(e.exception.args[0], "\033[41mNo job/task found without dependencies - most likely some jobs definition are missing from the yaml file\033[0m")
        

if __name__ == "__main__":
    unittest.main()
    #all_good()
    #unmet_dependency()
    #mutual_dependency()
    #yaml_problem1()
    #yaml_problem2()
    #yaml_problem3()