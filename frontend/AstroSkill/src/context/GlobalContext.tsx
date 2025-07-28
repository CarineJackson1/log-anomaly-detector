import { type ReactNode } from 'react';
import { ThemeProvider } from './ThemeContext'; 
import { ButtonProvider } from './Buttons/ButtonContext';
import { MediaProvider } from './MediaContext';  
// Import other providers as you create them, e.g.,
// import { AuthProvider } from './AuthContext';

// Global context provider props interface
interface GlobalContextProviderProps {
  children: ReactNode;
}

// Global context provider component
export const GlobalContextProvider: React.FC<GlobalContextProviderProps> = ({ children }) => {
  return (
    // Nest all your providers here.
    // The order might matter if one context depends on another.
    // Generally, more fundamental or independent contexts go higher up.
    <ThemeProvider>
      <ButtonProvider>
        <MediaProvider>
          {/* Add other providers here */}
          {children}
        </MediaProvider>
      </ButtonProvider>
    </ThemeProvider>
  );
};
