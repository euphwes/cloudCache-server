""" Contains JsonMixin class which provides easy JSON serialization for classes which extend
SQLAlchemy declarative base. """

# pylint: disable=R0903
# disable "too few public methods" warning, this Mixin has a single purpose

from json import dumps
from arrow.arrow import Arrow
from collections import OrderedDict

# -------------------------------------------------------------------------------------------------

class JsonMixin(object):
    """ Class which provides easy JSON serialization """

    def _to_json(self, attrs, compact=True, additional_kvp=None):
        """ Returns a JSON representation of this object. """

        json = OrderedDict()

        for attribute in attrs:
            attr_val = getattr(self, attribute)

            # if the attribute is an Arrow object, make the value just the string representation,
            # rather than the Arrow object itself, since json.dumps doesn't like Arrow objects
            if isinstance(attr_val, Arrow):
                attr_val = str(attr_val.to('local'))

            json[attribute] = attr_val

        if additional_kvp:
            for key, value in additional_kvp.items():
                json[key] = value

        kwargs = dict()
        kwargs['indent'] = 0 if compact else 4
        kwargs['separators'] = (',', ':') if compact else (',', ': ')

        return dumps(json, **kwargs)
