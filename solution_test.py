
import pytest
import pandas as pd
from io import StringIO
from solution import Ingredient, Recipe

CSV_CONTENT = StringIO("""Raw Material ID;Similarity Index;Melting Point;Availability in Country;Price
6Z9K9FXGBN9Y1GXA;6489;200;ALL except China;$6.00
P5XJ8TYFZZPV79EX;231;230;ALL;$15.00
X5VC25AYKD8CE3Z0;54;210;ALL;$3.00
9Z70ZMMBEA1863YG;6489;220;ALL;$6.50
5265NVB2GBHNQN2C;6489;190;ALL;$5.50
""")

@pytest.fixture
def optimizer():
    df = pd.read_table(CSV_CONTENT, sep=";")
    print(df)
    return Recipe(df)

def test_ingredient_availability():
    item = Ingredient({
        'Raw Material ID': '123',
        'Similarity Index': 1000,
        'Melting Point': 100,
        'Availability in Country': 'ALL except China',
        'Price': '$10.00'
    })
    assert not item.is_available_in_china()

def test_find_substitute(optimizer):
    sub = optimizer.find('6Z9K9FXGBN9Y1GXA')
    assert sub is not None
    assert sub.id != '6Z9K9FXGBN9Y1GXA'

def test_optimize_recipe(optimizer):
    optimizer.optimize()
    print(optimizer.final_recipe)
    assert len(optimizer.final_recipe) == 3

def test_cost_and_melting_point(optimizer):
    optimizer.optimize()
    cost, mp = optimizer.calculate_cost_and_melting_point()
    assert 0 < cost < 20
    assert 190 <= mp <= 230
