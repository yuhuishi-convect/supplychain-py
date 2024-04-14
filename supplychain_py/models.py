from abc import ABC, abstractmethod
from typing import List, Dict

class Node(ABC):
    """
    A node of the supply chain 
    """
    pass


class Location:
    """
    A geographical location of a node
    """
    def __init__(self, latitude: float, longitude: float, name=None) -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} ({self.latitude}, {self.longitude})"

    def __repr__(self) -> str:
        return f"{self.name} ({self.latitude}, {self.longitude})"


class Product:
    def __init__(self, name: str, unit_holding_cost:float=0.0) -> None:
        self.name = name
        self.unit_holding_cost = unit_holding_cost
        
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Product):
            return self.name == o.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{self.name}"


class Lane:
    """
    A transportation lane between two nodes
    """
    def __init__(self, origin: Node, destination: Node, unit_cost: float=0, minimum_quantity: float=0, time: int=0):
        self.origin = origin
        self.destination = destination
        self.unit_cost = unit_cost
        self.minimum_quantity = minimum_quantity
        self.time = time

    def __str__(self) -> str:
        return f"{self.origin} -> {self.destination}"
    
    def __repr__(self) -> str:
        return f"{self.origin} -> {self.destination}"


class Customer(Node):
    """
    A customer
    """

    def __init__(self, name: str, location: Location) -> None:
        self.name = name
        self.location = location
        self.products = {}

    def __str__(self) -> str:
        return f"{self.name} ({self.location})"

    def __repr__(self) -> str:
        return f"{self.name} ({self.location})"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Customer):
            return self.name == __o.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def add_product(self, product: Product, demand: float):
        """
        Indicate the demand of a product by the customer
        """
        self.products[product] = demand


    
class Supplier(Node):
    """
    A supplier
    """

    def ___init__(self, name: str, location: Location) -> None:
        self.name = name
        self.location = location

        self.unit_cost = {}
        self.maximum_throughput = {}


    def add_product(self, product: Product, unit_cost:float, maximum_throughput:float=float("inf")):
        """
        Indicate a supplier can supply a product at the unit cost, with a maximum throughput
        """
        self.unit_cost[product] = unit_cost
        self.maximum_throughput[product] = maximum_throughput

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Supplier):
            return self.name == __o.name

        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f"{self.name} ({self.location})"

    def __repr__(self) -> str:
        return f"{self.name} ({self.location})"


class Storage(Node):
    """
    A storage location
    """

    def __init__(self, name: str, location: Location, fixed_cost:float=0.0, opening_cost:float=0.0, closing_cost:float=float("-inf"), initial_opened:bool=True):
        self.name = name
        self.location = location
        self.fixed_cost = fixed_cost
        self.opening_cost = opening_cost
        self.closing_cost = closing_cost
        self.initial_opened = initial_opened

        self.initial_inventory = {}
        self.unit_handling_cost = {}
        self.maximum_throughput = {}
        self.additional_stock_coverage = {}

    def add_product(self, product: Product, initial_inventory:float=0.0, unit_handling_cost=0.0, maximum_throughput=float("inf"), additional_stock_cover=0.0):
        """
        Indicate a storage location can store a product with the initial inventory, unit handling cost, maximum throughput and additional stock coverage
        """
        self.initial_inventory[product] = initial_inventory
        self.unit_handling_cost[product] = unit_handling_cost
        self.maximum_throughput[product] = maximum_throughput
        self.additional_stock_coverage[product] = additional_stock_cover

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Storage):
            return self.name == __o.name

        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f"{self.name} ({self.location})"

    def __repr__(self) -> str:
        return f"{self.name} ({self.location})"


