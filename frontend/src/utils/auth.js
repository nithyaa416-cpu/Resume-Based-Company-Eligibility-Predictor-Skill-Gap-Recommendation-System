// Authentication utility functions

export const getRegisteredUsers = () => {
  try {
    return JSON.parse(localStorage.getItem('registeredUsers') || '[]');
  } catch (error) {
    console.error('Error parsing registered users:', error);
    return [];
  }
};

export const saveRegisteredUser = (userData) => {
  try {
    const users = getRegisteredUsers();
    users.push(userData);
    localStorage.setItem('registeredUsers', JSON.stringify(users));
    return true;
  } catch (error) {
    console.error('Error saving user:', error);
    return false;
  }
};

export const findUserByEmail = (email) => {
  const users = getRegisteredUsers();
  return users.find(user => user.email === email);
};

export const authenticateUser = (email, password) => {
  // Check registered users
  const user = findUserByEmail(email);
  if (user && user.password === password) {
    return {
      success: true,
      user: {
        email: user.email,
        name: user.name,
        jobTitle: user.jobTitle,
        experience: user.experience,
        token: user.token
      }
    };
  }
  
  // Check demo credentials
  if (email === 'demo@example.com' && password === 'password') {
    return {
      success: true,
      user: {
        email: email,
        name: 'Demo User',
        jobTitle: 'Software Engineer',
        experience: 'mid',
        token: 'mock-jwt-token'
      }
    };
  }
  
  return {
    success: false,
    error: 'Invalid email or password'
  };
};

export const getCurrentUser = () => {
  try {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  } catch (error) {
    console.error('Error parsing user data:', error);
    return null;
  }
};

export const setCurrentUser = (userData) => {
  try {
    localStorage.setItem('user', JSON.stringify(userData));
    return true;
  } catch (error) {
    console.error('Error saving user session:', error);
    return false;
  }
};

export const clearCurrentUser = () => {
  try {
    localStorage.removeItem('user');
    return true;
  } catch (error) {
    console.error('Error clearing user session:', error);
    return false;
  }
};

export const isEmailTaken = (email) => {
  const user = findUserByEmail(email);
  return !!user;
};