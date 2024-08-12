"use client";


import axios from 'axios';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation'
import Link from 'next/link';


export default function Home() {
    const router = useRouter();
    const [name, setName] = useState('');
    const [category, setCategory] = useState('')
    const [price, setPrice] = useState('');
    const [description, setDescription] = useState('');
    const [status, setStatus] = useState(null)
    const [categories, setCategories] = useState([])

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
        const SetCategories = async () => {
            const response = await axios.get('http://127.0.0.1:8000/products/categories/all')

            setCategories(response.data)
        }

        Redirection();
        SetCategories()
    }, [router]); // Пустой массив зависимостей означает, что хук выполнится только один раз при монтировании

    const SubmitForm = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/products/add', {
                name: name,
                description: description,
                price: price,
                category_name: category,
            }, {
                withCredentials: true
            });
            setName('')
            setCategory('')
            setDescription('')
            setPrice('')
            setStatus('Успешно создано!')
            console.log(response.data);
        } catch (err) {
                console.error(err);
            }
        }

    return (
        <>
            <Link href='/'>
                <button>Fakee shop</button>
            </Link>
            <h1>Создать товар</h1>
            {status && <p>{status}</p>}
            <Link href='/products'>
                <button>Все товары</button>
            </Link>
            <form onSubmit={SubmitForm}>
                <p>
                    <label htmlFor="username">Название товара:</label>
                    <input
                        type="text"
                        className='input-name'
                        onChange={(e) => setName(e.target.value)}
                        value={name}
                        required
                    />
                </p>

                <p>
                    <label htmlFor="username">Категория:</label>
                    <select value={category} onChange={(e) => setCategory(e.target.value)}>
                        <option value="" disabled>Выберите...</option>
                        {categories.map((category) => ( // Итерируем по массиву продуктов
                            <option key={category.id}>
                                <option>{category.name}</option>
                            </option>
                        ))}
                    </select>
                </p>

                <p>
                    <label htmlFor="password">Цена:</label>
                    <input
                        type="number"
                        className='input-price'
                        onChange={(e) => setPrice(e.target.value)}
                        min={1}
                        step={1}
                        required
                        value={price}
                    />
                </p>

                <p>
                    <label htmlFor="password">Описание:</label>
                    <input
                        type="text"
                        className='input-description'
                        onChange={(e) => setDescription(e.target.value)}
                        value={description}
                        required
                    />
                </p>

                <p>
                    <button type="submit">Создать</button>
                </p>
            </form>
        </>
    )
}