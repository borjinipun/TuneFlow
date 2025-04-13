import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Search,
    Play,
    Pause,
    ListMusic,
    Heart,
    ChevronDown,
    X,
    Loader2,
    Share,
    Moon,
    Sun,
    AlertCircle,
    Music,
    LayoutList,
    Settings,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import {
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
} from '@/components/ui/sheet';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from '@/lib/utils';

// Mock Data & Types (Replace with actual API calls and types)
interface VideoItem {
    id: string;
    title: string;
    artist: string;
    thumbnail: string;
    duration: string;
    url: string; // Add URL for direct playback
}

interface Playlist {
    id: string;
    name: string;
    videos: VideoItem[];
}

const mockSearchResults: VideoItem[] = [
    {
        id: 'dQw4w9WgXcQ',
        title: 'Rick Astley - Never Gonna Give You Up (Official Music Video)',
        artist: 'Rick Astley',
        thumbnail: 'https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
        duration: '3:32',
        url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    },
    {
        id: 'fJ9rUzIMcZQ',
        title: 'Queen – Bohemian Rhapsody (Official Video Remastered)',
        artist: 'Queen',
        thumbnail: 'https://img.youtube.com/vi/fJ9rUzIMcZQ/mqdefault.jpg',
        duration: '5:55',
        url: 'https://www.youtube.com/watch?v=fJ9rUzIMcZQ',
    },
    {
        id: 'pzigoHPE_mE',
        title: 'a-ha - Take On Me (Official 4K Music Video)',
        artist: 'a-ha',
        thumbnail: 'https://img.youtube.com/vi/pzigoHPE_mE/mqdefault.jpg',
        duration: '3:49',
        url: 'https://www.youtube.com/watch?v=pzigoHPE_mE',
    },
    {
        id: 'HgzUkwZGmJk',
        title: "Michael Jackson - Billie Jean (Official Music Video)",
        artist: "Michael Jackson",
        thumbnail: "https://img.youtube.com/vi/HgzUkwZGmJk/mqdefault.jpg",
        duration: "4:54",
        url: "https://www.youtube.com/watch?v=HgzUkwZGmJk",
    },
    {
        id: 'kOkQ4T5WO9E',
        title: "The Weeknd - Blinding Lights (Official Music Video)",
        artist: "The Weeknd",
        thumbnail: "https://img.youtube.com/vi/kOkQ4T5WO9E/mqdefault.jpg",
        duration: "3:21",
        url: "https://www.youtube.com/watch?v=kOkQ4T5WO9E"
    }
];

const mockPlaylists: Playlist[] = [
    {
        id: 'p1',
        name: 'My Favorites',
        videos: [mockSearchResults[0], mockSearchResults[2]],
    },
    {
        id: 'p2',
        name: '80s Hits',
        videos: [mockSearchResults[1], mockSearchResults[2]],
    },
];

const mockLyrics = `
[Verse 1]
We're no strangers to love
You know the rules and so do I
A full commitment's what I'm thinking of
You wouldn't get this from any other guy

[Pre-Chorus]
I just wanna tell you how I'm feeling
Gotta make you understand

[Chorus]
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
`;

