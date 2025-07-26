import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';

// Theme type definition
type Theme = 'light' | 'dark';

// Theme context interface
interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

// Theme context creation
export const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Theme provider props interface
interface ThemeProviderProps {
  children: ReactNode;
}

// Theme provider component
export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  // Theme state with localStorage initialization
  const [theme, setTheme] = useState<Theme>(() => {
    const storedTheme = localStorage.getItem('theme');
    return (storedTheme === 'light' || storedTheme === 'dark') ? storedTheme : 'light';
  });

  // Effect to update data-theme attribute and localStorage
  useEffect(() => {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  // Theme toggle function
  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  // Context value
  const contextValue: ThemeContextType = {
    theme,
    toggleTheme,
  };

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
};

// Custom hook for theme consumption
export const useTheme = () => {
  const context = useContext(ThemeContext);
  // Error handling for missing provider
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
