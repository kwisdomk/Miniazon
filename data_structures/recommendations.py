class ProductGraph:
    def __init__(self):
        # self graph, the big boy. holding everything
        self.graph = {} #a dict. with key -prod.id- and value- related ids-
    
    def add_relationship(self, product_a, product_b): # conn. 2prods -a&b-
        """Addo bi-dir. relationship btwn products"""
        if product_a not in self.graph: # if in me page 4 a aint paging, blank page it 4 a
            self.graph[product_a] = []
        if product_b not in self.graph: # same as upgraph
            self.graph[product_b] = []

        #2-way street. bi directional
        if product_b not in self.graph[product_a]: # go to a's page-> write b, if its not there
            self.graph[product_a].append(product_b)
        if product_a not in self.graph[product_b]: # same as above.
            self.graph[product_b].append(product_a)

    # do i have this product's page in my address book.
    def get_recommendations(self, product_id, limit=3):  # if yes, give me 1st III names
        """Get producto recommendations"""
        if product_id not in self.graph: # if no retun empty list
            return []
        
        return self.graph[product_id][:limit]
    
    def get_stats(self):
        """Returno-desu graph stats fro display"""
        total_connections = sum(len(connections) for connections in self.graph.values())
        return {
            'total_products': len(self.graph),
            'total_connections': total_connections
        }