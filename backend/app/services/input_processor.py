from app.repositories.input_repository import InputRepository


class InputProcessor:
    def __init__(self, repository: InputRepository):
        self.repository = repository

    def process_pending(self):
        pending_inputs = self.repository.list_pending()
        for input_record in pending_inputs:
            self.repository.update_status(input_record, "PROCESSING")
            self.repository.update_status(input_record, "COMPLETED")
            return input_record
        return None
