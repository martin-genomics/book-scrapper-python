# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscrapperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all whitespaces from strings (except certain fields)
        field_names = adapter.field_names()
        fields_to_ignore = ['price_excl_tax', 'price_incl_tax', 'price', 'tax', 'description', "stars", "title", "stock", "url"]

        for field_name in field_names:
            if field_name not in fields_to_ignore:
                value = adapter.get(field_name)
                if value is not None:
                    if isinstance(value, tuple):
                        value = value[0]  # Extract the first element if tuple
                    adapter[field_name] = value.strip() if isinstance(value, str) else value

        # Convert category & product type to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            if value:
                adapter[lowercase_key] = value.lower()

        # Convert price fields to float
        price_keys = ['price_excl_tax', 'price_incl_tax', 'price', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if value:
                value = value.replace('£', '')
                try:
                    adapter[price_key] = float(value)
                except ValueError:
                    adapter[price_key] = 0.0  # Default to 0 if conversion fails

        # Convert stock to integer
        stock_string = adapter.get("stock")
        if stock_string:
            split_string_array = stock_string.split('(')
            if len(split_string_array) < 2:
                adapter['stock'] = 0
            else:
                stock_array = split_string_array[1].split(' ')
                try:
                    adapter['stock'] = int(stock_array[0])
                except ValueError:
                    adapter['stock'] = 0  # Default to 0 if conversion fails

        # Convert reviews to integer
        reviews = adapter.get('reviews')
        try:
            adapter['reviews'] = int(reviews) if reviews is not None else 0
        except ValueError:
            adapter['reviews'] = 0  # Default to 0 if conversion fails

        # Convert stars to integer
        stars_string = adapter.get('stars')
        if stars_string:
            split_stars_array = stars_string.split(' ')
            if len(split_stars_array) > 1:
                stars_text_value = split_stars_array[1].lower()
                stars_map = {
                    'zero': 0,
                    'one': 1,
                    'two': 2,
                    'three': 3,
                    'four': 4,
                    'five': 5
                }
                adapter['stars'] = stars_map.get(stars_text_value, 0)  # Default to 0 if not found

        return item


from mongoengine import connect, Document, StringField, IntField, FloatField

class BookModel(Document):
    url = StringField(required=True)
    title = StringField(required=True)
    category = StringField()
    description = StringField()
    price = FloatField()
    stock = IntField()
    stars = FloatField()
    reviews = FloatField()
    tax = FloatField()
    product_type = StringField()
    price_excl_tax = FloatField()
    price_incl_tax = FloatField()


class SaveToMongoDBPipeline:

    def __init__(self):
        connect(host=f'mongodb+srv://martincodegene:87MpTtsnOBLEdRna@cluster0.ej92x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    def process_item(self, item, spider):
        # Define a new instance of the book model class
        book = BookModel()

        # Assign actual data value to attributes of the class
        book['url'] = item['url']
        book['title'] = item['title']
        book['category'] = item['category'][0]  # Removed trailing comma
        book['description'] = item['description']
        book['product_type'] = item['product_type']
        book['price_excl_tax'] = item['price_excl_tax']
        book['price_incl_tax'] = item['price_incl_tax']
        book['tax'] = item['tax']
        book['stock'] = item['stock']
        book['reviews'] = item['reviews']
        book['stars'] = item['stars']
        book['price'] = item['price']

        # Save the data in the database
        book.save()

        # Return the saved data
        return book
        # return item
    def close_spider(self, item, spider):
        pass

