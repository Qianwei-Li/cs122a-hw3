from relational_algebra import *

class Expressions:

    # --------------------------------------------------
    # Base Relations
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Question 1
    # --------------------------------------------------

    Q1 = Projection(
        Selection(Menu_Item, GreaterThan("price", 20.00)),
        ["name", "description"]
    )

    # --------------------------------------------------
    # Question 2
    # --------------------------------------------------

    _appetizers = Projection(Appetizer, ["item_id"])
    _main_dishes = Projection(Main_Dish, ["item_id"])
    Q2 = _appetizers | _main_dishes

    # --------------------------------------------------
    # Question 3
    # --------------------------------------------------

    _all_items = Projection(Menu_Item, ["item_id"])
    _included_items = Projection(Includes, ["item_id"])
    Q3 = _all_items - _included_items

    # --------------------------------------------------
    # Question 4
    # --------------------------------------------------

    _order_101 = Selection(Order, Equals("order_id", 101))

    _order_waiter = ThetaJoin(
        _order_101,
        Waiter,
        Equals("'Order'.waiter_id", "Waiter.employee_id")
    )

    _waiter_employee = ThetaJoin(
        _order_waiter,
        Employee,
        Equals("employee_id", "Employee.employee_id")
    )

    Q4 = Projection(_waiter_employee, ["name"])

    # --------------------------------------------------
    # Question 5
    # --------------------------------------------------

    _boston_branches = Selection(Branch, Equals("city", "Boston"))

    _branch_menu = ThetaJoin(
        _boston_branches,
        Menu_Item_Branch,
        And(
            Equals("Branch.branch_number", "Menu_Item_Branch.branch_number"),
            Equals("Branch.restaurant_id", "Menu_Item_Branch.restaurant_id")
        )
    )

    _boston_items = ThetaJoin(
        _branch_menu,
        Menu_Item,
        Equals("Menu_Item_Branch.item_id", "Menu_Item.item_id")
    )

    Q5 = Projection(_boston_items, ["name", "price"])

    # --------------------------------------------------
    # Question 6
    # --------------------------------------------------

    _fresh_pho = Selection(Menu_Item, Equals("name", "Fresh Pho"))

    _pho_orders = ThetaJoin(
        _fresh_pho,
        Includes,
        Equals("Menu_Item.item_id", "Includes.item_id")
    )

    _customer_orders = ThetaJoin(
        _pho_orders,
        Order,
        Equals("Includes.order_id", "'Order'.order_id")
    )

    _pho_customers = ThetaJoin(
        _customer_orders,
        Customer,
        Equals("'Order'.customer_id", "Customer.customer_id")
    )

    Q6 = Projection(_pho_customers, ["first_name", "last_name"])

    # --------------------------------------------------
    # Question 7
    # --------------------------------------------------

    _cancelled_orders = Selection(Order, Equals("status", "CANCELLED"))

    _all_waiters = ThetaJoin(
        Waiter,
        Employee,
        Equals("Waiter.employee_id", "Employee.employee_id")
    )

    _bad_waiters = ThetaJoin(
        _cancelled_orders,
        _all_waiters,
        Equals("'Order'.waiter_id", "Employee.employee_id")
    )

    _good_waiters = _all_waiters - _bad_waiters

    Q7 = Projection(_good_waiters, ["name"])

    # --------------------------------------------------
    # Question 8
    # --------------------------------------------------

    _emp5 = Selection(Employee, Equals("employee_id", 5))
    Employee_2 = Rename(Employee, "Employee_2")

    _same_branch = ThetaJoin(
        Employee,
        Employee_2,
        And(
            Equals("Employee.branch_number", "Employee_2.branch_number"),
            Equals("Employee.restaurant_id", "Employee_2.restaurant_id")
        )
    )

    _same_as_5 = ThetaJoin(
        _same_branch,
        _emp5,
        Equals("Employee_2.employee_id", "employee_id")
    )

    _not_5 = Selection(_same_as_5, Not(Equals("Employee.employee_id", 5)))

    Q8 = Projection(_not_5, ["Employee.name"])

    # --------------------------------------------------
    # Question 9
    # --------------------------------------------------

    _all_main_dishes = Projection(Main_Dish, ["item_id"])

    _main_branch_items = ThetaJoin(
        Menu_Item_Branch,
        Main_Dish,
        Equals("Menu_Item_Branch.item_id", "Main_Dish.item_id")
    )

    _branch_item_pairs = Projection(
        _main_branch_items,
        ["branch_number", "restaurant_id", "item_id"]
    )

    Q9 = _branch_item_pairs / _all_main_dishes

    # --------------------------------------------------
    # Question 10
    # --------------------------------------------------

    Menu_Item_2 = Rename(
        Menu_Item,
        {"item_id": "item_id2", "price": "price2"}
    )

    _more_expensive = ThetaJoin(
        Menu_Item,
        Menu_Item_2,
        GreaterThan("price2", "price")
    )

    _not_max_items = Projection(_more_expensive, ["item_id"])
    _max_items = _all_items - _not_max_items

    _max_item_names = ThetaJoin(
        _max_items,
        Menu_Item,
        Equals("item_id", "Menu_Item.item_id")
    )

    Q10 = Projection(_max_item_names, ["name"])

