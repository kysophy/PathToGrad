import { createContext, useState, useContext, ReactNode } from 'react';

export interface UserData {
  id: string;
  name: string;
  role: 'Student' | 'Advisor' | 'Admin';
}

// Define the shape of your auth state
interface AuthState {
  isAuthenticated: boolean;
  role: 'Student' | 'Advisor' | 'Admin' | null;
  user: UserData | null;
}

interface AuthContextType extends AuthState {
  login: (userData: UserData) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [auth, setAuth] = useState<AuthState>({
    isAuthenticated: false,
    role: null,
    user: null,
  });

  const login = (userData: UserData) => {
    setAuth({ 
      isAuthenticated: true, 
      role: userData.role, 
      user: userData 
    });
  };

  const logout = () => {
    setAuth({ isAuthenticated: false, role: null, user: null });
  };

  return (
    <AuthContext.Provider value={{ ...auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
};