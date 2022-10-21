import unittest
import json

from main import sniff_schema


class test_code(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # load file
        with open("../data/data_2.json", "r") as load_data:
            cls.test_data_2 = json.load(load_data)

    # utility function
    def utility(self): 

        schema1 = sniff_schema()
        schema1.load("../data/data_1.json")

        schema2 = sniff_schema(self.test_data_2["message"])

        # this is returned to be used in sniffing test
        return schema1, schema2

    # test sniffer
    def test_snif_instance(self): 
        snf = sniff_schema()
        snf2 = sniff_schema({"key" : "val"})
        self.assertEqual(snf.data, {}) # empty dict as no data provided at creation
        self.assertEqual(snf2.data, {"key" : "val"}) # A dict was provided at creation and is test against

    # test json data
    def test_loading(self):

        snf = sniff_schema()

        retload = snf.load("../data/data_2.json")

        self.assertEqual(snf.data, self.test_data_2["message"]) # compare updated data with presaved
        self.assertEqual(retload, self.test_data_2["message"]) 	# compare what's returned with presaved

    # test the logic 
    def test_sniffing(self):

        schema1, schema2 = self.utility()

        schema1.sniff()
        schema2.sniff()

        # comparing schema data with expected output
        with open("../data/test_outputs/example_output1.json", "r") as read_data:

            testdata1 = json.load(read_data)
            self.assertEqual(testdata1, schema2.data)

        with open("../data/test_outputs/example_output2.json", "r") as read_data:

            testdata2 = json.load(read_data)
            self.assertEqual(testdata2, schema2.data)

    # json saving test
    def test_output_save(self):

        snf = sniff_schema(self.test_data_2)
        snf.save("../data/test_outputs/save_output.json")

        with open("../data/test_outputs/save_output.json", "r") as read_data:

            testdata = json.load(read_data)
        # test if whatever is in self.data is well saved to provided directory at save() call

        self.assertEqual(self.test_data_2, testdata)

if __name__ == '__main__' :
    unittest.main()