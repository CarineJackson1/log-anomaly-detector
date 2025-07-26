import { createContext, useContext, useState, type ReactNode } from 'react';

// Button context interface
interface ButtonContextType {
  lastClickedButtonId: string | null;
  setLastClickedButtonId: (id: string) => void;
  // Add other button-related global states or functions here
  // Example: isProcessing: boolean;
  // Example: setProcessing: (status: boolean) => void;
}

// Button context creation
export const ButtonContext = createContext<ButtonContextType | undefined>(undefined);

// Button provider props interface
interface ButtonProviderProps {
  children: ReactNode;
}

// Button provider component
export const ButtonProvider: React.FC<ButtonProviderProps> = ({ children }) => {
  // State for last clicked button ID
  const [lastClickedButtonId, setLastClickedButtonId] = useState<string | null>(null);
  // Example state: const [isProcessing, setProcessing] = useState<boolean>(false);

  // Context value
  const contextValue: ButtonContextType = {
    lastClickedButtonId,
    setLastClickedButtonId,
    // isProcessing,
    // setProcessing,
  };

  return (
    <ButtonContext.Provider value={contextValue}>
      {children}
    </ButtonContext.Provider>
  );
};

// Custom hook for button context consumption
export const useButton = () => {
  const context = useContext(ButtonContext);
  // Error handling for missing provider
  if (context === undefined) {
    throw new Error('useButton must be used within a ButtonProvider');
  }
  return context;
};
