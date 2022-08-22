class Project:
    def __init__(self, name, directory_path):
        self.name = name
        self.directory_path = directory_path

    def add_process(self):
        pass

    def validate(self):
        #  TODO: validate the layers and the processes present in the project
        pass

    def add_layers(self):
        #  TODO: add dasemaps, geodata wms and other generic layers
        pass

    def write_metadata(self):
        pass

    def read_metadata(self):
        pass

    @staticmethod
    def initiate():
        # Search layers in current project
        # check metadata
        # create a project isinstance
        # validate data
        # return project isinstance
        pass


# Or not class-based


def validate_process_layers():
    pass


def validate_process_data():
    pass


def get_existing_processes():
    pass


def calculate_danger():
    """Calculate the danger zones of a process"""

    # TODO:
    # - depending on the process do what is necessary
