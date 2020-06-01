from flask import Flask, Response
import json
from models import Company, Person
import logging
from flask_restful import Api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

@app.route('/companies/<index>/employees')
def company(index):
    logger.info(f"Received request for fetching employees working for company with index - {index}")
    try:
        company = Company.objects(index=index).first()
        if not company:
            return output(message='Company not found', status=404)
        return output(data=company.employees())
    except Exception as ex:
        logger.exception(ex)
        return output(message=str(ex), status=500)


@app.route('/people/<index1>/<index2>/populate_details_and_common_friends')
def populate_details_and_common_friends(index1, index2):
    logger.info(f"Received request for fetching employees with index - {index1} and {index2} and their common friends")
    try:
        person = Person.objects(index=index1).first()
        if not person:
            return output(message='First person not found', status=404)
        other_person = Person.objects(index=index2).first()
        if not other_person:
            return output(message='Second person not found', status=404)
        data = person.details_with_common_friends(other_person)
        return output(data=data)
    except Exception as ex:
        logger.exception(ex)
        return output(message=str(ex), status=500)


def output(data=None, message='', status=200):
    """Returns results containing data and message"""
    if data is None:
        data = []
    result = dict(data=data,
                  message=message)
    api_response = json.dumps(result)
    return Response(api_response, status, mimetype='application/json')
    


if __name__ == "__main__":
    app.run(debug=True)
