from relational_algebra import *


Restaurant = Relation("Restaurant")
Branch = Relation("Branch")
Table = Relation("'Table'")
Menu_Item = Relation("Menu_Item")
Appetizer = Relation("Appetizer")
Main_Dish = Relation("Main_Dish")
Drink = Relation("Drink")
Employee = Relation("Employee")
Manager = Relation("Manager")
Waiter = Relation("Waiter")
Chef = Relation("Chef")
Customer = Relation("Customer")
Order = Relation("'Order'")
Occupies = Relation("Occupies")
Menu_Item_Branch = Relation("Menu_Item_Branch")
Includes = Relation("Includes")


# Question 1

Q1 = Projection(
    Selection(
        Menu_Item,
        GreaterThan("price", 20.00)
    ),
    ["name", "description"]
)



# Question 2

_appetizers = Projection(Appetizer, ["item_id"])
_main_dishes = Projection(Main_Dish, ["item_id"])

Q2 = _appetizers | _main_dishes



# Question 3

_all_items = Projection(Menu_Item, ["item_id"])
_included_items = Projection(Includes, ["item_id"])

Q3 = _all_items - _included_items



# Question 4

_order_101 = Selection(
    Order,
    Equals("order_id", 101)
)

_order_waiter = ThetaJoin(
    _order_101,
    Waiter,
    Equals("'Order'.waiter_id", "Waiter.employee_id")
)

_waiter_employee = ThetaJoin(
    _order_waiter,
    Employee,
    Equals("Waiter.employee_id", "Employee.employee_id")
)

Q4 = Projection(
    _waiter_employee,
    ["Employee.name"]
)



# Question 5

_boston_branches = Selection(
    Branch,
    Equals("city", "Boston")
)

_boston_menu = NaturalJoin(
    _boston_branches,
    Menu_Item_Branch
)

_boston_items = NaturalJoin(
    _boston_menu,
    Menu_Item
)

Q5 = Projection(
    _boston_items,
    ["name", "price"]
)



# Question 6

_fresh_pho = Selection(
    Menu_Item,
    Equals("name", "Fresh Pho")
)

_pho_orders = NaturalJoin(
    _fresh_pho,
    Includes
)

_customer_orders = NaturalJoin(
    _pho_orders,
    Order
)

_pho_customers = ThetaJoin(
    _customer_orders,
    Customer,
    Equals("'Order'.customer_id", "Customer.customer_id")
)

Q6 = Projection(
    _pho_customers,
    ["first_name", "last_name"]
)



# Question 7

_cancelled_orders = Selection(
    Order,
    Equals("status", "CANCELLED")
)

_cancelled_waiters = ThetaJoin(
    _cancelled_orders,
    Waiter,
    Equals("'Order'.waiter_id", "Waiter.employee_id")
)

_cancelled_waiter_ids = Projection(
    _cancelled_waiters,
    ["employee_id"]
)

_all_waiter_ids = Projection(
    Waiter,
    ["employee_id"]
)

_valid_waiter_ids = _all_waiter_ids - _cancelled_waiter_ids

_valid_waiters = ThetaJoin(
    _valid_waiter_ids,
    Employee,
    Equals("employee_id", "Employee.employee_id")
)

Q7 = Projection(
    _valid_waiters,
    ["name"]
)



# Question 8

_emp5 = Selection(
    Employee,
    Equals("employee_id", 5)
)

_same_branch = ThetaJoin(
    Employee,
    _emp5,
    And(
        Equals("Employee.branch_number", "Employee_2.branch_number"),
        Equals("Employee.restaurant_id", "Employee_2.restaurant_id")
    )
)

_not_emp5 = Selection(
    _same_branch,
    Not(Equals("Employee.employee_id", 5))
)

Q8 = Projection(
    _not_emp5,
    ["Employee.name"]
)



# Question 9

_all_main_dishes = Projection(Main_Dish, ["item_id"])

_branch_item_pairs = Projection(
    Menu_Item_Branch,
    ["branch_number", "restaurant_id", "item_id"]
)

Q9 = _branch_item_pairs / _all_main_dishes



# Question 10

_expensive_pairs = ThetaJoin(
    Menu_Item,
    Menu_Item,
    GreaterThan("Menu_Item_2.price", "Menu_Item.price")
)

_not_max_items = Projection(
    _expensive_pairs,
    ["Menu_Item.item_id"]
)

_max_items = _all_items - _not_max_items

_max_item_names = ThetaJoin(
    _max_items,
    Menu_Item,
    Equals("item_id", "Menu_Item.item_id")
)

Q10 = Projection(
    _max_item_names,
    ["name"]
)
