class ImagingTest:
    def __init__(self, name, description, image_path):
        self.name = name
        self.description = description
        self.image_path = image_path

    def set_image(self,path):
        self.image_path = path

    def set_name(self, name):
        self.name = name

    def set_description(self,description):
        self.description = description

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description



class RTG(ImagingTest):
    def __init__(self, name, description, image_path):
        super().__init__(name,description,image_path)


class TK(ImagingTest):
    def __init__(self, name, description, image_path):
        super().__init__(name,description,image_path)

class MR(ImagingTest):
    def __init__(self, name, description, image_path):
        super().__init__(name,description,image_path)

class USG(ImagingTest):
    def __init(self,name,description,image_path):
        super().__init__(name,description,image_path)













