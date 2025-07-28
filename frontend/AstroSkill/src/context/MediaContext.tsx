import { createContext, useContext, useState, type ReactNode } from 'react';

// Media context interface
interface MediaContextType {
  isPlaying: boolean;
  currentTrack: string | null;
  playPause: () => void;
  setTrack: (trackName: string) => void;
  // Add other media-related global states or functions here
  // Example: volume: number;
  // Example: setVolume: (vol: number) => void;
}

// Media context creation
export const MediaContext = createContext<MediaContextType | undefined>(undefined);

// Media provider props interface
interface MediaProviderProps {
  children: ReactNode;
}

// Media provider component
export const MediaProvider: React.FC<MediaProviderProps> = ({ children }) => {
  // State for playback status
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  // State for current track
  const [currentTrack, setCurrentTrack] = useState<string | null>(null);
  // Example state: const [volume, setVolume] = useState<number>(0.5);

  // Play/Pause toggle function
  const playPause = () => {
    setIsPlaying((prev) => !prev);
  };

  // Set track function
  const setTrack = (trackName: string) => {
    setCurrentTrack(trackName);
    setIsPlaying(true); // Automatically play when new track is set
  };

  // Context value
  const contextValue: MediaContextType = {
    isPlaying,
    currentTrack,
    playPause,
    setTrack,
    // volume,
    // setVolume,
  };

  return (
    <MediaContext.Provider value={contextValue}>
 {children}
    </MediaContext.Provider>
  );
};

// Custom hook for media context consumption
export const useMedia = () => {
  const context = useContext(MediaContext);
  // Error handling for missing provider
  if (context === undefined) {
    throw new Error('useMedia must be used within a MediaProvider');
  }
  return context;
};
