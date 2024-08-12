"use client";


import axios from 'axios';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation'
import Link from 'next/link';


export default function Home() {
    const router = useRouter();
    const [products, setProducts] = useState([]); // Изменил имя состояния на множественное

    // Используйте useEffect для загрузки данных при монтировании компонента
    useEffect(() => {
        const Redirection = async () => {
            try {
                const response = await axios.post('http://127.0.0.1:8000/user/check/auth', {}, {
                    withCredentials: true
                });
                console.log(response.data);
            } catch (error) {
                console.error('Пользователь не авторизован, произойдёт перенаправление');
                router.push('/login'); // Замените '/login' на нужный путь
            }
        };

        const GetAllProducts = async () => {
            try {
                const response = await axios.post('http://127.0.0.1:8000/products/my', {}, {
                    withCredentials: true
                });
                setProducts(response.data);
                console.log(response.data);
            } catch (error) {
                console.error('Ошибка при получении продуктов:', error);
            }
        };

        Redirection()
        GetAllProducts();
    }, [router]);


    const DeleteProduct = async (product_id) => {
        const response = await axios.delete('http://127.0.0.1:8000/products/delete/' + product_id)

        setProducts(prevProducts => prevProducts.filter(product => product.id !== product_id));
        console.log(response.data);
    }

    return (
        <>
            <Link href='/'>
                <button>Fakee shop</button>
            </Link>
            <h1>Ваши товары</h1>
            <Link href='/products/create'>
                <button>Создать товар</button>
            </Link>
            <Link href='/products'>
                <button>Все товары</button>
            </Link>
            <ul>
                {products.map((product) => ( // Итерируем по массиву продуктов
                    <li key={product.id}>
                        <h1>{product.name} ({product.category_name}), {product.price}$ <button onClick={() => DeleteProduct(product.id)}>Удалить товар</button></h1>
                        <p>{product.description}</p>
                    </li> // Предполагается, что у продукта есть уникальный id и name
                ))}
            </ul>
        </>
    );
}