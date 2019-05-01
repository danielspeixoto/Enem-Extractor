from src.main.domain.enem.Handler import ENEMHandler
from src.main.data.JSONExporter import JSONExporter


class Operation:

    def __init__(self,
                 repo: JSONExporter
                 ):
        self.repo = repo

    def run(self, handler: ENEMHandler):
        handler.pre_process()

        results = []

        def on_next(question):
            m = handler.pos_process(question)
            results.append(m)

        def on_completed():
            if handler.validate(results):
                for q in results:
                    self.repo.save(q)
            else:
                print("Not valid result")

        handler.split(). \
            subscribe(on_next=on_next, on_completed=on_completed)
