import unittest # to test the digital forensics MAS (Python Software Foundation, 2024).
from final_new import CoordinatorAgent

class TestDigitalForensics(unittest.TestCase):

    def setUp(self):
        # Initialize test data
        self.evidence = ["term1", "term2"]

    def test_display_results(self):

        # Test display_results method of CoordinatorAgent

        coordinator_agent = CoordinatorAgent(self.evidence)
        coordinator_agent.results = [("term1", 5), ("term2", 3)]
        coordinator_agent.frequent_terms = [("term1", 5), ("term2", 3)]
        coordinator_agent.top_senders = [("sender1@example.com", 10), ("sender2@example.com", 7)]

        # Call the display_results method and capture the output
        # Assert that the output matches the expected output

        coordinator_agent.coordinate_search()
        # coordinator_agent.save_results()
        # coordinator_agent.display_results()

        self.assertEqual(coordinator_agent.top_senders, ["sender3@example.com", "sender4@example.com"]) 
        # Add strings that the agent is expected to find

if __name__ == '__main__':
    unittest.main()

