from .base_result import BaseResult


class StorageResult(BaseResult):

    def __init__(self,
                 path=None,
                 additional_parameters_dict: dict = None,
                 output=None,
                 error=None):
        # the path of the backup on the storage system
        self.path = path
        # additional parameters or information, which the storage system maybe needs for a future retrieving process
        self.additional_parameters_dict = additional_parameters_dict
        # string output of a backup, which is an information or similar
        self.output = output
        # error
        self.error = error

    @staticmethod
    def with_error(error, output=None):
        return StorageResult(error=error, output=output)
