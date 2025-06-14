import React, { useEffect, useState } from 'react';

function App() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/products')
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch(console.error);
  }, []);

  return (
    <div>
      <h1>Store Products</h1>
      <ul>
        {products.map((p) => (
          <li key={p.name}>
            <strong>{p.name}</strong> - {p.model} - ${'{'}p.price{'}'}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
