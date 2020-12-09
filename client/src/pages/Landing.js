import React, { useState, useEffect, Fragment } from 'react';
import { Tag, Input, Col, Row, Pagination, List, notification, Select } from 'antd';
import { motion } from "framer-motion";
import Axios from 'axios';
import { CloseOutlined, CheckOutlined, CloseCircleOutlined } from '@ant-design/icons';


const { location: { hostname } } = window;

const getWindowDimensions = () => window.innerHeight;

export default function Landing(props) {
    const [page, setPage] = useState(props.match.params.page);
    const { Search } = Input;
    const { Option } = Select;
    const [height, setHeight] = useState(getWindowDimensions());
    const [xValue, setXValue] = useState(height * 50 / 100);
    const [data, setData] = useState({ data: [] });
    const [query, setQuery] = useState(props.match.params.query);
    const [searchValue, setSearchValue] = useState('');
    const [irrelevantList, setIrrelevantList] = useState([]);
    const [prevQuery, setPrevQuery] = useState('');
    const [cluster, setCluster] = useState(props.match.params.cluster);

    async function getQuery(value, page) {
        if (value) {
            try {
                let query = `http://${hostname}/api/search?q=${value}&page=${page}&cluster=${cluster}`;
                let { data } = await Axios.get(query);
                setData(data);
                setPrevQuery(value);
                if (!(Array.isArray(data.data) && data.data.length)) {
                    notification.error({
                        message: 'Query Error',
                        description:
                            'Hasil tidak ada',
                        duration: 3,
                    });
                }
            }
            catch (e) {
                notification.error({
                    message: 'Query Error',
                    description:
                        'Kesalahan Penulisan Query',
                    duration: 3,
                });
            }
        }


    }

    const getScores = (dataCount, irrelevantCount) => {
        const relevant = (dataCount - irrelevantCount);
        const precision = relevant / dataCount;
        const recall = relevant / relevant;

        return [
            { 'title': 'Relevan', 'value': relevant },
            { 'title': 'Tidak Relevan', 'value': irrelevantCount },
            { 'title': 'Precision', 'value': precision },
            { 'title': 'Recall', 'value': recall },
            { 'title': 'F1 Score', 'value': (2 * precision * recall) / (precision + recall) },
        ];
    };

    useEffect(() => {
        function handleResize() {
            setHeight(getWindowDimensions());
        }
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    useEffect(() => {
        if (!props.match.params.page) {
            setPage(1);
        }
        setSearchValue(props.match.params.query);
        getQuery(query, page);
    }, [query, page, cluster])

    useEffect(() => {
        if (data.data.length) {
            setXValue(height * 1.5 / 100);
        }
    }, [data]);

    const toggleRelevant = (slug) => {
        if (irrelevantList.indexOf(slug) === -1) {
            setIrrelevantList([...irrelevantList, slug]);
        } else {
            setIrrelevantList(irrelevantList.filter(item => item !== slug));
        }
    };

    return (
        <div style={{ padding: 16 }}>
            <motion.div
                style={{ flex: 1, width: '100%' }}
                animate={{
                    y: xValue,
                    scale: 1,
                }}
                transition={{ type: 'spring', stiffness: 50 }}>
                <Row gutter={24}>
                    <Col xs={2} sm={4} md={6} lg={8} />
                    <Col xs={20} sm={16} md={12} lg={8}>
                        <Input.Group compact>
                            <Select
                                defaultValue="Cluster"
                                style={{ width: '100%' }}
                                onChange={value => {
                                    setCluster(value);
                                    setQuery(query);
                                }}>
                                <Option value='0'>Semua Cluster</Option>
                                <Option value='1'>Cluster 1</Option>
                                <Option value='2'>Cluster 2</Option>
                                <Option value='3'>Cluster 3</Option>
                                <Option value='4'>Cluster 4</Option>
                                <Option value='5'>Cluster 5</Option>
                                <Option value='6'>Cluster 6</Option>
                                <Option value='7'>Cluster 7</Option>
                            </Select>
                            <Search
                                placeholder="Cari ayat di sini..."
                                enterButton="Search"
                                style={{ color: 'black' }}
                                size="large"
                                value={searchValue}
                                onChange={value => {
                                    setSearchValue(value.target.value);
                                    setQuery(query);
                                }}
                                onSearch={value => {
                                    setCluster(cluster);
                                    setQuery(value);
                                    if (value) {
                                        if (value !== prevQuery) {
                                            setIrrelevantList([]);
                                            props.history.push(`/${value}/${1}/${cluster}`)
                                        }
                                        props.history.push(`/${value}/${page}/${cluster}`)
                                    }
                                    else {
                                        props.history.push('/');
                                        setXValue(height * 50 / 100);
                                    }
                                }}
                                autoFocus
                            />
                        </Input.Group>

                    </Col>
                    <Col xs={2} sm={4} md={6} lg={8} />
                </Row>
            </motion.div>
            {(data.data.length && query) ?
                <div style={{ display: 'flex', marginTop: '2vw' }}>
                    <Row style={{ flex: 1 }}>
                        <Col xs={2} sm={4} md={6} lg={4} ></Col>
                        <Col xs={20} sm={16} md={12} lg={16}>
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                flexDirection: 'column'
                            }}>
                                <h4 style={{ width: '100%' }}>Didapat {data.meta.total} hasil - {data.execution_time.toFixed(3)} detik</h4>
                                <List
                                    itemLayout="horizontal"
                                    style={{ color: 'black' }}
                                    dataSource={data.data}
                                    renderItem={(item, index) => {
                                        const { slug } = item;
                                        const isIrrelevant = irrelevantList.indexOf(slug) !== -1;
                                        return (
                                            <List.Item key={index}>
                                                <List.Item.Meta
                                                    title={<a>{item.slug}</a>}
                                                    description={<Row gutter={24}>
                                                        <Col sm={16} md={12}><p style={{ textAlign: 'justify' }}>{item.tafsir}</p></Col>
                                                        <Col sm={4} md={4}><p style={{ textAlign: 'center' }}>{(item.cosine).toFixed(4)}</p></Col>
                                                        <Col sm={4} md={4}><p style={{ textAlign: 'center' }}>{(item.cluster)}</p></Col>
                                                        <Col sm={4} md={4}>
                                                            <div style={{ textAlign: 'center' }}>
                                                                {isIrrelevant && (<Tag icon={<CloseCircleOutlined style={{ color: 'red' }} />} color="error">
                                                                    Tidak Relevan
                                                                </Tag>)}
                                                                <a onClick={() => toggleRelevant(slug)}>
                                                                    <h5>Tandai {isIrrelevant ? 'Sebagai' : 'Tidak'} Relevan</h5>
                                                                    {isIrrelevant ? <CheckOutlined style={{ color: 'blue' }} /> : <CloseOutlined style={{ color: 'red' }} />}
                                                                </a>
                                                            </div>
                                                        </Col>
                                                    </Row>}
                                                />
                                            </List.Item>
                                        )
                                    }}
                                />
                                <Row style={{ display: 'flex', width: '100%' }}>
                                    {getScores(data.meta.total, irrelevantList.length).map((score, index) => (
                                        <Col key={index} flex={1} style={{ textAlign: 'center' }}>
                                            <h4>{score.title}</h4>
                                            <h4>{score.value}</h4>
                                        </Col>
                                    ))}
                                </Row>
                                <Pagination {...data.meta} defaultCurrent={page} showSizeChanger={false} onChange={(page) => {
                                    setPage(page);
                                    document.body.scrollTop = 0;
                                    document.documentElement.scrollTop = 0;
                                    props.history.push(`/${query}/${page}/${cluster}`)
                                }} />
                            </div>
                        </Col>
                        <Col xs={2} sm={4} md={6} lg={4} ></Col>
                    </Row>
                </div> : <Fragment />}
        </div>
    )
}
