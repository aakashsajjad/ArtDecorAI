'use client';
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

// Mock data for demonstration
const MOCK_ARTWORKS = [
  {
    id: '1',
    title: 'Modern Abstract Waves',
    brand: 'Contemporary Gallery',
    price: 299.99,
    style_tags: ['abstract', 'modern', 'blue'],
    dominant_palette: {
      primary: '#1e3a8a',
      secondary: '#3b82f6',
      accent: '#93c5fd'
    },
    image_url: 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400',
    created_at: new Date().toISOString()
  },
  {
    id: '2',
    title: 'Minimalist Black Lines',
    brand: 'Minimal Designs',
    price: 199.99,
    style_tags: ['minimalist', 'black', 'geometric'],
    dominant_palette: {
      primary: '#000000',
      secondary: '#404040',
      accent: '#808080'
    },
    image_url: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400',
    created_at: new Date().toISOString()
  },
  {
    id: '3',
    title: 'Vintage Botanical Print',
    brand: 'Botanical Arts',
    price: 149.99,
    style_tags: ['vintage', 'botanical', 'green'],
    dominant_palette: {
      primary: '#166534',
      secondary: '#22c55e',
      accent: '#84cc16'
    },
    image_url: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400',
    created_at: new Date().toISOString()
  }
];