// Helper Components
const VideoCard: React.FC<{
    video: VideoItem;
    onPlay: (video: VideoItem) => void;
    onAddToPlaylist?: (video: VideoItem, playlistId: string) => void;
    playlists?: Playlist[];
    isListView?: boolean;
}> = ({ video, onPlay, onAddToPlaylist, playlists, isListView }) => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    return (
        <Card
            className={cn(
                'group relative overflow-hidden transition-all duration-300',
                isListView
                    ? 'flex flex-row items-center gap-4 p-4'
                    : 'hover:scale-[1.02] hover:shadow-lg',
            )}
            onClick={() => onPlay(video)}
        >
            {isListView ? (
                <>
                    <img
                        src={video.thumbnail}
                        alt={video.title}
                        className="w-24 h-24 rounded-md object-cover"
                    />
                    <div className="flex-1">
                        <CardTitle className="text-sm font-semibold">{video.title}</CardTitle>
                        <CardDescription className="text-xs text-gray-400">
                            {video.artist} - {video.duration}
                        </CardDescription>
                    </div>
                </>
            ) : (
                <>
                    <img
                        src={video.thumbnail}
                        alt={video.title}
                        className="w-full h-48 object-cover rounded-t-lg"
                    />
                    <CardHeader>
                        <CardTitle className="text-sm font-semibold">{video.title}</CardTitle>
                        <CardDescription className="text-xs text-gray-400">
                            {video.artist} - {video.duration}
                        </CardDescription>
                    </CardHeader>
                </>
            )}

            {playlists && (
                <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <DropdownMenu open={isMenuOpen} onOpenChange={setIsMenuOpen}>
                        <DropdownMenuTrigger asChild>
                            <Button
                                variant="ghost"
                                size="icon"
                                className="text-white hover:bg-white/20"
                            >
                                <ListMusic className="h-4 w-4" />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" className="min-w-[200px]">
                            <DropdownMenuLabel>Add to Playlist</DropdownMenuLabel>
                            <DropdownMenuSeparator />
                            {playlists.length > 0 ? (
                                playlists.map((playlist) => (
                                    <DropdownMenuItem
                                        key={playlist.id}
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            onAddToPlaylist?.(video, playlist.id);
                                            setIsMenuOpen(false);
                                        }}
                                    >
                                        {playlist.name}
                                    </DropdownMenuItem>
                                ))
                            ) : (
                                <DropdownMenuItem disabled>No playlists</DropdownMenuItem>
                            )}
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                                onClick={(e) => {
                                    e.stopPropagation();
                                    // Handle create new playlist
                                    setIsMenuOpen(false);
                                }}
                            >
                                + New Playlist
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </div>
            )}
        </Card>
    );
};

