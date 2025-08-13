// UserProfile.js - React component with multiple issues
import React, { useState, useEffect } from 'react';
import { getUserData, updateUserData } from '../services/userService';
import { validateEmail } from '../utils/validation';

const UserProfile = ({ userId }) => {
    const [userData, setUserData] = useState({});
    const [loading, setLoading] = useState(true);
    const [errors, setErrors] = useState({});

    // GLARING ISSUE: Infinite re-render loop
    useEffect(() => {
        fetchUserData();
    }); // Missing dependency array

    // SUBTLE ISSUE: No error handling for async operations
    const fetchUserData = async () => {
        const data = await getUserData(userId);
        setUserData(data);
        setLoading(false);
    };

    // GLARING ISSUE: Direct DOM manipulation in React
    const highlightField = (fieldName) => {
        document.getElementById(fieldName).style.backgroundColor = 'yellow';
    };

    // SUBTLE ISSUE: Not properly sanitizing user input
    const handleInputChange = (field, value) => {
        setUserData(prev => ({
            ...prev,
            [field]: value
        }));
        // Clear error when user starts typing
        if (errors[field]) {
            setErrors(prev => ({ ...prev, [field]: null }));
        }
    };

    // GLARING ISSUE: XSS vulnerability - dangerouslySetInnerHTML with user data
    const renderBio = () => {
        return (
            <div 
                dangerouslySetInnerHTML={{ __html: userData.bio }}
            />
        );
    };

    // SUBTLE ISSUE: Inefficient array operations in render
    const renderInterests = () => {
        return userData.interests?.map((interest, index) => {
            // PERFORMANCE ISSUE: Creating new objects in render
            const style = {
                padding: '5px',
                margin: '2px',
                backgroundColor: '#f0f0f0'
            };
            return (
                <span key={index} style={style}>
                    {interest}
                </span>
            );
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // SUBTLE ISSUE: Validation logic mixed with component logic
        const emailValid = validateEmail(userData.email);
        if (!emailValid) {
            setErrors({ email: 'Invalid email format' });
            return;
        }

        // GLARING ISSUE: No CSRF protection
        try {
            await updateUserData(userData);
            alert('Profile updated successfully!'); // SUBTLE ISSUE: Using alert instead of proper UI feedback
        } catch (error) {
            // SUBTLE ISSUE: Exposing error details to user
            alert('Error: ' + error.message);
        }
    };

    if (loading) {
        // PERFORMANCE ISSUE: Inline styles causing re-renders
        return <div style={{textAlign: 'center', padding: '20px'}}>Loading...</div>;
    }

    return (
        <div className="user-profile">
            <h2>User Profile</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="name">Name:</label>
                    <input
                        id="name"
                        type="text"
                        value={userData.name || ''}
                        onChange={(e) => handleInputChange('name', e.target.value)}
                        onClick={() => highlightField('name')}
                    />
                    {errors.name && <span className="error">{errors.name}</span>}
                </div>

                <div>
                    <label htmlFor="email">Email:</label>
                    <input
                        id="email"
                        type="email"
                        value={userData.email || ''}
                        onChange={(e) => handleInputChange('email', e.target.value)}
                    />
                    {errors.email && <span className="error">{errors.email}</span>}
                </div>

                <div>
                    <label htmlFor="bio">Bio:</label>
                    <textarea
                        id="bio"
                        value={userData.bio || ''}
                        onChange={(e) => handleInputChange('bio', e.target.value)}
                        rows="4"
                    />
                </div>

                <div>
                    <h3>Interests:</h3>
                    {renderInterests()}
                </div>

                <div>
                    <h3>Bio Preview:</h3>
                    {renderBio()}
                </div>

                <button type="submit">Update Profile</button>
            </form>
        </div>
    );
};

export default UserProfile;
