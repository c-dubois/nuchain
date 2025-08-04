import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { RegisterData } from '../../types/auth';
import './AuthForms.css';

interface RegisterFormProps {
    onSuccess: () => void;
    onSwitchToLogin: () => void;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({ onSuccess, onSwitchToLogin }) => {
    const [formData, setFormData] = useState<RegisterData>({
        username: '',
        email: '',
        password: '',
        password_confirm: '',
        first_name: '',
        last_name: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { register } = useAuth();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
        ...formData,
        [e.target.name]: e.target.value,
        });
    };
};