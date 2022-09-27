import json
import keyword


class ParsableFromJSON:
    pass


class Location(ParsableFromJSON):
    pass


class AdvertParser:
    LOCATION = 'location'

    def parse_class(self, instance: ParsableFromJSON, mapping: dict):
        for k in mapping:
            attribute_name = k
            attribute_value = mapping[k]

            if keyword.iskeyword(k):
                attribute_name += '_'

            if attribute_name == self.LOCATION:
                attribute_value = Location()
                self.parse_class(attribute_value, mapping[k])

            setattr(instance, attribute_name, attribute_value)


class ChangeColorMixin:
    def __repr__(self):
        return f'\033[1;{self.repr_color_code};40m'


class Advert(ChangeColorMixin, ParsableFromJSON):
    repr_color_code = 33
    PRICE = "_price"

    @property
    def price(self):
        if self.PRICE in self.__dict__:
            return self._price

        return 0

    @price.setter
    def price(self, value: int):
        if value < 0:
            raise ValueError("must be >= 0")

        self._price = value

    def __init__(self, mapping: dict):
        parser = AdvertParser()
        parser.parse_class(self, mapping)

    def __repr__(self):
        return super().__repr__() + f'{self.title} | {self.price} ₽'


if __name__ == '__main__':
    a = '{"title": "aaaa", "price": 1}'
    mapping = json.loads(a)

    advert = Advert(mapping)

    print(advert)
