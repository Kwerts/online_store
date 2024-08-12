"use client";


import axios from 'axios';
import { useState, useEffect } from 'react';
import Link from 'next/link';


export default function Home() {
    const [products, setProducts] = useState([]); // Изменил имя состояния на множественное

    // Используйте useEffect для загрузки данных при монтировании компонента
    useEffect(() => {
        const GetAllProducts = async () => {
            try {
                const response = await axios.get('/api/products');
                setProducts(response.data);
                console.log(response.data);
            } catch (error) {
                console.error('Ошибка при получении продуктов:', error);
            }
        };

        GetAllProducts();
    }, []);

    return (
        <>
            <Link href='/'>
                <button>Fakee shop</button>
            </Link>
            <h1>Все товары</h1>
            <Link href='/products/create'>
                <button>Создать товар</button>
            </Link>
            <Link href='/products/my'>
                <button>Мои товары</button>
            </Link>
            <ul>
                {products.map((product) => ( // Итерируем по массиву продуктов
                    <li key={product.id}>
                        <h1>{product.name} ({product.category_name}), {product.price}$</h1>
                        <p>{product.description}</p>
                        <Link href={'/sellers/' + product.added_by_user_username}>
                            <button>Продавец</button>
                        </Link>
                    </li> // Предполагается, что у продукта есть уникальный id и name
                ))}
            </ul>
        </>
    );
}