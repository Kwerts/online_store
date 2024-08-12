"use client";


import axios from 'axios';
import { useState } from 'react';
import Link from 'next/link';


export default function Home() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const SubmitForm = async (event) => {
        event.preventDefault();
        setError('');
        setSuccess('');
        console.log({
            username: username,
            password: password
        })
        try {
            const response = await axios.post('http://127.0.0.1:8000/user/login', new URLSearchParams({
                username: username,
                password: password,
            }), {
                withCredentials: true
            });
            setSuccess('Успешный вход!');
            console.log(response.data);
        } catch (err) {
            if (err.response.status === 400) {
                setError('Пароль не подходит или пользователь с таким логином не найден.');
            }
            else {
                setError('Ошибка при входе!');
                console.error(err);
            }
        }
    };

    return (
        <>
            <Link href='/'>
                <button>Fakee shop</button>
            </Link>
            <h1>Войти в Fakee shop</h1>
            {error && <p>{error}</p>}
            {success && <p>{success}</p>}
            <form onSubmit={SubmitForm}>
                <label htmlFor="username">Логин:</label>
                <input
                    type="text"
                    id="username"
                    className='input-username'
                    onChange={(e) => setUsername(e.target.value)}
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

                <button type="submit">Отправить</button>
            </form>
        </>
    );
}