
import { createContext, useState, useEffect } from "react"

export const ThemeContext = createContext()

export function ThemeProvider({ children }) {
  const [darkMode, setDarkMode] = useState(false)

  // Initialize theme from localStorage if available
  useEffect(() => {
    const savedTheme = localStorage.getItem("quicktrip_theme")
    if (savedTheme) {
      setDarkMode(savedTheme === "dark")
    } else {
      // Check if user prefers dark mode
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches
      setDarkMode(prefersDark)
    }
  }, [])

  // Apply theme to document when it changes
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark-mode")
    } else {
      document.documentElement.classList.remove("dark-mode")
    }
    localStorage.setItem("quicktrip_theme", darkMode ? "dark" : "light")
  }, [darkMode])

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
  }

  return <ThemeContext.Provider value={{ darkMode, toggleDarkMode }}>{children}</ThemeContext.Provider>
}

