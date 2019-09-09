from unittest import TestCase
import unittest
from actor import Actor
from model import Model
from talent_agency import TalentAgency
import inspect
from unittest.mock import patch, mock_open
from sqlalchemy import create_engine
from base import Base
import os


class TestTalentAgency(TestCase):
    '''Unit tests for the TestTalentAgency Class'''


    def setUp(self):
        """ Creates a test fixture before each test method is run """
        engine = create_engine('sqlite:///test_talent.sqlite')

        Base.metadata.create_all(engine)
        Base.metadata.bind = engine

        self.talent_mgr = TalentAgency('test_talent.sqlite')

        self.actor1 = Actor("Sub","Hossan","A01050900","2012-12-25 00:00:00",4)
        self.actor1.movie_to_string()

        self.actor2 = Actor("Ewan","Watt","A01020509","1995-04-08 00:00:00",4)
        self.actor2.movie_to_string()

        self.model1 = Model("Ashvan", "Wal", "A01023474", "2000-01-15 00:00:00", "commercial")
        self.model2 = Model("Phuong", "Ho", "A01023444", "2011-05-23 00:00:00", "vedette")

        self.logPoint()


    def test_empty_constructor(self):
        '''Test with empty parameter of constructor'''
        self.assertRaisesRegex(FileNotFoundError, "Invalid Database File", TalentAgency, "")

    def test_none_constructor(self):
        '''Test with none parameter of constructor'''
        self.assertRaisesRegex(FileNotFoundError, "Invalid Database File", TalentAgency, None)

    def test_valid_constructor(self):
        '''Test with valid constructor'''
        self.assertIsNotNone(self.talent_mgr)

    def test_valid_constructor_file(self):
        """Test with valid file path"""
        talent2 = TalentAgency("food.json")
        self.assertIsNotNone(talent2)

    def test_add_talent_return_id(self):
        '''Test with valid talent'''
        self.assertEqual(self.talent_mgr.add_talent(self.model1),1)

    def test_add_talent(self):
        '''Test with valid talent'''
        self.talent_mgr.add_talent(self.model1)
        self.talent_mgr.add_talent(self.actor1)

        all_talent = self.talent_mgr.get_all()
        self.assertEqual(len(all_talent), 2)

        model1_id = self.talent_mgr.add_talent(self.model1)

        retrieved_model1 = self.talent_mgr.get_talent(model1_id)
        self.assertEqual(retrieved_model1.first_name, "Ashvan")
        self.assertEqual(retrieved_model1.last_name, "Wal")
        self.assertEqual(retrieved_model1.talent_num, "A01023474")
        self.assertEqual(retrieved_model1.date_debut, "2000-01-15 00:00:00")
        self.assertEqual(retrieved_model1.model_type, "commercial")

        actor1_id = self.talent_mgr.add_talent(self.actor1)

        retrieved_actor1 = self.talent_mgr.get_talent(actor1_id)
        self.assertEqual(retrieved_actor1.first_name, "Sub")
        self.assertEqual(retrieved_actor1.last_name, "Hossan")
        self.assertEqual(retrieved_actor1.talent_num, "A01050900")
        self.assertEqual(retrieved_actor1.date_debut, "2012-12-25 00:00:00")
        self.assertEqual(retrieved_actor1.award_num, 4)
    
    def test_add_invalid_talent(self):
        '''Test with invalid talent'''
        invalid_object = ""
        self.assertRaisesRegex(ValueError,"Invalid Talent Object",self.talent_mgr.add_talent,invalid_object)

        invalid_object = None
        self.assertRaisesRegex(ValueError, "Invalid Talent Object", self.talent_mgr.add_talent, invalid_object)
   
    def test_get_talent(self):
        '''Test with valid talent id'''
        model1_id = self.talent_mgr.add_talent(self.model1)

        retrieved_model1 = self.talent_mgr.get_talent(model1_id)
        self.assertIsNotNone(retrieved_model1)

        self.assertEqual(retrieved_model1.first_name, "Ashvan")
        self.assertEqual(retrieved_model1.last_name, "Wal")
        self.assertEqual(retrieved_model1.talent_num, "A01023474")
        self.assertEqual(retrieved_model1.date_debut, "2000-01-15 00:00:00")
        self.assertEqual(retrieved_model1.model_type, "commercial")

        actor1_id = self.talent_mgr.add_talent(self.actor1)

        retrieved_actor1 = self.talent_mgr.get_talent(actor1_id)
        self.assertIsNotNone(retrieved_actor1)

        self.assertEqual(retrieved_actor1.first_name, "Sub")
        self.assertEqual(retrieved_actor1.last_name, "Hossan")
        self.assertEqual(retrieved_actor1.talent_num, "A01050900")
        self.assertEqual(retrieved_actor1.date_debut, "2012-12-25 00:00:00")
        self.assertEqual(retrieved_actor1.award_num, 4)


    def test_get_talent_not_valid_talent_id(self):
        '''Test with invalid talent id'''
        invalid_id = "acb"
        self.assertRaisesRegex(ValueError, "Invalid Talent ID", self.talent_mgr.get_talent, invalid_id)


    def test_get_talent_not_exist(self):
        '''Test with not exist talent id'''
        invalid_id = 4
        self.assertRaisesRegex(ValueError,"Talent Not Found", self.talent_mgr.get_talent, invalid_id)


    def test_get_all(self):
        '''Test with valid talents returned'''
        all_talents = self.talent_mgr.get_all()
        self.assertEqual(len(all_talents), 0)

        self.talent_mgr.add_talent(self.model1)
        self.talent_mgr.add_talent(self.actor1)

        all_talents = self.talent_mgr.get_all()
        self.assertEqual(len(all_talents), 2)

    def test_get_all_by_type_model(self):
        '''Test with valid talents by type'''

        all_model = self.talent_mgr.get_all_by_type("model")
        self.assertEqual(len(all_model), 0)

        self.talent_mgr.add_talent(self.model1)
        self.talent_mgr.add_talent(self.model2)
        self.talent_mgr.add_talent(self.actor1)
        self.talent_mgr.add_talent(self.actor2)

        all_model = self.talent_mgr.get_all_by_type("model")

        retrieved_model1 = all_model[0]
        self.assertIsNotNone(retrieved_model1)

        self.assertEqual(retrieved_model1.first_name, "Ashvan")
        self.assertEqual(retrieved_model1.last_name, "Wal")
        self.assertEqual(retrieved_model1.talent_num, "A01023474")
        self.assertEqual(retrieved_model1.date_debut, "2000-01-15 00:00:00")
        self.assertEqual(retrieved_model1.model_type, "commercial")

    def test_get_all_by_type_actor(self):
        '''Test with valid talents by type'''

        all_actor = self.talent_mgr.get_all_by_type("actor")
        self.assertEqual(len(all_actor), 0)

        self.talent_mgr.add_talent(self.model1)
        self.talent_mgr.add_talent(self.model2)
        self.talent_mgr.add_talent(self.actor1)
        self.talent_mgr.add_talent(self.actor2)

        all_actor = self.talent_mgr.get_all_by_type("actor")

        retrieved_actor1 = all_actor[0]
        self.assertIsNotNone(retrieved_actor1)

        self.assertEqual(retrieved_actor1.first_name, "Sub")
        self.assertEqual(retrieved_actor1.last_name, "Hossan")
        self.assertEqual(retrieved_actor1.talent_num, "A01050900")
        self.assertEqual(retrieved_actor1.date_debut, "2012-12-25 00:00:00")
        self.assertEqual(retrieved_actor1.award_num, 4)


    def test_get_all_by_type_invalid_type(self):
        '''Test with invalid type'''
        self.talent_mgr.add_talent(self.model1)
        self.talent_mgr.add_talent(self.model2)
        self.talent_mgr.add_talent(self.actor1)
        self.talent_mgr.add_talent(self.actor2)

        invalid_type_empty = ""
        self.assertRaisesRegex(ValueError, "Type cannot be empty.", self.talent_mgr.get_all_by_type, invalid_type_empty)

        invalid_type_none = None
        self.assertRaisesRegex(ValueError, "Type cannot be undefined.", self.talent_mgr.get_all_by_type,
                               invalid_type_none)


    def test_update_model(self):
        '''Test with valid update model'''

        model1_id = self.talent_mgr.add_talent(self.model1)

        retrieved_model1 = self.talent_mgr.get_talent(model1_id)
        self.assertEqual(retrieved_model1.first_name, "Ashvan")
        self.assertEqual(retrieved_model1.last_name, "Wal")
        self.assertEqual(retrieved_model1.talent_num, "A01023474")
        self.assertEqual(retrieved_model1.date_debut, "2000-01-15 00:00:00")
        self.assertEqual(retrieved_model1.model_type, "commercial")

        retrieved_model1.first_name = "P"
        retrieved_model1.last_name = "H"
        self.talent_mgr.update(retrieved_model1)

        retrieved_model1 = self.talent_mgr.get_talent(model1_id)
        self.assertEqual(retrieved_model1.first_name, "P")
        self.assertEqual(retrieved_model1.last_name, "H")


    def test_update_actor(self):
        '''Test with valid update actor '''
        actor1_id = self.talent_mgr.add_talent(self.actor1)

        retrieved_actor1 = self.talent_mgr.get_talent(actor1_id)
        self.assertEqual(retrieved_actor1.first_name, "Sub")
        self.assertEqual(retrieved_actor1.last_name, "Hossan")
        self.assertEqual(retrieved_actor1.talent_num, "A01050900")
        self.assertEqual(retrieved_actor1.date_debut, "2012-12-25 00:00:00")
        self.assertEqual(retrieved_actor1.award_num, 4)

        retrieved_actor1.first_name = "P"
        retrieved_actor1.last_name = "H"
        self.talent_mgr.update(retrieved_actor1)

        retrieved_actor1 = self.talent_mgr.get_talent(actor1_id)
        self.assertEqual(retrieved_actor1.first_name, "P")
        self.assertEqual(retrieved_actor1.last_name, "H")

 
    def test_update_talent_invalid(self):
        """Test with invalid talent"""
        self.assertRaisesRegex(ValueError, "Invalid Talent Object", self.talent_mgr.update, None)
        self.assertRaisesRegex(ValueError, "Invalid Talent Object", self.talent_mgr.update, 1)


    def test_delete_talent_invalid(self):
        """Test with delete talent functions"""
        self.assertRaisesRegex(ValueError, "Talent ID has to be an integer.", self.talent_mgr.delete, None)
        self.assertRaisesRegex(ValueError, "Talent does not exist", self.talent_mgr.delete, 1)

    def test_delete(self):
        """Test with delete valid talent"""

        model1_id = self.talent_mgr.add_talent(self.model1)
        retrieved_model1 = self.talent_mgr.get_talent(model1_id)
        self.assertIsNotNone(retrieved_model1)
        self.talent_mgr.delete(model1_id)
        self.assertRaisesRegex(ValueError, "Talent Not Found", self.talent_mgr.get_talent, model1_id)

        actor1_id = self.talent_mgr.add_talent(self.actor1)
        retrieved_model1 = self.talent_mgr.get_talent(actor1_id)
        self.assertIsNotNone(retrieved_model1)
        self.talent_mgr.delete(actor1_id)
        self.assertRaisesRegex(ValueError, "Talent Not Found", self.talent_mgr.get_talent, actor1_id)


    def tearDown(self):
        """ Creates a test fixture for tear down after each test method is run """
        os.remove('test_talent.sqlite')
        self.logPoint()

    def logPoint(self):
        """ Utility function used for module functions and class methods """
        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))

if __name__ == '__main__':
    unittest.main()


