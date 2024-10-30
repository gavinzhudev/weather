import pytest
from . import *
from exceptions import CityNotFoundError


def test_search_city():
    city_list = city_service.search_city("beijing", 10)
    assert city_list is not None
    assert len(city_list) >= 1
    assert any("北京市" in element for element in city_list), "列表中没有包含'北京市'的元素"
    city_list = city_service.search_city("广州", 10)
    assert city_list is not None
    assert any("广州市" in element for element in city_list), "列表中没有包含'广州市'的元素"

    with pytest.raises(CityNotFoundError) as e:
        city_service.search_city("不存在的城市", 10)
    assert 404 == e.value.status
    assert 6202 == e.value.code