export default function ArtworkCRUDDemo() {
  const [artworks, setArtworks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingArtwork, setEditingArtwork] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStyle, setFilterStyle] = useState('');
  const [filterPriceMin, setFilterPriceMin] = useState('');
  const [filterPriceMax, setFilterPriceMax] = useState('');
  const [operationLog, setOperationLog] = useState([]);

  // Form state
  const [formData, setFormData] = useState({
    title: '',
    brand: '',
    price: '',
    style_tags: '',
    dominant_palette: '',
    image_url: ''
  });

  // Load mock data on component mount
  useEffect(() => {
    loadArtworks();
  }, []);

  // Mock API Functions
  const loadArtworks = async () => {
    setLoading(true);
    addToLog('Loading all artworks...');
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    setArtworks([...MOCK_ARTWORKS]);
    addToLog(`✅ Loaded ${MOCK_ARTWORKS.length} artworks`);
    setLoading(false);
  };

  const createArtwork = async (artworkData) => {
    addToLog('Creating new artwork...');
    
    const newArtwork = {
      id: Date.now().toString(),
      ...artworkData,
      price: parseFloat(artworkData.price) || null,
      style_tags: artworkData.style_tags ? artworkData.style_tags.split(',').map(tag => tag.trim()) : [],
      dominant_palette: artworkData.dominant_palette ? JSON.parse(artworkData.dominant_palette) : null,
      created_at: new Date().toISOString()
    };

    setArtworks(prev => [newArtwork, ...prev]);
    addToLog(`✅ Created artwork: ${newArtwork.title}`);
    return newArtwork;
  };

  const updateArtwork = async (id, artworkData) => {
    addToLog(`Updating artwork ${id}...`);
    
    const updatedArtwork = {
      ...artworkData,
      id,
      price: parseFloat(artworkData.price) || null,
      style_tags: artworkData.style_tags ? artworkData.style_tags.split(',').map(tag => tag.trim()) : [],
      dominant_palette: artworkData.dominant_palette ? JSON.parse(artworkData.dominant_palette) : null,
      created_at: artworks.find(a => a.id === id)?.created_at || new Date().toISOString()
    };

    setArtworks(prev => prev.map(a => a.id === id ? updatedArtwork : a));
    addToLog(`✅ Updated artwork: ${updatedArtwork.title}`);
    return updatedArtwork;
  };

  const deleteArtwork = async (id) => {
    const artwork = artworks.find(a => a.id === id);
    addToLog(`Deleting artwork ${id}...`);
    
    setArtworks(prev => prev.filter(a => a.id !== id));
    addToLog(`✅ Deleted artwork: ${artwork?.title || 'Unknown'}`);
  };

  const searchArtworks = async () => {
    setLoading(true);
    addToLog('Searching artworks...');
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    let filtered = [...MOCK_ARTWORKS];
    
    if (filterStyle) {
      filtered = filtered.filter(artwork => 
        artwork.style_tags.some(tag => tag.toLowerCase().includes(filterStyle.toLowerCase()))
      );
    }
    
    if (filterPriceMin) {
      filtered = filtered.filter(artwork => artwork.price >= parseFloat(filterPriceMin));
    }
    
    if (filterPriceMax) {
      filtered = filtered.filter(artwork => artwork.price <= parseFloat(filterPriceMax));
    }
    
    setArtworks(filtered);
    addToLog(`✅ Found ${filtered.length} artworks matching criteria`);
    setLoading(false);
  };

  // Form handlers
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    addToLog('Processing form submission...');

    try {
      if (editingArtwork) {
        await updateArtwork(editingArtwork.id, formData);
        setEditingArtwork(null);
      } else {
        await createArtwork(formData);
      }

      setShowForm(false);
      setFormData({
        title: '',
        brand: '',
        price: '',
        style_tags: '',
        dominant_palette: '',
        image_url: ''
      });
    } catch (err) {
      addToLog(`❌ Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (artwork) => {
    setEditingArtwork(artwork);
    setFormData({
      title: artwork.title || '',
      brand: artwork.brand || '',
      price: artwork.price || '',
      style_tags: artwork.style_tags ? artwork.style_tags.join(', ') : '',
      dominant_palette: artwork.dominant_palette ? JSON.stringify(artwork.dominant_palette, null, 2) : '',
      image_url: artwork.image_url || ''
    });
    setShowForm(true);
    addToLog(`📝 Editing artwork: ${artwork.title}`);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this artwork?')) {
      setLoading(true);
      try {
        await deleteArtwork(id);
      } catch (err) {
        addToLog(`❌ Error: ${err.message}`);
      } finally {
        setLoading(false);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      brand: '',
      price: '',
      style_tags: '',
      dominant_palette: '',
      image_url: ''
    });
    setEditingArtwork(null);
    setShowForm(false);
    addToLog('📝 Form reset');
  };

  const addToLog = (message) => {
    const timestamp = new Date().toLocaleTimeString();
    setOperationLog(prev => [...prev, `[${timestamp}] ${message}`]);
  };

  // Filter artworks based on search term
  const filteredArtworks = artworks.filter(artwork =>
    artwork.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    artwork.brand?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg shadow-lg p-6 mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Artwork CRUD Operations Demo</h1>
          <p className="text-gray-600 mb-6">This is a frontend demonstration of CRUD operations for the artwork table</p>
          
          {/* Search and Filter Controls */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <input
              type="text"
              placeholder="Search artworks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="text"
              placeholder="Style filter..."
              value={filterStyle}
              onChange={(e) => setFilterStyle(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="number"
              placeholder="Min price"
              value={filterPriceMin}
              onChange={(e) => setFilterPriceMin(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="number"
              placeholder="Max price"
              value={filterPriceMax}
              onChange={(e) => setFilterPriceMax(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div className="flex flex-wrap gap-4 mb-6">
            <button
              onClick={loadArtworks}
              disabled={loading}
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Load All'}
            </button>
            <button
              onClick={searchArtworks}
              disabled={loading}
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 disabled:opacity-50"
            >
              Search
            </button>
            <button
              onClick={() => setShowForm(true)}
              className="bg-purple-500 text-white px-4 py-2 rounded-lg hover:bg-purple-600"
            >
              Add New Artwork
            </button>
            <button
              onClick={() => setOperationLog([])}
              className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
            >
              Clear Log
            </button>
          </div>

          {/* Operation Log */}
          <div className="bg-gray-100 rounded-lg p-4 mb-6">
            <h3 className="text-lg font-semibold mb-2">Operation Log:</h3>
            <div className="max-h-32 overflow-y-auto text-sm font-mono">
              {operationLog.length === 0 ? (
                <p className="text-gray-500">No operations yet...</p>
              ) : (
                operationLog.map((log, index) => (
                  <div key={index} className="text-gray-700">{log}</div>
                ))
              )}
            </div>
          </div>
        </motion.div>

        {/* Artwork Form */}
        {showForm && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg shadow-lg p-6 mb-8"
          >
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              {editingArtwork ? 'Edit Artwork' : 'Add New Artwork'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Title *</label>
                  <input
                    type="text"
                    required
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Brand</label>
                  <input
                    type="text"
                    value={formData.brand}
                    onChange={(e) => setFormData({...formData, brand: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Price</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.price}
                    onChange={(e) => setFormData({...formData, price: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Style Tags (comma-separated)</label>
                  <input
                    type="text"
                    value={formData.style_tags}
                    onChange={(e) => setFormData({...formData, style_tags: e.target.value})}
                    placeholder="abstract, modern, blue"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Image URL</label>
                  <input
                    type="url"
                    value={formData.image_url}
                    onChange={(e) => setFormData({...formData, image_url: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Color Palette (JSON)</label>
                  <textarea
                    value={formData.dominant_palette}
                    onChange={(e) => setFormData({...formData, dominant_palette: e.target.value})}
                    placeholder='{"primary": "#1e3a8a", "secondary": "#3b82f6"}'
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              <div className="flex gap-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
                >
                  {loading ? 'Saving...' : (editingArtwork ? 'Update' : 'Create')}
                </button>
                <button
                  type="button"
                  onClick={resetForm}
                  className="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600"
                >
                  Cancel
                </button>
              </div>
            </form>
          </motion.div>
        )}

        {/* Artworks List */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {filteredArtworks.map((artwork, index) => (
            <motion.div
              key={artwork.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
            >
              {artwork.image_url && (
                <img
                  src={artwork.image_url}
                  alt={artwork.title}
                  className="w-full h-48 object-cover"
                  onError={(e) => {
                    e.target.style.display = 'none';
                  }}
                />
              )}
              <div className="p-6">
                <h3 className="text-xl font-bold text-gray-800 mb-2">{artwork.title}</h3>
                <p className="text-gray-600 mb-2">{artwork.brand}</p>
                {artwork.price && (
                  <p className="text-green-600 font-semibold mb-2">${artwork.price}</p>
                )}
                {artwork.style_tags && artwork.style_tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-3">
                    {artwork.style_tags.map((tag, i) => (
                      <span
                        key={i}
                        className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
                {artwork.dominant_palette && (
                  <div className="flex gap-1 mb-3">
                    {Object.values(artwork.dominant_palette).map((color, i) => (
                      <div
                        key={i}
                        className="w-6 h-6 rounded-full border border-gray-300"
                        style={{ backgroundColor: color }}
                        title={color}
                      />
                    ))}
                  </div>
                )}
                <div className="flex gap-2">
                  <button
                    onClick={() => handleEdit(artwork)}
                    className="bg-yellow-500 text-white px-3 py-1 rounded text-sm hover:bg-yellow-600"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(artwork.id)}
                    className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {artworks.length === 0 && !loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <p className="text-gray-500 text-lg">No artworks found. Add some artworks to get started!</p>
          </motion.div>
        )}
      </div>
    </div>
  );
}
