from sqlalchemy import Column, Integer, String
from abstract_talent import AbstractTalent
import datetime

class Model(AbstractTalent):
    '''Maintain the details of model'''

    VEDETTE = "vedette"
    MODEL_TYPE = "model"


    model_type = Column(String(20))

    def __init__(self, first_name, last_name, talent_num, date_debut, model_type):
        '''Constructor of Model object'''

        Model._validate_string_input("Model Type", model_type)
        self.model_type = model_type

        super().__init__(first_name, last_name, talent_num, date_debut)

        self.type = Model.MODEL_TYPE

    def get_model_type(self) ->str:
        '''Return model type'''
        return self.model_type

    def is_vedette(self) ->bool:
        '''Return True if model is a vedette
            and False if the model is not a vedette'''
        if self.get_model_type() == Model.VEDETTE:
            return True
        else:
            return False

    def get_details(self) ->str:
        '''Returns the model's details in a printable format'''

        return '{} with id: {} , talent number: {}, Year debut: {} is a {} model'.format(self.get_full_name(),self.get_id(),
                                                                                         self.get_talent_num(),self.get_year_debut(),
                                                                                         self.get_model_type())
    def get_type(self) ->str:
        '''Return model for any object in this class'''
        return Model.MODEL_TYPE

    def to_dict(self) ->dict:
        '''Return a dictionary representation of a model'''
        dict = {}
        dict['id'] = self.id
        dict['first_name'] = self.first_name
        dict['last_name'] = self.last_name
        dict['talent_num'] = self.talent_num
        dict['date_debut'] = str(self.date_debut)
        dict['model_type'] = self.model_type
        dict['type'] = self.type

        return dict

    def copy(self,object):
        """Copies data from a Student object to this Student object"""
        self._validate_string_input("Object", object)

        if isinstance(object, Model):
            super().copy(object)
            self.type = object.type
            self.model_type = object.model_type

    @staticmethod
    def _validate_string_input(display_name, str_value):
        """ Private helper to validate string values """

        if str_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if str_value == "":
            raise ValueError(display_name + " cannot be empty.")