const MiniPlayer: React.FC<{
    currentVideo: VideoItem | null;
    onPause: () => void;
    onPlay: () => void;
    isPlaying: boolean;
    onClose: () => void;
}> = ({ currentVideo, onPause, onPlay, isPlaying, onClose }) => {
    if (!currentVideo) return null;

    return (
        <motion.div
            initial={{ y: '100%', opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: '100%', opacity: 0 }}
            transition={{ type: 'spring', stiffness: 200, damping: 20 }}
            className="fixed bottom-0 left-0 right-0 bg-gray-900/90 backdrop-blur-md border-t border-gray-800 p-4 flex items-center justify-between z-50"
        >
            <div className="flex items-center gap-4">
                <img
                    src={currentVideo.thumbnail}
                    alt={currentVideo.title}
                    className="w-16 h-16 rounded-md object-cover"
                />
                <div>
                    <h3 className="text-sm font-semibold text-white">{currentVideo.title}</h3>
                    <p className="text-xs text-gray-400">{currentVideo.artist}</p>
                </div>
            </div>
            <div className="flex items-center gap-4">
                <Button
                    variant="ghost"
                    size="icon"
                    className="text-white hover:bg-white/20"
                    onClick={isPlaying ? onPause : onPlay}
                >
                    {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6" />}
                </Button>
                <Button
                    variant="ghost"
                    size="icon"
                    className="text-white hover:bg-white/20"
                    onClick={onClose}
                >
                    <X className="h-6 w-6" />
                </Button>
            </div>
        </motion.div>
    );
};

const FullScreenPlayer: React.FC<{
    currentVideo: VideoItem | null;
    onPause: () => void;
    onPlay: () => void;
    isPlaying: boolean;
    onClose: () => void;
    lyrics: string | null;
}> = ({ currentVideo, onPause, onPlay, isPlaying, onClose, lyrics }) => {
    const [showLyrics, setShowLyrics] = useState(false);
    if (!currentVideo) return null;

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 bg-black z-50 flex flex-col"
        >
            <div className="absolute top-4 left-4">
                <Button
                    variant="ghost"
                    size="icon"
                    className="text-white hover:bg-white/20"
                    onClick={onClose}
                >
                    <X className="h-6 w-6" />
                </Button>
            </div>

            <div className="flex-grow flex items-center justify-center">
                {/* eslint-disable-next-line jsx-a11y/media-has-caption */}
                <iframe
                    className="w-full aspect-video"
                    src={`https://www.youtube.com/embed/${currentVideo.id}?autoplay=1`}
                    title={currentVideo.title}
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowFullScreen
                />
            </div>

            <div className="absolute bottom-20 left-0 right-0 p-4 flex items-center justify-center gap-4">
                <Button
                    variant="ghost"
                    size="icon"
                    className="text-white hover:bg-white/20"
                    onClick={isPlaying ? onPause : onPlay}
                >
                    {isPlaying ? <Pause className="h-8 w-8" /> : <Play className="h-8 w-8" />}
                </Button>
                <Button
                    variant="ghost"
                    size="icon"
                    className="text-white hover:bg-white/20"
                    onClick={() => setShowLyrics(!showLyrics)}
                >
                    <Music className="h-6 w-6" />
                </Button>
            </div>

            <AnimatePresence>
                {showLyrics && lyrics && (
                    <motion.div
                        initial={{ y: '100%' }}
                        animate={{ y: '0%' }}
                        exit={{ y: '100%' }}
                        transition={{ type: 'spring', stiffness: 200, damping: 25 }}
                        className="absolute bottom-0 left-0 right-0 bg-black/80 backdrop-blur-md p-4 max-h-48 overflow-y-auto"
                    >
                        <h4 className="text-lg font-semibold text-white mb-2">Lyrics</h4>
                        <p className="text-gray-200 whitespace-pre-line">{lyrics}</p>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
};

const PlaylistSheet: React.FC<{
    playlists: Playlist[];
    onSelectPlaylist: (playlistId: string) => void;
    onClose: () => void;
}> = ({ playlists, onSelectPlaylist, onClose }) => {
    return (
        <SheetContent side="bottom" className="bg-gray-900 text-white border-gray-800">
            <SheetHeader>
                <SheetTitle>Playlists</SheetTitle>
                <SheetDescription>
                    Add to an existing playlist or create a new one.
                </SheetDescription>
            </SheetHeader>
            <div className="space-y-4">
                {playlists.length > 0 ? (
                    playlists.map((playlist) => (
                        <Button
                            key={playlist.id}
                            variant="ghost"
                            className="w-full justify-start text-white hover:bg-white/10"
                            onClick={() => {
                                onSelectPlaylist(playlist.id);
                                onClose();
                            }}
                        >
                            {playlist.name} ({playlist.videos.length} tracks)
                        </Button>
                    ))
                ) : (
                    <p className="text-gray-400">No playlists yet.</p>
                )}
                <Button
                    variant="outline"
                    className="w-full text-white hover:bg-white/10 border-gray-700"
                    onClick={() => {
                        // Handle create new playlist
                        onClose();
                    }}
                >
                    + New Playlist
                </Button>
            </div>
        </SheetContent>
    );
};

const SettingsSheet: React.FC<{
    isDarkMode: boolean;
    onToggleDarkMode: () => void;
    onResetData: () => void;
}> = ({ isDarkMode, onToggleDarkMode, onResetData }) => {
    return (
        <SheetContent side="right" className="bg-gray-900 text-white border-gray-800 w-full md:max-w-md">
            <SheetHeader>
                <SheetTitle>Settings</SheetTitle>
                <SheetDescription>
                    Customize the app to your preferences.
                </SheetDescription>
            </SheetHeader>
            <div className="space-y-6">
                <div className="flex items-center justify-between">
                    <span className="text-lg font-medium">Dark Mode</span>
                    <Button
                        variant="outline"
                        size="icon"
                        className={cn(
                            "w-12 h-12 rounded-full",
                            isDarkMode ? "bg-gray-800 text-white" : "bg-gray-200 text-gray-900",
                            "hover:bg-gray-700",
                        )}
                        onClick={onToggleDarkMode}
                    >
                        {isDarkMode ? <Sun className="h-6 w-6" /> : <Moon className="h-6 w-6" />}
                    </Button>
                </div>
                <div>
                    <h3 className="text-lg font-medium mb-2">Data</h3>
                    <p className="text-sm text-gray-400 mb-4">
                        Clear your saved playlists and history. This action cannot be undone.
                    </p>
                    <Button
                        variant="destructive"
                        className="w-full bg-red-500/90 hover:bg-red-500"
                        onClick={onResetData}
                    >
                        <AlertCircle className="mr-2 h-4 w-4" /> Reset Data
                    </Button>
                </div>
            </div>
        </SheetContent>
    );
};

const TuneFlowApp = () => {
    const [searchResults, setSearchResults] = useState<VideoItem[]>([]);
    const [currentVideo, setCurrentVideo] = useState<VideoItem | null>(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [playlists, setPlaylists] = useState<Playlist[]>(mockPlaylists); // Replace with state management
    const [showPlaylistSheet, setShowPlaylistSheet] = useState(false);
    const [showFullScreenPlayer, setShowFullScreenPlayer] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(false);
    const [isDarkMode, setIsDarkMode] = useState(false);
    const [showSettingsSheet, setShowSettingsSheet] = useState(false);
    const [isListView, setIsListView] = useState(false); // List view toggle
    const [lyrics, setLyrics] = useState<string | null>(null);

    // Function to handle video playback
    const handlePlay = useCallback((video: VideoItem) => {
        setCurrentVideo(video);
        setIsPlaying(true);
        setShowFullScreenPlayer(false); // Start with mini player
    }, []);

    const handlePause = () => {
        setIsPlaying(false);
    };

    const handleResume = () => {
        setIsPlaying(true);
    };

    const handleClosePlayer = () => {
        setCurrentVideo(null);
        setIsPlaying(false);
        setShowFullScreenPlayer(false);
    };

    // Function to simulate fetching search results
    const handleSearch = async (query: string) => {
        setLoading(true);
        setSearchTerm(query);
        // Simulate API call delay
        setTimeout(() => {
            if (query) {
                const filteredResults = mockSearchResults.filter((video) =>
                    video.title.toLowerCase().includes(query.toLowerCase()) ||
                    video.artist.toLowerCase().includes(query.toLowerCase())
                );
                setSearchResults(filteredResults);
            } else {
                setSearchResults([]);
            }
            setLoading(false);
        }, 500);
    };

    const handleAddToPlaylist = (video: VideoItem, playlistId: string) => {
        setPlaylists((prevPlaylists) =>
            prevPlaylists.map((playlist) =>
                playlist.id === playlistId
                    ? { ...playlist, videos: [...playlist.videos, video] }
                    : playlist
            )
        );
    };

    const handleSelectPlaylist = (playlistId: string) => {
        // Handle logic to add currentVideo to the selected playlist
        if (currentVideo) {
            handleAddToPlaylist(currentVideo, playlistId);
        }
    };

    const handleResetData = () => {
        // Implement logic to clear user data (playlists, history, etc.)
        setPlaylists([]); // Clear playlists
        setCurrentVideo(null); // Clear current video
        setSearchResults([]);
        setSearchTerm('');
        // Show a toast/alert to confirm
        alert('All data has been reset.');
    };

    // Dark mode toggle
    useEffect(() => {
        if (isDarkMode) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }, [isDarkMode]);

    // Function to simulate fetching lyrics
    const fetchLyrics = useCallback(async (videoId: string) => {
        // Replace with actual API call
        setLyrics(null); // Clear previous lyrics
        if (!videoId) return;

        setTimeout(() => {
            setLyrics(mockLyrics); // set mock lyrics
        }, 750);

    }, []);

    // Fetch lyrics when a new video is played
    useEffect(() => {
        if (currentVideo) {
            fetchLyrics(currentVideo.id);
        } else {
            setLyrics(null);
        }
    }, [currentVideo, fetchLyrics]);

    return (
        <div className={cn(
            "min-h-screen bg-gray-100 dark:bg-gray-950",
            currentVideo ? "pb-20" : ""
        )}>
            {/* Main Content Area */}
            <div className="container mx-auto p-4">
                {/* Search Bar */}
                <div className="mb-8">
                    <div className="flex items-center gap-4">
                        <Input
                            type="text"
                            placeholder="Search for songs, artists..."
                            value={searchTerm}
                            onChange={(e) => handleSearch(e.target.value)}
                            className="w-full md:w-96 bg-white dark:bg-gray-800 text-gray-900 dark:text-white border-gray-300 dark:border-gray-700"
                        />
                        <Button
                            variant="outline"
                            className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white border-gray-300 dark:border-gray-700"
                            onClick={() => handleSearch(searchTerm)}
                            disabled={loading}
                        >
                            {loading ? (
                                <Loader2 className="animate-spin h-5 w-5" />
                            ) : (
                                <Search className="h-5 w-5" />
                            )}
                        </Button>
                        <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                                <Button
                                    variant="outline"
                                    className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white border-gray-300 dark:border-gray-700"
                                >
                                    <LayoutList className="h-5 w-5" />
                                    <ChevronDown className="ml-2 h-4 w-4" />
                                </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                                <DropdownMenuItem onClick={() => setIsListView(false)}>
                                    Grid View
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => setIsListView(true)}>
                                    List View
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                        <Sheet open={showSettingsSheet} onOpenChange={setShowSettingsSheet}>
                            <SheetTrigger asChild>
                                <Button
                                    variant="outline"
                                    className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white border-gray-300 dark:border-gray-700"
                                >
                                    <Settings className="h-5 w-5" />
                                </Button>
                            </SheetTrigger>
                            <SettingsSheet
                                isDarkMode={isDarkMode}
                                onToggleDarkMode={() => setIsDarkMode(!isDarkMode)}
                                onResetData={handleResetData}
                            />
                        </Sheet>
                    </div>
                </div>

                {/* Search Results */}
                {loading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {[...Array(6)].map((_, i) => (
                            <Card key={i} className="animate-pulse">
                                <div className="w-full h-48 bg-gray-300 dark:bg-gray-700 rounded-t-lg"></div>
                                <CardHeader>
                                    <div className="h-4 bg-gray-300 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                                    <div className="h-3 bg-gray-200 dark:bg-gray-800 rounded w-1/2"></div>
                                </CardHeader>
                            </Card>
                        ))}
                    </div>
                ) : (
                    <AnimatePresence>
                        {searchResults.length > 0 ? (
                            <div
                                className={cn(
                                    'grid gap-6',
                                    isListView ? 'grid-cols-1' : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
                                )}
                            >
                                {searchResults.map((video) => (
                                    <VideoCard
                                        key={video.id}
                                        video={video}
                                        onPlay={handlePlay}
                                        onAddToPlaylist={(v, pId) => {
                                            handleAddToPlaylist(v, pId);
                                            setShowPlaylistSheet(false); // Close sheet after adding
                                        }}
                                        playlists={playlists}
                                        isListView={isListView}
                                    />
                                ))}
                            </div>) : (
                            searchTerm && (
                                <div className="text-center text-gray-500 dark:text-gray-400">
                                    No results found for "{searchTerm}".
                                </div>
                            )
                        )}
                    </AnimatePresence>
                )}
            </div>

            {/* Mini Player */}
            <AnimatePresence>
                {currentVideo && !showFullScreenPlayer && (
                    <MiniPlayer
                        currentVideo={currentVideo}
                        onPause={handlePause}
                        onPlay={handleResume}
                        isPlaying={isPlaying}
                        onClose={handleClosePlayer}
                    />
                )}
            </AnimatePresence>

            {/* Full Screen Player */}
            <AnimatePresence>
                {currentVideo && showFullScreenPlayer && (
                    <FullScreenPlayer
                        currentVideo={currentVideo}
                        onPause={handlePause}
                        onPlay={handleResume}
                        isPlaying={isPlaying}
                        onClose={handleClosePlayer}
                        lyrics={lyrics}
                    />
                )}
            </AnimatePresence>

            {/* Playlist Sheet */}
            <Sheet open={showPlaylistSheet} onOpenChange={setShowPlaylistSheet}>
                <PlaylistSheet
                    playlists={playlists}
                    onSelectPlaylist={handleSelectPlaylist}
                    onClose={() => setShowPlaylistSheet(false)}
                />
            </Sheet>
            {/* Play Directly from URL */}
            {currentVideo && (
                <div className="absolute top-4 right-4 z-50">
                    <Button
                        variant="outline"
                        size="sm"
                        className="bg-white/90 text-gray-900 border-gray-300 hover:bg-white"
                        onClick={() => window.open(currentVideo.url, '_blank')}
                    >
                        <Share className="mr-2 h-4 w-4" />
                        Play in Browser
                    </Button>
                </div>
            )}
        </div>
    );
};

export default TuneFlowApp;

