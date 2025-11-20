class SearchIndex:
    def __init__(self):
        self.index = {} # inverted index: term -> set of product IDs
    
    def add_product(self, product_id, name, description):
        """Add product to search index"""
        text = f"{name} {description}".lower()
        words = text.split()

        for word in words:

            word = word.strip('.,!?;:')