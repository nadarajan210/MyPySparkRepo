
import pytest
from lib.DataReader import read_customers, read_orders
from lib.DataManipulation import filter_closed_orders,filter_orders_generic
from lib.ConfigReader import get_app_config



def test_read_customers_df(spark):
    customers_count = read_customers(spark, "LOCAL").count()
    assert customers_count == 12435

def test_read_orders_df(spark):
    orders_count = read_orders(spark, "LOCAL").count()
    assert orders_count == 68884    

def test_filter_closed_orders(spark):
    orders_df = read_orders(spark, "LOCAL")
    filtered_count = filter_closed_orders(orders_df).count()
    assert filtered_count == 7556

def test_read_app_config():
    config = get_app_config("LOCAL")
    assert config["orders.file.path"] == "data/orders.csv"

@pytest.mark.parametrize(
"entry1,count",
[("CLOSED", 7556),
("PENDING_PAYMENT", 15030),
("COMPLETE", 22900)])

def test_check_count_df(spark,entry1,count):
    orders_df = read_orders(spark, "LOCAL")
    filtered_count = filter_orders_generic(orders_df,entry1).count()
    assert filtered_count == count
