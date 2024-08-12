"use client";

import Link from 'next/link';
import { useState, useEffect } from 'react';
import axios from 'axios';


const Sellers = ({ params }) => {
    const { name } = params;

    const [products, setProducts] = useState([])

    useEffect(() => {
        const GetAllUserProducts = async () => {
            try {
                const response = await axios.post('http://127.0.0.1:8000/products/user/' + name);
                setProducts(response.data);
            } catch (error) {
                console.error('Ошибка при получении продуктов:', error);
            }
        };

        GetAllUserProducts();
    }, [name]);

    return (
        <>
            <Link href='/'>
                <button>Fakee shop</button>
            </Link>
            <h1>Продавец: {name}</h1>
            <Link href='/products/create'>
                <button>Создать товар</button>
            </Link>
            <Link href='/products'>
                <button>Все товары</button>
            </Link>
            <Link href='/products/my'>
                <button>Мои товары</button>
            </Link>
            <ul>
                {products.map((product) => (
                    <li key={product.id}>
                        <h1>{product.name} ({product.category_name}), {product.price}$</h1>
                        <p>{product.description}</p>
                    </li>
                ))}
            </ul>
        </>
    );
};

export default Sellers;
