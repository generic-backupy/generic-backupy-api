from .base_result import BaseResult


class RestoreResult(BaseResult):

    def __init__(self,
                 output=None,
                 error=None):
        # string output of a backup, which is an information or similar
        self.output = output
        # error
        self.error = error

    @staticmethod
    def with_error(error, output=None):
        return RestoreResult(error=error, output=output)
