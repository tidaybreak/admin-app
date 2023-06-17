"""
    SQLAlchemy-ElasticQuery
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    This extension allow you use the ElasticSearch syntax for search in SQLAlchemy.
    Get a query string and return a SQLAlchemy query

    Example query string:

        {
            "filter" : {
                "or" : {
                    "firstname" : {
                        "equals" : "Jhon"
                    },
                    "lastname" : "Galt",
                    "uid" : {
                        "like" : "111111"
                    }
                },
                "and" : {
                    "status" : "active",
                    "age" : {
                        "gt" : 18
                    }
                }
            },
            "sort" : {
                { "firstname" : "asc" },
                { "age" : "desc" }
            }
        }

"""
import json
from sqlalchemy import and_, or_, desc, asc

__version__ = '0.0.1'


def elastic_query(model, query, session=None, enabled_fields=None):
    """ Public method for init the class ElasticQuery
        :model: SQLAlchemy model
        :query: valid string like a ElasticSearch
        :session: SQLAlchemy session *optional
        :enabled_fields: Fields allowed for make a query *optional
    """
    # TODO: make session to optional
    instance = ElasticQuery(model, query, session, enabled_fields)
    return instance.search()

""" Valid operators """
OPERATORS = {
    'like': lambda f, a: f.like(a),
    'equals': lambda f, a: f == a,
    'gt': lambda f, a: f > a,
    'gte': lambda f, a: f >= a,
    'lt': lambda f, a: f < a,
    'lte': lambda f, a: f <= a,
    'in': lambda f, a: f.in_(a),
    'not_in': lambda f, a: ~f.in_(a),
    'not_equal_to': lambda f, a: f != a,
    'null': lambda f, a: f.is_(None) if a else f.isnot(None)
    }


class ElasticQuery(object):
    """ Magic method """

    def __init__(self, model, query, session=None, enabled_fields=None):
        """ Initializator of the class 'ElasticQuery' """
        self.model = model
        self.query = query
        if hasattr(model, 'query'):
            self.model_query = model.query
        else:
            self.model_query = session.query(self.model)
        self.enabled_fields = enabled_fields

    def search(self):
        """ This is the most important method """
        try:
            if isinstance(self.query, str):
                filters = json.loads(self.query)
            else:
                filters = self.query
        except ValueError:
            return False

        result = self.model_query
        if 'filter'in filters.keys():
            result = self.parse_filter(filters['filter'])
        if 'sort'in filters.keys():
            result = result.order_by(*self.sort(filters['sort']))

        return result

    def parse_filter(self, filters):
        """ This method process the filters """
        for filter_type in filters:
            if filter_type == 'or' or filter_type == 'and':
                conditions = []
                for field in filters[filter_type]:
                    if self.is_field_allowed(field):
                        # {gte lte}
                        if isinstance(filters[filter_type][field], dict):
                            for condition in filters[filter_type][field]:
                                attr = {
                                    condition: filters[filter_type][field][condition]
                                }
                                conditions.append(self.create_query(self.parse_field(field, attr)))
                        else:
                            conditions.append(self.create_query(self.parse_field(field, filters[filter_type][field])))
                if filter_type == 'or':
                    self.model_query = self.model_query.filter(or_(*conditions))
                elif filter_type == 'and':
                    self.model_query = self.model_query.filter(and_(*conditions))
            else:
                if self.is_field_allowed(filter_type):
                    conditions = self.create_query(self.parse_field(filter_type, filters[filter_type]))
                    self.model_query = self.model_query.filter(conditions)
        return self.model_query

    def parse_field(self, field, field_value):
        """ Parse the operators and traduce: ES to SQLAlchemy operators """
        if type(field_value) is dict:
            # TODO: check operators and emit error
            keys = list(field_value.keys())
            operator = keys[0]
            if self.verify_operator(operator) is False:
                return "Error: operador no exite", operator
            value = field_value[operator]
        else:
            operator = u'equals'
            value = field_value
        return field, operator, value

    @staticmethod
    def verify_operator(operator):
        """ Verify if the operator is valid """
        try:
            if hasattr(OPERATORS[operator], '__call__'):
                return True
            else:
                return False
        except ValueError:
            return False

    def is_field_allowed(self, field):
        if self.enabled_fields:
            return field in self.enabled_fields
        else:
            return True

    def create_query(self, attr):
        """ Mix all values and make the query """
        field = attr[0]
        operator = attr[1]
        value = attr[2]
        model = self.model

        if '.' in field:
            field_items = field.split('.')
            field_name = getattr(model, field_items[0], None)
            class_name = field_name.property.mapper.class_
            new_model = getattr(class_name, field_items[1])
            return field_name.has(OPERATORS[operator](new_model, value))

        return OPERATORS[operator](getattr(model, field, None), value)

    def sort(self, sort_dict):
        """ Sort """
        sort_dict = sorted(sort_dict.items(), key=lambda item: item[1]["idx"], reverse=False)
        order = []
        for sort in sort_dict:
            if sort[1]["order"] == "asc":
                order.append(asc(getattr(self.model, sort[0], None)))
            elif sort[1]["order"] == "desc":
                order.append(desc(getattr(self.model, sort[0], None)))
        return order
