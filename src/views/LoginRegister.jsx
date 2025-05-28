import React, { useState, useContext } from 'react'
import { Context } from '../js/store/appContext.jsx';

const LoginRegister = () => {

    const { store, actions } = useContext(Context)

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: ''
      });

    const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    };

    const handleRegister = () => {
        const { name, email, password } = formData;
        actions.register(name, email, password);
      }; 

    return (
    <div>
        <h2>Register</h2>
        <h3>Test store: {store.personas}</h3>
        {store.registerStatus && <h4>Registro Exitoso</h4>}
        <form>
        <div>
            <label htmlFor="name">Nombre:</label>
            <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            />
        </div>
        <div>
            <label htmlFor="email">Email:</label>
            <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            />
        </div>
        <div>
            <label htmlFor="password">Contraseña:</label>
            <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            />
        </div>
        </form>
        <button onClick={handleRegister}>Register</button>
    </div>
    );
};

export default LoginRegister;