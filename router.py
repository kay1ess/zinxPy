import abc


class BaseRouter:

    def before_handle(self, request):
        pass

    @abc.abstractmethod
    def handle(self, request):
        raise NotImplementedError

    def after_handle(self, request):
        pass
