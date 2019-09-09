from sqlalchemy import Column, Integer, String
from abc import ABCMeta, abstractmethod
import datetime

from base import Base

class AbstractTalent(Base):
    """ AbstractTalent - Maintains the details of a AbstractTalent """

    __tablename__ = "talent"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    talent_num = Column(String(100), nullable=False)
    date_debut = Column(String(100), nullable=False)
    type = Column(String(10))


    def __init__(self, first_name, last_name, talent_num, date_debut):
        '''Constructors of AbstractTalent'''

        AbstractTalent._validate_string_input("First Name", first_name)
        self.first_name = first_name
        AbstractTalent._validate_string_input("Last Name", last_name)
        self.last_name = last_name
        AbstractTalent._validate_string_input("Talent Number", talent_num)
        self.talent_num = talent_num
        AbstractTalent._validate_string_input("Date Debut", date_debut)
        self.date_debut = datetime.datetime.strptime(date_debut, "%Y-%m-%d %H:%M:%S")

    def get_full_name(self) -> str:
        '''Return full name of talent'''
        return self.first_name + ", " + self.last_name

    def get_talent_num(self) -> str:
        '''Return talent number of talent'''
        return self._talent_num

    def get_year_debut(self):
        '''Return year debuted of talent'''
        year_debut = self.date_debut
        return year_debut.year

    def get_date_debut(self):
        '''Return date debuted of talent'''
        return self._date_debut

    def get_years_debut(self):
        '''Return year debuted of talent'''
        year_now = datetime.datetime.now()
        year_join = self.get_year_debut()
        return year_now.year - year_join

    @abstractmethod
    def to_dict(self) ->dict:
        '''Return a dictionary representation of a talent'''
        raise NotImplementedError("Must be implemented in subclass")

    @abstractmethod
    def copy(self,object):
        """Copies data from a Student object to this Student object"""

        self._validate_string_input("Object", object)

        if isinstance(object, AbstractTalent):
            self.first_name = str(object.first_name)
            self.last_name = str(object.last_name)
            self.talent_num = str(object.talent_num)
            self.date_debut = str(object.date_debut)

    @abstractmethod
    def get_details(self) -> str:
        '''Return details of talent'''
        raise NotImplementedError("Must be implemented in subclass")

    @abstractmethod
    def get_type(self) -> str:
        '''Return type of talent'''
        raise NotImplementedError("Must be implemented in subclass")

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

