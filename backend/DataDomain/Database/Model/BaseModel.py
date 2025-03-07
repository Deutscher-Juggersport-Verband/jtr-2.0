
class BaseModel:

    __abstract__ = True

    @staticmethod
    def toCamelCase(snakeStr):
        components = snakeStr.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def serialize(self):
        return {self.toCamelCase(c.name): getattr(self, c.name)
                for c in self.__table__.columns}
