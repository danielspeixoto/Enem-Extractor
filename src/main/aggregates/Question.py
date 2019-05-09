class Question:

    def __init__(self,
                 identifier: str,
                 source: str,
                 variant: str,
                 edition: int,
                 number: int,
                 item_code: str,
                 domain: str,
                 stage: int,
                 view: str
                 ):
        self.id = identifier
        self.source = source
        self.variant = variant
        self.edition = edition
        self.number = number
        self.item_code = item_code
        self.domain = domain
        self.stage = stage
        self.view = view
