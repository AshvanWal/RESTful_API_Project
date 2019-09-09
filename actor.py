from sqlalchemy import Column, Integer, String
from abstract_talent import AbstractTalent
import datetime

class Actor(AbstractTalent):
    '''Maintain details of Actor class'''
    ACTOR_TYPE = "actor"


    movie_list = Column(String(100))
    award_num = Column(Integer, nullable= True)
    # type = Column(String(20), nullable=False)

    def __init__(self, first_name, last_name, talent_num, date_debut,award_num):
        '''Constructor - Initializes the main attributes for the actor'''

        self.movie_list = []
        Actor._validate_integer_input("Award Number", award_num)

        self.award_num = award_num
        super().__init__(first_name, last_name, talent_num, date_debut)

        self.type = Actor.ACTOR_TYPE

    def add_movie(self, new_movie):
        '''Add new movie to list of movie actor plays'''
        Actor._validate_string_input("New Movie", new_movie)

        self.movie_list.append(new_movie)

    def movie_to_string(self):
        """Transform list to string"""
        self.movie_list = "".join(self.movie_list)


    def get_movie_list(self) ->list:
        '''Return movie list'''
        return self.movie_list

    def get_movie_summary(self) ->str:
        '''Get movies actor plays'''
        if len(self._movie_list) > 0:
            movie_list = ', '.join(str(movie) for movie in self.movie_list)
            details = self.get_full_name() + " is an actor in the " + movie_list
            return details
        else:
            return "{} has no movie".format(self.get_full_name())

    def get_num_movie(self) ->int:
        '''Get number of movies actor plays'''
        return len(self.movie_list)

    def get_num_award(self) ->int:
        '''Get number of award actor has'''
        return self.award_num


    def get_details(self) ->str:
        '''Returns the actor's details in a printable format'''
        if self.get_num_award() < 1:
            return '{} id {} talent number {} year debuted {} has no award'.format(self.get_full_name(),
                                                                                   self.get_id(),
                                                                                   self.get_talent_num(),
                                                                                   self.get_year_debut())
        else:
            return '{} id {} talent number {} year debuted {} has {} awards'.format(self.get_full_name(),
                                                                                    self.get_id(),
                                                                                    self.get_talent_num(),                                                                                       self.get_year_debut(),
                                                                                         self.get_num_award())


    def to_dict(self) -> dict:
        '''Return a dictionary representation of an actor'''
        dict = {}
        dict['id'] = self.id
        dict['first_name'] = self.first_name
        dict['last_name'] = self.last_name
        dict['talent_num'] = self.talent_num
        dict['date_debut'] = str(self.date_debut)
        dict['movie_list'] = self.movie_list
        dict['award_num'] = self.award_num
        dict['type'] = Actor.ACTOR_TYPE
        return dict


    def copy(self,object):
        """Copies data from a Talent object to this Talent object"""
        self._validate_string_input("Object", object)

        if isinstance(object, Actor):
            super().copy(object)
            self.type = object.type
            self.award_num = object.award_num
            self.movie_list = object.get_movie_list()

    @staticmethod
    def _validate_integer_input(display_name, int_value):
        """ Private helper to validate string values """

        if type(int_value) != type(0):
            raise ValueError(display_name + " has to be an integer.")

        if int_value < 0 :
            raise ValueError(display_name + " cannot be negative.")

        if int_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if int_value == "":
            raise ValueError(display_name + " cannot be empty.")

    @staticmethod
    def _validate_string_input(display_name, int_value):
        """ Private helper to validate string values """

        if int_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if int_value == "":
            raise ValueError(display_name + " cannot be empty.")
