import { useIsLoggedIn } from './hooks/useIsLoggedIn'
import { API_BASE_URL } from './config'

import { Header } from './components/layout/Header'
import { PlaylistTransfer } from './components/features/PlaylistTransfer'
import { SpotifyToYouTubeTransfer } from './components/features/SpotifyToYouTubeTransfer'

import { AmazonToSpotifyTransfer } from './components/features/AmazonToSpotifyTransfer'
import { PrivacyPolicy } from './components/pages/PrivacyPolicy'
import { TermsOfService } from './components/pages/TermsOfService'
import { motion } from 'framer-motion'
import { Music2, Youtube, ArrowRightLeft, Sparkles } from 'lucide-react'
import { useEffect, useState, useLayoutEffect } from 'react'
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AmazonMusicIcon } from './components/ui/Icons'

// --- Components ---

interface ServiceAppButtonProps {
  icon: React.ElementType
  label: string
  onClick: () => void
  loading?: boolean
  gradient: string
  iconColor?: string
}

function ServiceAppButton({ icon: Icon, label, onClick, loading, gradient, iconColor = "text-white" }: ServiceAppButtonProps) {
  return (
    <motion.button
      whileHover={{ scale: 1.05, y: -5 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      disabled={loading}
      className={`
        relative group flex flex-col items-center justify-center
        w-32 h-32 sm:w-40 sm:h-40 rounded-[2rem]
        ${gradient} shadow-xl hover:shadow-2xl
        transition-all duration-300
        disabled:opacity-70 disabled:cursor-not-allowed
      `}
    >
      <div className="absolute inset-0 rounded-[2rem] bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity" />

      {loading ? (
        <div className="w-10 h-10 border-4 border-white/30 border-t-white rounded-full animate-spin" />
      ) : (
        <Icon className={`w-14 h-14 sm:w-16 sm:h-16 ${iconColor} drop-shadow-lg`} />
      )}

      <span className="mt-3 text-white font-bold text-sm sm:text-base tracking-wide drop-shadow-md">
        {loading ? '...' : label}
      </span>
    </motion.button>
  )
}

function LoginPage() {
  const [dark, setDark] = useState(true)
  const [isRetrying, setIsRetrying] = useState(false)

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
  }, [dark])

  const handleLogin = (provider: string) => {
    setIsRetrying(true)
    window.location.href = `${API_BASE_URL}/${provider}/login?redirect=true`;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 via-gray-200 to-gray-300 dark:from-gray-950 dark:via-gray-900 dark:to-black flex flex-col items-center justify-center p-4 relative overflow-hidden font-sans">
      {/* Background Blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-500/20 rounded-full blur-[100px] animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-blue-500/20 rounded-full blur-[100px] animate-pulse" style={{ animationDelay: '2s' }} />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        className="text-center space-y-10 max-w-4xl relative z-10"
      >
        <div className="space-y-4">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="inline-flex items-center justify-center p-4 bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 shadow-2xl mb-4"
          >
            <Sparkles className="w-10 h-10 text-yellow-400 mr-3" />
            <h1 className="text-4xl md:text-6xl font-black bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400 tracking-tight">
              StaySoft
            </h1>
          </motion.div>

          <p className="text-lg md:text-xl text-gray-600 dark:text-gray-400 font-medium max-w-xl mx-auto leading-relaxed">
            Sua música, em qualquer lugar. Conecte suas contas para transferir playlists.
          </p>
        </div>

        <motion.div
          className="flex flex-wrap justify-center gap-6 md:gap-8"
          initial="hidden"
          animate="visible"
          variants={{
            hidden: { opacity: 0 },
            visible: {
              opacity: 1,
              transition: {
                staggerChildren: 0.1
              }
            }
          }}
        >
          <motion.div variants={{ hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } }}>
            <ServiceAppButton
              icon={Music2}
              label="Spotify"
              onClick={() => handleLogin('spotify')}
              gradient="bg-gradient-to-br from-[#1DB954] to-[#191414]"
              loading={isRetrying}
            />
          </motion.div>

          <motion.div variants={{ hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } }}>
            <ServiceAppButton
              icon={Youtube}
              label="YouTube"
              onClick={() => handleLogin('youtube')}
              gradient="bg-gradient-to-br from-[#FF0000] to-[#282828]"
              loading={isRetrying}
            />
          </motion.div>



          <motion.div variants={{ hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } }}>
            <ServiceAppButton
              icon={AmazonMusicIcon}
              label="Amazon"
              onClick={() => handleLogin('amazon')}
              gradient="bg-gradient-to-br from-[#25D1DA] to-[#232F3E]"
              loading={isRetrying}
            />
          </motion.div>
        </motion.div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="flex items-center justify-center gap-6 text-sm text-gray-500 dark:text-gray-500 pt-8"
        >
          <a href="/privacy-policy" className="hover:text-gray-900 dark:hover:text-gray-300 transition-colors">Privacidade</a>
          <a href="/terms" className="hover:text-gray-900 dark:hover:text-gray-300 transition-colors">Termos</a>
          <button
            onClick={() => setDark(!dark)}
            className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors"
          >
            {dark ? <SunIcon className="w-5 h-5" /> : <MoonIcon className="w-5 h-5" />}
          </button>
        </motion.div>
      </motion.div>
    </div>
  )
}

type TransferMode = 'youtube-to-spotify' | 'spotify-to-youtube' | 'deezer-to-spotify' | 'spotify-to-deezer' | 'amazon-to-spotify'

function TransferApp({ loginStatus }: { loginStatus: any }) {
  const [transferMode, setTransferMode] = useState<TransferMode>('youtube-to-spotify')
  const [isRetrying, setIsRetrying] = useState(false)

  const handleLogin = (provider: string) => {
    setIsRetrying(true)
    window.location.href = `${API_BASE_URL}/${provider}/login?redirect=true`;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#0a0a0a] relative overflow-hidden">
      <Header />

      <main className="relative z-10 container mx-auto px-4 py-8">

        {/* Mode Selection - App Icon Style */}
        <div className="flex justify-center mb-10 overflow-x-auto py-4 px-2 no-scrollbar">
          <div className="flex gap-4 p-2 bg-white/50 dark:bg-gray-900/50 backdrop-blur-md rounded-[2rem] border border-gray-200 dark:border-gray-800 shadow-lg">
            {[
              { id: 'youtube-to-spotify', from: Youtube, to: Music2, label: 'YT → Spotify', color: 'from-red-500 to-green-500' },
              { id: 'spotify-to-youtube', from: Music2, to: Youtube, label: 'Spotify → YT', color: 'from-green-500 to-red-500' },
              { id: 'amazon-to-spotify', from: AmazonMusicIcon, to: Music2, label: 'Amazon → Spotify', color: 'from-cyan-500 to-green-500' },
            ].map((mode) => (
              <button
                key={mode.id}
                onClick={() => setTransferMode(mode.id as TransferMode)}
                className={`
                  relative group flex flex-col items-center justify-center p-3 rounded-2xl transition-all duration-300 min-w-[100px]
                  ${transferMode === mode.id
                    ? 'bg-white dark:bg-gray-800 shadow-md scale-105 ring-2 ring-purple-500/50'
                    : 'hover:bg-white/50 dark:hover:bg-gray-800/50 opacity-70 hover:opacity-100'}
                `}
              >
                <div className="flex items-center gap-1 mb-1">
                  <mode.from className="w-5 h-5 text-gray-700 dark:text-gray-200" />
                  <ArrowRightLeft className="w-3 h-3 text-gray-400" />
                  <mode.to className="w-5 h-5 text-gray-700 dark:text-gray-200" />
                </div>
                <span className="text-xs font-semibold text-gray-600 dark:text-gray-300 whitespace-nowrap">
                  {mode.label}
                </span>

                {transferMode === mode.id && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute inset-0 rounded-2xl border-2 border-purple-500/20 pointer-events-none"
                  />
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Missing Login Cards */}
        <div className="flex flex-wrap justify-center gap-4 mb-8 max-w-3xl mx-auto">
          {!loginStatus.spotify_logged_in && (
            <ServiceAppButton
              icon={Music2}
              label="Conectar Spotify"
              onClick={() => handleLogin('spotify')}
              gradient="bg-gradient-to-br from-[#1DB954] to-[#191414]"
              loading={isRetrying}
            />
          )}
          {!loginStatus.youtube_logged_in && (
            <ServiceAppButton
              icon={Youtube}
              label="Conectar YouTube"
              onClick={() => handleLogin('youtube')}
              gradient="bg-gradient-to-br from-[#FF0000] to-[#282828]"
              loading={isRetrying}
            />
          )}

          {!loginStatus.amazon_logged_in && (
            <ServiceAppButton
              icon={AmazonMusicIcon}
              label="Conectar Amazon"
              onClick={() => handleLogin('amazon')}
              gradient="bg-gradient-to-br from-[#25D1DA] to-[#232F3E]"
              loading={isRetrying}
            />
          )}
        </div>

        {/* Transfer Components */}
        <motion.div
          key={transferMode}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="max-w-4xl mx-auto"
        >
          {transferMode === 'youtube-to-spotify' ? (
            <PlaylistTransfer />
          ) : transferMode === 'spotify-to-youtube' ? (
            <SpotifyToYouTubeTransfer />
          ) : transferMode === 'amazon-to-spotify' ? (
            <AmazonToSpotifyTransfer />
          ) : (
            <div className="text-center p-8">
              <p className="text-gray-500">Modo de transferência em desenvolvimento...</p>
            </div>
          )}
        </motion.div>
      </main>
    </div>
  )
}

function AppContent() {
  useLayoutEffect(() => {
    document.documentElement.classList.add('dark');
  }, []);

  const loginStatus = useIsLoggedIn()

  useEffect(() => {
    if ('caches' in window) {
      caches.keys().then(names => {
        names.forEach(name => {
          caches.delete(name);
        });
      });
    }
  }, []);

  if (loginStatus === null) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin mx-auto mb-6"></div>
          <p className="text-gray-400 font-medium animate-pulse">Carregando...</p>
        </div>
      </div>
    )
  }

  if (!loginStatus.spotify_logged_in && !loginStatus.youtube_logged_in && !loginStatus.deezer_logged_in && !loginStatus.amazon_logged_in) {
    return <LoginPage />
  }

  return <TransferApp loginStatus={loginStatus} />
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/privacy-policy" element={<PrivacyPolicy />} />
        <Route path="/terms" element={<TermsOfService />} />
        <Route path="*" element={<AppContent />} />
      </Routes>
    </Router>
  )
}

export default App