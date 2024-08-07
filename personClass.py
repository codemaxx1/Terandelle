'''
    Person class, for use with loading data on peoplpe
'''
class Person:
    def __init__(self, personData):
        self.firstName = personData.firstName
        self.lastName = personData.lastName
        self.birthday = personData.birthday
        self.pronouns = personData.pronouns
