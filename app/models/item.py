"""Items Model"""
from marshmallow import Schema, fields


class Item:
    """Item Model"""

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class ItemStore:
    """Item store  Model"""

    def __init__(self):
        self.items = []
        self.next_id = 1

    def create_item(self, name, description):
        """Create item

        Args:
            name (str)
            description (str)

        Returns:
            Item
        """

        item = Item(self.next_id, name, description)
        self.items.append(item)
        self.next_id += 1
        return item

    def get_item(self, item_id):
        """Get item

        Args:
            item_id (int)

        Returns:
            Item|None
        """

        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def update_item(self, item_id, name, description):
        """update item

        Args:
            item_id (int)
            name (str)
            description (str)

        Returns:
            Item|None
        """

        item = self.get_item(item_id)
        if item:
            item.name = name
            item.description = description
            return item
        return None

    def delete_item(self, item_id):
        """delete item

        Args:
            item_id (int)

        Returns:
            Item|None
        """

        item = self.get_item(item_id)
        if item:
            self.items.remove(item)
            return item
        return None


class DefaultFileResponseSchema(Schema):
    """Default File Response Schema"""

    message = fields.Str()
    path = fields.Str()


class DefaultResponseSchema(Schema):
    """Default Response Schema"""

    message = fields.Str()


class ItemSchema(Schema):
    """Item Schema"""

    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
