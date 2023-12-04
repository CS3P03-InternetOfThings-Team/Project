import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme, StyledEngineProvider } from '@mui/material';
import { themeCreator } from './base';

export const ThemeContext = React.createContext((themeName: string): void => {});

type ThemeProviderWrapperProps = {
  children: React.ReactNode;
}

const ThemeProviderWrapper: React.FC<ThemeProviderWrapperProps> = (props) => {
  const [themeName, setThemeName] = useState('NebulaFighterTheme');
  const theme = themeCreator(themeName);

  useEffect(() => {
    const curThemeName = localStorage.getItem('appTheme');
    if (curThemeName) {
      setThemeName(curThemeName);
    }
  }, []);

  const updateThemeName = (newThemeName: string): void => {
    setThemeName(newThemeName);
    localStorage.setItem('appTheme', newThemeName);
  };

  return (
    <StyledEngineProvider injectFirst>
      <ThemeContext.Provider value={updateThemeName}>
        <ThemeProvider theme={createTheme(theme)}>
          {props.children}
        </ThemeProvider>
      </ThemeContext.Provider>
    </StyledEngineProvider>
  );
};

export default ThemeProviderWrapper;
