from src.main.domain.enem.Handler import ENEMHandler
from src.main.data.JSONExporter import JSONExporter


class Operation:

    def __init__(self,
                 repo: JSONExporter,
                 handler: ENEMHandler,
                 working_dir: str
                 ):
        self.handler = handler
        self.repo = repo
        self.working_dir = working_dir

    def run(self):
        pre_dir = self.working_dir + "/preprocessor/"
        os.mkdir(pre_dir)

        output = "/out.pdf"
        self.handler.pre_process(output, pre_dir)

        results = []
        pos_dir = working_dir + "/posprocessor/"
        os.mkdir(pos_dir)

        def on_next(question):
            q_dir = pos_dir + "/" + str(len(results) + 1)
            m = self.handler.pos_process(question, q_dir)
            results.append(m)

        def on_completed():
            if self.handler.validate(results):
                for q in results:
                    self.repo.save(q)
            else:
                print("Not valid result")

        split_dir = self.working_dir + "/splitter/"
        os.mkdir(split_dir)
        self.handler.split(output, split_dir). \
            subscribe(on_next=on_next, on_completed=on_completed)
