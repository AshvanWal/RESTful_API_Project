from flask import Flask, request
from talent_agency import TalentAgency
from actor import Actor
from model import Model

import json

app = Flask(__name__)

TALENT_DB = 'talents.sqlite'

talent_agency = TalentAgency(TALENT_DB)

@app.route('/talent_agency/talent',methods=['POST'])
def add_talent():
    """Add an talent to the Talent Agency"""

    content = request.json

    try:
        talent_id = 0
        movie_list = "A"
        if content['type'] is None or content['type'] == "":
            raise ValueError("Type can not be empty")

        if content['type'] == 'actor':

            actor = Actor(content['first_name'],content['last_name'], content['talent_num'], content['date_debut'], content['award_num'])


            for movie in content['movie_list']:
                actor.add_movie(movie)

            actor.movie_to_string()

            talent_id = talent_agency.add_talent(actor)


        if content['type'] == 'model':
            model = Model(content['first_name'],content['last_name'], content['talent_num'], content['date_debut'], content['model_type'])
            talent_id = talent_agency.add_talent(model)


        response = app.response_class(status=200,
                                      response = str(talent_id),
                                      # response=str(movie_list),
                                      )

    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=400
        )
    return response

@app.route('/talent_agency/talent/<int:talent_id>', methods=['PUT'])
def update_talent(talent_id):
    """Updates an existing talent on the Talent Agency"""

    content = request.json


    if talent_id <= 0:
        response = app.response_class(
            status=400
        )
        return response

    try:
        if content['type'] is None or content['type'] == "":
            raise ValueError("Type can not be empty")

        elif content['type'] == 'actor':

            actor = Actor(content['first_name'],content['last_name'], content['talent_num'], content['date_debut'], content['award_num'])
            actor.id = talent_id

            for movie in content['movie_list']:
                actor.add_movie(movie)

            actor.movie_to_string()

            talent_agency.update(actor)

        elif content['type'] == 'model':

            model = Model(content['first_name'],content['last_name'], content['talent_num'], content['date_debut'], content['model_type'])
            model.id = talent_id
            talent_agency.update(model)

        response = app.response_class(status=200)

    except ValueError as e:
        if str(e) == "Talent ID does not exist":

            response = app.response_class(
                response=str(e),
                status=404)
        elif str(e) == "Type can not be empty":

            response = app.response_class(
                response=str(e),
                status=400)
        else:
            response = app.response_class(
                response="Object invalid",
                status=400
            )


    return response

@app.route('/talent_agency/talent/<int:talent_id>',methods=['DELETE'])
def delete_talent(talent_id):
    """Delete an existing talent on the Talent Agency"""


    try:
        talent_agency.delete(talent_id)
        response = app.response_class(status=200)

    except ValueError as e:
        if str(e) == "Talent ID does not exist":

            response = app.response_class(
                response=str(e),
                status=404)
        else:
            response = app.response_class(
                response="Talent ID invalid",
                status=400
            )
    return response

@app.route('/talent_agency/talent/<int:talent_id>',methods=[ 'GET'])
def get_talent(talent_id):
    """Updates an existing talent on the Talent Agency"""
    try:
        talent = talent_agency.get_talent(talent_id)
        response = app.response_class(
            status=200,
            response=json.dumps(talent.to_dict()),
            mimetype='application/json'
        )
        return response

    except ValueError as e:
        response = app.response_class(
            response="Talent ID does not exist",
            status=404)

        return response


@app.route('/talent_agency/talent/all',methods=['GET'])
def get_all_talents():
    """Gets all talents on the Talent Agency"""
    talents= talent_agency.get_all()
    talent_list = []
    for talent in talents:
        talent_list.append(talent.to_dict())

    response = app.response_class(
        status=200,
        response=json.dumps(talent_list),
        mimetype='application/json'
    )

    return response

@app.route('/talent_agency/talent/<talent_type>',methods=[ 'GET'])
def get_talent_type(talent_type):
    """Get talent by type on Talent Agency"""
    try:
        if talent_type != "actor" and talent_type != "model":
            raise ValueError("Type can not be found")
        else:

            talents_by_type = talent_agency.get_all_by_type(talent_type)
            talent_list = []
            for talent in talents_by_type:
                talent_list.append(talent.to_dict())

            response = app.response_class(
                status=200,
                response=json.dumps(talent_list),
                mimetype='application/json'
            )
        return response

    except ValueError as e:
        response = app.response_class(
            response="Type invalid",
            status=400
        )
        return response


if __name__ == "__main__":
    app.run()

