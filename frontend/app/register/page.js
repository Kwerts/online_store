"use client";


import axios from 'axios';
import { useState } from 'react';
import Link from 'next/link';


export default function Home() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState(''); // Для отображения ошибок
    const [success, setSuccess] = useState(''); // Для отображения успеха

    const SubmitForm = async (event) => {
        event.preventDefault(); // Предотвращаем стандартное поведение формы
        setError(''); // Сброс ошибок перед новой попыткой
        setSuccess(''); // Сброс успеха перед новой попыткой

        try {
            const response = await axios.post('http://127.0.0.1:8000/user/register', {
                username: username,
                email: email,
                password: password
            });
            setSuccess('Регистрация прошла успешно!'); // Отображаем сообщение об успехе
            console.log(response.data); // Выводим ответ от сервера
        } catch (err) {
            if (err.response.status === 400) {
                setError('Такой логин уже занят.');
            }
            else {
                setError('Ошибка при входе!'); // Обработка ошибок
                console.error(err);
            }
        }
    };

    return (
        <>
            <Link href='/'>
                <button>Fakee shop</button>
            </Link>
            <h1>Зарегестрироваться в Fakee shop</h1>
            {error && <p>{error}</p>}
            {success && <p>{success}</p>}
            <form onSubmit={SubmitForm}>
                <label htmlFor="username">Логин:</label>
                <input
                    type="text"
                    id="username"
                    className='input-username'
                    onChange={(e) => setUsername(e.target.value)} // Изменено на "text" вместо "email"
                    required
                />

                <label htmlFor="password">Пароль:</label>
                <input
                    type="password"
                    id="password"
                    className='input-password'
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <label htmlFor="email">Почта:</label>
                <input
                    type="email"
                    id="email"
                    className='input-email'
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <button type="submit">Отправить</button>
            </form>
        </>
    );
}