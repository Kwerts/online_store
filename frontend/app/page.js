"use client";


import Link from 'next/link';


export default function Home() {
  return (
    <>
        <h1>Fakee shop</h1>
        <Link href='/register'>
            <button>Зарегестрироваться в Fakee shop</button>
        </Link>
        <Link href='/login'>
            <button>Войти в Fakee shop</button>
        </Link>
        <p>
            <Link href='/products/'>
                <button>Все товары</button>
            </Link>
        </p>
    </>
  );
}