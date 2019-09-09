from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

import json
from model import Model
from actor import Actor
import os.path
import datetime

class TalentAgency:
    '''Maintains details about talent agency'''
    def __init__(self,db_filename):
        """Constructor of TalentAgency"""

        if db_filename is None or db_filename == "":
            raise FileNotFoundError("Invalid Database File")

        engine = create_engine('sqlite:///'+ db_filename)

        #Bind the engine to the metadata of the Base Class so that the
        #declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine

        self._db_session = sessionmaker(bind=engine)

    def add_talent(self,talent_object):
        '''Return talent_id, adds new talent to the list of talents.'''


        if talent_object is None or (not isinstance(talent_object,Model) and not isinstance(talent_object,Actor)):
            raise ValueError("Invalid Talent Object")

        session = self._db_session()

        session.add(talent_object)
        session.commit()

        talent_id = talent_object.id


        session.close()

        return talent_id

    def get_talent(self, talent_id: int):
        '''Gets talent object based on talent_id'''

        if(talent_id is None or type(talent_id) != int):
            raise ValueError("Invalid Talent ID")

        session = self._db_session()

        existing_talent = session.query(Actor).filter(Actor.id == talent_id).first()

        if existing_talent is None:
            raise ValueError("Talent Not Found")

        if existing_talent.type != "actor":
            existing_talent = session.query(Model).filter(Model.id == talent_id).first()

        session.close()

        return existing_talent

    def get_all(self) -> list:
        '''Returns list of all the talents.'''
        session = self._db_session()

        talent_actor = session.query(Actor).filter(Actor.type == "actor").all()
        talent_model = session.query(Model).filter(Model.type == "model").all()

        talent_all = talent_actor + talent_model

        session.close()

        return talent_all

    def get_all_by_type(self, type: str) -> list:
        '''Returns talent list based on type provided'''

        self._validate_string_input("Type", type)

        session = self._db_session()

        talent_by_type = []

        if type == "actor":
            talent_by_type = session.query(Actor).filter(Actor.type == "actor").all()

        if type == "model":
            talent_by_type = session.query(Model).filter(Model.type == "model").all()

        session.close()

        return talent_by_type

    def update(self, talent_object):
        '''Updates talent list based on talent_id provided'''

        if talent_object is None or (not isinstance(talent_object, Model) and not isinstance(talent_object, Actor)):
            raise ValueError("Invalid Talent Object")

        session = self._db_session()

        existing_talent = None

        if isinstance(talent_object, Actor):

            existing_talent = session.query(Actor).filter(Actor.id == talent_object.id).first()

        if isinstance(talent_object, Model):

            existing_talent = session.query(Model).filter(Actor.id == talent_object.id).first()

        if existing_talent is None:
            raise ValueError("Talent does not exist")

        existing_talent.copy(talent_object)

        session.commit()
        session.close()


    def delete(self, talent_id: int):
        '''Deletes talent from list based on talent_id provided'''

        self._validate_integer_input("Talent ID", talent_id)

        session = self._db_session()

        existing_talent = session.query(Actor).filter(Actor.id == talent_id).first()

        if existing_talent is None:
            raise ValueError("Talent does not exist")

        if existing_talent.type != "actor":

            existing_talent = session.query(Model).filter(Model.id == talent_id).first()

        session.delete(existing_talent)

        session.commit()

        session.close()


    @staticmethod
    def _validate_string_input(display_name, str_value):
        """ Private helper to validate string values """

        if str_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if str_value == "":
            raise ValueError(display_name + " cannot be empty.")

    @staticmethod
    def _validate_integer_input(display_name, int_value):
        """ Private helper to validate integer values """

        if type(int_value) != type(0):
            raise ValueError(display_name + " has to be an integer.")

        if int_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if int_value == "":
            raise ValueError(display_name + " cannot be empty.")

        if int_value < 0 :
            raise ValueError(display_name + " cannot be negative.")

