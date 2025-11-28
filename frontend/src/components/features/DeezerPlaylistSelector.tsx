import { useState, useEffect } from 'react'
import { API_BASE_URL } from '../../config'
import { Button } from '../ui/Button'
import { ArrowPathIcon, CheckCircleIcon } from '@heroicons/react/24/outline'
import { DeezerIcon } from '../ui/Icons'

interface Playlist {
    id: string
    name: string
    tracks_count: number
    creator: string
    cover_image: string | null
    public: boolean
}

interface DeezerPlaylistSelectorProps {
    onSelect: (playlist: Playlist) => void
    selectedPlaylistId?: string
}

export function DeezerPlaylistSelector({ onSelect, selectedPlaylistId }: DeezerPlaylistSelectorProps) {
    const [playlists, setPlaylists] = useState<Playlist[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    const fetchPlaylists = async () => {
        setLoading(true)
        setError(null)
        try {
            const res = await fetch(`${API_BASE_URL}/deezer/playlists`, { credentials: 'include' })
            if (!res.ok) {
                if (res.status === 401) {
                    throw new Error('Não autenticado no Deezer')
                }
                throw new Error('Falha ao carregar playlists')
            }
            const data = await res.json()
            setPlaylists(data.playlists)
        } catch (err: any) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchPlaylists()
    }, [])

    if (loading) {
        return (
            <div className="flex justify-center p-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="text-center p-8 bg-red-50 dark:bg-red-900/20 rounded-xl">
                <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
                <Button onClick={fetchPlaylists} variant="outline" size="sm">
                    <ArrowPathIcon className="w-4 h-4 mr-2" />
                    Tentar Novamente
                </Button>
            </div>
        )
    }

    if (playlists.length === 0) {
        return (
            <div className="text-center p-8 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
                <p className="text-gray-600 dark:text-gray-400">Nenhuma playlist encontrada no Deezer.</p>
            </div>
        )
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-[600px] overflow-y-auto p-2">
            {playlists.map((playlist) => (
                <div
                    key={playlist.id}
                    onClick={() => onSelect(playlist)}
                    className={`
            relative group cursor-pointer rounded-xl p-3 transition-all duration-200 border-2
            ${selectedPlaylistId === playlist.id
                            ? 'border-purple-600 bg-purple-50 dark:bg-purple-900/20 shadow-md transform scale-[1.02]'
                            : 'border-transparent bg-white dark:bg-gray-800 hover:border-purple-300 dark:hover:border-purple-700 hover:shadow-md'
                        }
          `}
                >
                    <div className="flex items-start gap-4">
                        <div className="relative w-16 h-16 flex-shrink-0 rounded-lg overflow-hidden bg-gray-200 dark:bg-gray-700">
                            {playlist.cover_image ? (
                                <img
                                    src={playlist.cover_image}
                                    alt={playlist.name}
                                    className="w-full h-full object-cover"
                                />
                            ) : (
                                <div className="w-full h-full flex items-center justify-center">
                                    <DeezerIcon className="w-8 h-8 text-gray-400" />
                                </div>
                            )}
                            {selectedPlaylistId === playlist.id && (
                                <div className="absolute inset-0 bg-purple-600/20 flex items-center justify-center">
                                    <CheckCircleIcon className="w-8 h-8 text-white drop-shadow-lg" />
                                </div>
                            )}
                        </div>

                        <div className="flex-1 min-w-0">
                            <h3 className={`font-semibold truncate ${selectedPlaylistId === playlist.id
                                    ? 'text-purple-700 dark:text-purple-300'
                                    : 'text-gray-900 dark:text-white'
                                }`}>
                                {playlist.name}
                            </h3>
                            <p className="text-sm text-gray-500 dark:text-gray-400 truncate">
                                {playlist.tracks_count} músicas
                            </p>
                            <p className="text-xs text-gray-400 dark:text-gray-500 mt-1 truncate">
                                Por {playlist.creator}
                            </p>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}
