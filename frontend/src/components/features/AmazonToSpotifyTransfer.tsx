import { useState, useEffect } from 'react'
import { API_BASE_URL } from '../../config'
import { Button } from '../ui/Button'
import { AmazonPlaylistSelector } from './AmazonPlaylistSelector'
import { ArrowRightIcon, CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline'
import { AmazonMusicIcon } from '../ui/Icons'
import { Music2 } from 'lucide-react'

interface TransferStatus {
    state: string
    status: string
    progress: number
    current?: number
    total?: number
    result?: {
        success: { count: number; tracks: any[] }
        failed: { count: number; tracks: any[] }
    }
    error?: string
}

export function AmazonToSpotifyTransfer() {
    const [selectedPlaylist, setSelectedPlaylist] = useState<any>(null)
    const [taskId, setTaskId] = useState<string | null>(null)
    const [status, setStatus] = useState<TransferStatus | null>(null)
    const [isStarting, setIsStarting] = useState(false)

    useEffect(() => {
        let intervalId: any

        if (taskId && status?.state !== 'SUCCESS' && status?.state !== 'FAILURE') {
            intervalId = setInterval(async () => {
                try {
                    const res = await fetch(`${API_BASE_URL}/tasks/status/${taskId}`)
                    const data = await res.json()
                    setStatus(data)

                    if (data.state === 'SUCCESS' || data.state === 'FAILURE') {
                        clearInterval(intervalId)
                    }
                } catch (error) {
                    console.error('Error polling status:', error)
                }
            }, 2000)
        }

        return () => {
            if (intervalId) clearInterval(intervalId)
        }
    }, [taskId, status?.state])

    const startTransfer = async () => {
        if (!selectedPlaylist) return

        setIsStarting(true)
        try {
            const res = await fetch(`${API_BASE_URL}/amazon/transfer`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    source: 'amazon',
                    target: 'spotify',
                    playlist_id: selectedPlaylist.id
                }),
                credentials: 'include'
            })

            const data = await res.json()
            if (data.task_id) {
                setTaskId(data.task_id)
                setStatus({ state: 'PENDING', status: 'Iniciando...', progress: 0 })
            } else {
                alert('Erro ao iniciar transferência: ' + (data.error || 'Erro desconhecido'))
            }
        } catch (error) {
            console.error('Error starting transfer:', error)
            alert('Erro ao iniciar transferência. Verifique sua conexão.')
        } finally {
            setIsStarting(false)
        }
    }

    const resetTransfer = () => {
        setTaskId(null)
        setStatus(null)
        setSelectedPlaylist(null)
    }

    if (taskId && status) {
        return (
            <div className="max-w-2xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-xl">
                <div className="text-center mb-8">
                    <h2 className="text-2xl font-bold mb-2 text-gray-900 dark:text-white">Transferindo Playlist</h2>
                    <p className="text-gray-600 dark:text-gray-400">
                        {selectedPlaylist?.name}
                    </p>
                </div>

                <div className="mb-8">
                    <div className="flex justify-between text-sm mb-2 text-gray-600 dark:text-gray-400">
                        <span>Progresso</span>
                        <span>{Math.round(status.progress)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 overflow-hidden">
                        <div
                            className="bg-gradient-to-r from-cyan-500 to-green-500 h-4 rounded-full transition-all duration-500 ease-out"
                            style={{ width: `${status.progress}%` }}
                        ></div>
                    </div>
                    <p className="text-center mt-4 text-sm text-gray-500 dark:text-gray-400 animate-pulse">
                        {status.status}
                    </p>
                </div>

                {status.state === 'SUCCESS' && (
                    <div className="bg-green-50 dark:bg-green-900/20 p-6 rounded-xl border border-green-100 dark:border-green-900/30">
                        <div className="flex items-center gap-3 mb-4">
                            <CheckCircleIcon className="w-8 h-8 text-green-600 dark:text-green-400" />
                            <h3 className="text-lg font-semibold text-green-900 dark:text-green-100">Transferência Concluída!</h3>
                        </div>
                        <div className="space-y-2 text-green-800 dark:text-green-200">
                            <p>✅ {status.result?.success.count} músicas transferidas com sucesso</p>
                            {status.result?.failed.count ? (
                                <p className="text-red-600 dark:text-red-400">❌ {status.result?.failed.count} músicas não encontradas</p>
                            ) : null}
                        </div>
                        <Button onClick={resetTransfer} className="mt-6 w-full bg-green-600 hover:bg-green-700 text-white">
                            Transferir Outra Playlist
                        </Button>
                    </div>
                )}

                {status.state === 'FAILURE' && (
                    <div className="bg-red-50 dark:bg-red-900/20 p-6 rounded-xl border border-red-100 dark:border-red-900/30">
                        <div className="flex items-center gap-3 mb-4">
                            <ExclamationCircleIcon className="w-8 h-8 text-red-600 dark:text-red-400" />
                            <h3 className="text-lg font-semibold text-red-900 dark:text-red-100">Erro na Transferência</h3>
                        </div>
                        <p className="text-red-800 dark:text-red-200 mb-6">{status.error}</p>
                        <Button onClick={resetTransfer} variant="outline" className="w-full border-red-200 hover:bg-red-50 text-red-700">
                            Tentar Novamente
                        </Button>
                    </div>
                )}
            </div>
        )
    }

    return (
        <div className="space-y-8">
            <div className="text-center space-y-4">
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center justify-center gap-3">
                    <AmazonMusicIcon className="w-8 h-8 text-cyan-500" />
                    <ArrowRightIcon className="w-6 h-6 text-gray-400" />
                    <Music2 className="w-8 h-8 text-green-600" />
                </h2>
                <p className="text-gray-600 dark:text-gray-300 max-w-xl mx-auto">
                    Selecione uma playlist do Amazon Music para transferir para sua conta do Spotify.
                </p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
                <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white flex items-center gap-2">
                    <span className="flex items-center justify-center w-6 h-6 rounded-full bg-cyan-100 dark:bg-cyan-900/30 text-cyan-600 text-sm">1</span>
                    Selecione a Playlist de Origem
                </h3>

                <AmazonPlaylistSelector
                    onSelect={setSelectedPlaylist}
                    selectedPlaylistId={selectedPlaylist?.id}
                />
            </div>

            <div className="flex justify-center pt-4">
                <Button
                    onClick={startTransfer}
                    disabled={!selectedPlaylist || isStarting}
                    size="lg"
                    className={`
            w-full md:w-auto min-w-[300px] text-lg py-6 shadow-xl transition-all duration-300
            ${!selectedPlaylist
                            ? 'opacity-50 cursor-not-allowed bg-gray-300 dark:bg-gray-700 text-gray-500'
                            : 'bg-gradient-to-r from-cyan-500 to-green-600 hover:from-cyan-600 hover:to-green-700 hover:scale-105 hover:shadow-2xl text-white'
                        }
          `}
                >
                    {isStarting ? (
                        <span className="flex items-center gap-2">
                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                            Iniciando...
                        </span>
                    ) : (
                        <span className="flex items-center gap-2">
                            Iniciar Transferência
                            <ArrowRightIcon className="w-5 h-5" />
                        </span>
                    )}
                </Button>
            </div>
        </div>
    )
}
