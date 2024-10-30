import React, {useEffect, useState} from 'react';
import {AutoComplete, Card, Input, Space} from 'antd';

const pics = {
    "晴": "qing",
    "阴": "yin",
    "多云": "duoyun",
    "小雨": "xiaoyu",
    "中雨": "zhongyu",
    "大雨": "dayu",
    "阵雨": "zhenyu",
    "雷阵雨": "leizhenyu",
    "暴雨": "baoyu",
    "大暴雨": "dabaoyu",
    "特大暴雨": "tedabaoyu",
    "小雪": "xiaoxue",
    "中雪": "zhongxue",
    "大雪": "daxue",
    "暴雪": "baoxue",
    "阵雪": "zhenxue",
    "雨夹雪": "yujiaxue",
    "雾": "wu",
    "雾霾": "wumai",
    "扬沙": "yangsha",
    "浮尘": "fuchen",
    "沙尘暴": "shachenbao",
    "无数据": "wushuju",
}

const week = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "日"}

const Pic = (props) => {
    if (props.name in pics) {
        return <img className={"wpic"} alt="" src={`/weather/${pics[props.name]}.png`}/>;
    } else {
        return <img className={"wpic"} alt="" src={`/weather/wushuju.png`}/>;
    }
}

const fetchData = (city) => {
    return fetch(`${process.env.REACT_APP_WEATHER_API}?city=${city}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            throw new Error(`获取数据失败: ${error.message}`);
        });
}

const Cards = ({data}) => {
    if (!data) {
        return <div></div>
    }
    const d = data.data;
    return (
        <div className={"cards"}>
            {/* eslint-disable-next-line array-callback-return */}
            {Object.keys(d).map(key => {
                if (key === 'casts') {
                    return d[key].map((item, index) => (

                        <Space direction="vertical" size={16} key={index}>
                            <Card className="card" hoverable={true} activeTabKey={"abc"}>
                                <div>
                                    <p className={"middle"}>星期{week[item["week"]]}</p>
                                    <p>{item["date"]}</p>
                                    <p className={"big"}>{item["nighttemp"]}~{item["daytemp"]}°</p>
                                    <p>
                                        <Pic name={item["dayweather"]}/>
                                    </p>
                                    <p>{item["dayweather"]}</p>
                                    <p>{item["daywind"]}风{item["daypower"]}级</p>
                                </div>
                            </Card>
                        </Space>
                    ));
                }
            })}
        </div>
    )
}


export const Search = ({setCity}) => {
    const [options, setOptions] = React.useState([]);
    const onSelect = (data) => {
        setCity(data);
    };
    const onClick = (value, event) => {
        setCity(value);
    }

    const getData = async (data) => {
        try {
            const response = await fetch(`${process.env.REACT_APP_CITY_API}?name=${data}`);
            return await response.json();
        } catch (error) {
            return [];
        }
    };
    const handleSearch = async (data) => {
        if (!data) {
            setOptions([]);
            return;
        }
        const c = await getData(data);
        const cities = c.data;
        if (!Array.isArray(cities)) {
            setOptions([]);
            return;
        }
        const uniqueCities = Array.from(
            new Map(
                cities.map(city => [
                    city[2].includes('区') ? city[1] : city[2],
                    city
                ])
            ).values()
        );

        const formattedOptions = uniqueCities.map((city) => {
            const [province, city_name, district] = city;
            const location = district === city_name ? province : `${province} ${city_name}`;
            const v = district.includes('区') ? city_name : district;
            return {
                label: `${district} (${location})`,
                value: v
            };
        });
        setOptions(formattedOptions);
    };
    return (
        <AutoComplete
            style={{
                width: 320,
            }}
            onSearch={handleSearch}
            options={options}
            onSelect={onSelect}
            status={"error"}
        ><Input.Search onSearch={onClick} size="large" placeholder="input here" enterButton/>
        </AutoComplete>
    );
};

const ShowCity = ({data}) => {
    if (!data) {
        return <div>暂无数据</div>;
    }
    const d = data.data
    return <div className={"show-city"}>
        <div className={"big"}>{d["city"]}</div>
        <div>更新时间 {d["reporttime"].split(" ")[1]}</div>
    </div>
}


export const Content = () => {
    const [displayData, setDisplayData] = useState(null);
    const [city, setCity] = useState("广州");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async (city) => {
        try {
            setLoading(true);
            setError(null);
            const result = await fetchData(city);
            setDisplayData(result);
        } catch (err) {
            setError("暂时找不到数据");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        handleSearch(city);
    }, [city]);

    return (
        <div className="content">
            <Search setCity={setCity}/>
            <div className="spacer"></div>
            {loading && !displayData && <div>加载中...</div>}
            {error && <div>{error}</div>}
            <div>
                {displayData && <ShowCity className="show-city" data={displayData}/>}
                {displayData && <Cards className="cards" data={displayData}/>}
            </div>
        </div>
    );
};
export default Content;