class Plant(Node):
    """
    A production plant
    """

    def __init__(self, name, location: Location, fixed_cost=0.0, opening_cost=0.0, closing_cost=float("inf"), initial_opened=True):
        self.name = name
        self.location = location
        self.fixed_cost = fixed_cost
        self.opening_cost = opening_cost
        self.closing_cost = closing_cost
        self.initial_opened = initial_opened

        self.unit_cost = {}
        self.time = {}
        self.maximum_throughput = {}
        self.bill_of_material = {}


    def add_product(self, product: Product, bill_of_material:dict, unit_cost:float, maximum_throughput:float=float("inf"), time:int=0):
        """
        Indicate a plant can produce a product at the unit cost, with the time and maximum throughput
        """
        self.unit_cost[product] = unit_cost
        self.time[product] = time
        self.maximum_throughput[product] = maximum_throughput
        self.bill_of_material[product] = bill_of_material

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Plant):
            return self.name == __o.name

        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f"{self.name} ({self.location})"

    def __repr__(self) -> str:
        return f"{self.name} ({self.location})"


class Demand:
    """
    The demand a customer has for a product
    """ 

    def __init__(self, customer: Customer, product: Product, service_level:float, demand:list) -> None:
        self.customer = customer
        self.product = product
        self.service_level = service_level
        self.demand = demand

    def __str__(self) -> str:
        return f"{self.customer} -> {self.product}"

    def __repr__(self) -> str:
        return f"{self.customer} -> {self.product}"


class SupplyChainModel:
    """
    A supply chain model
    """

    def __init__(
        self,
        horizon:int,
        products:List[Product],
        storages:List[Storage],
        suppliers:List[Supplier],
        customers:List[Customer],
        plants:List[Plant],
        lanes:List[Lane],
        demands:List[Demand],

        lanes_in:Dict[Node, List[Lane]],
        lanes_out:Dict[Node, List[Lane]],
    ) -> None:
        self.horizon = horizon
        self.products = products
        self.storages = storages
        self.suppliers = suppliers
        self.customers = customers
        self.plants = plants
        self.lanes = lanes
        self.demands = demands

        self.lanes_in = lanes_in
        self.lanes_out = lanes_out

        self.model = None


    def add_demand(self, customer: Customer, product: Product, demand: List[float], service_level:float=1.0):
        """
        Add customer demand for a product. The demand is specifeid for each time period
        """
        if service_level < 0 or service_level > 1:
            raise ValueError("Service level must be between 0 and 1")

        self.demands.append(Demand(customer, product, service_level, demand))
    
    def add_product(self, product: Product):
        """
        Add a product to the supply chain
        """
        self.products.append(product)

    def add_customer(self, customer: Customer):
        """
        Add a customer to the supply chain
        """
        self.customers.append(customer)

    def add_supplier(self, supplier: Supplier):
        """
        Add a supplier to the supply chain
        """
        self.suppliers.append(supplier)

    def add_storage(self, storage: Storage):
        """
        Add a storage location to the supply chain
        """
        self.storages.append(storage)

    def add_plant(self, plant: Plant):
        """
        Add a plant to the supply chain
        """
        self.plants.append(plant)

    def add_lane(self, lane: Lane):
        """
        Add a lane to the supply chain
        """
        self.lanes.append(lane)

        if lane.destination not in self.lanes_in:
            self.lanes_in[lane.destination] = []
        self.lanes_in[lane.destination].append(lane)

        if lane.origin not in self.lanes_out:
            self.lanes_out[lane.origin] = []
        self.lanes_out[lane.origin].append(lane)


    # querying methods
    def get_demands(self, customer:Customer, product:Product, time:int):
        """
        Get the demand for a customer and product
        """
        for demand in self.demands:
            if demand.customer == customer and demand.product == product:
                return demand.demand[time]

        return None


    def get_service_level(self, customer:Customer, product:Product):
        """
        Get the service level for a customer and product
        """
        for demand in self.demands:
            if demand.customer == customer and demand.product == product:
                return demand.service_level

        return None


    def get_lanes_in(self, node:Node):
        """
        Get the lanes that lead to a node
        """
        return self.lanes_in[node]


    def get_lanes_out(self, node:Node):
        """
        Get the lanes that leave a node
        """
        return self.lanes_out[node]


        
