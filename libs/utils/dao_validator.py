# Python's Libraries
from libs.utils.decorators import step
from libs.errors.dao_error import DaoError


class DaoValidator(object):

    @classmethod
    @step("Checkin ID value ...")
    def check_Id(self, _id):
        if _id is None:
            raise DaoError("No ID provided.")

        if isinstance(_id, str):
            if _id.isnumeric() is False:
                raise DaoError("ID values should be numeric.")

        return _id
