import { SunIcon, MoonIcon, ArrowRightOnRectangleIcon } from '@heroicons/react/24/outline'
import { Sparkles } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { API_BASE_URL } from '../../config'

export const Header = () => {
  const [dark, setDark] = useState(false)

  const toggleTheme = () => {
    setDark(!dark)
    document.documentElement.classList.toggle('dark', !dark)
  }

  const handleLogout = async () => {
    try {
      await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        credentials: 'include'
      })
      window.location.reload()
    } catch (error) {
      console.error('Logout failed:', error)
      window.location.reload()
    }
  }

  return (
    <header className="glass-effect mx-4 mt-4 px-6 py-4 rounded-2xl shadow-xl backdrop-blur-md">
      <div className="flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 group">
          <Sparkles className="w-7 h-7 text-purple-600 dark:text-purple-400 group-hover:rotate-12 transition-transform duration-300" />
          <span className="text-2xl font-extrabold gradient-text tracking-tight">
            StaySoft
          </span>
        </Link>

        <div className="flex items-center gap-3">
          {/* Footer Links */}
          <div className="hidden md:flex space-x-4 text-sm text-gray-600 dark:text-gray-400 mr-2">
            <a href="/privacy-policy" className="hover:text-purple-600 dark:hover:text-purple-400 transition-colors font-medium">
              Privacy Policy
            </a>
            <a href="/terms" className="hover:text-purple-600 dark:hover:text-purple-400 transition-colors font-medium">
              Terms of Service
            </a>
          </div>

          <button
            aria-label="Toggle theme"
            onClick={toggleTheme}
            className="p-2.5 rounded-xl glass-effect hover:bg-white/20 dark:hover:bg-white/10 transition-all shadow-lg"
          >
            {dark ? (
              <SunIcon className="w-5 h-5 text-yellow-400" />
            ) : (
              <MoonIcon className="w-5 h-5 text-purple-600" />
            )}
          </button>

          <button
            aria-label="Logout"
            onClick={handleLogout}
            className="p-2.5 rounded-xl bg-gradient-to-r from-red-500/20 to-pink-500/20 hover:from-red-500/30 hover:to-pink-500/30 transition-all shadow-lg text-red-600 dark:text-red-400 hover:scale-105"
          >
            <ArrowRightOnRectangleIcon className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  )
}
