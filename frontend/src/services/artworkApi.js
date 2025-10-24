/**
 * API service for artwork CRUD operations
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ArtworkAPI {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      // Handle 204 No Content responses
      if (response.status === 204) {
        return null;
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // CREATE - Create new artwork
  async createArtwork(artworkData) {
    return this.request('/api/artworks/', {
      method: 'POST',
      body: JSON.stringify(artworkData),
    });
  }

  // READ - Get artwork by ID
  async getArtwork(id) {
    return this.request(`/api/artworks/${id}`);
  }

  // READ - Get all artworks with pagination
  async getAllArtworks(limit = 10, offset = 0) {
    return this.request(`/api/artworks/?limit=${limit}&offset=${offset}`);
  }

  // UPDATE - Update artwork
  async updateArtwork(id, artworkData) {
    return this.request(`/api/artworks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(artworkData),
    });
  }

  // DELETE - Delete artwork
  async deleteArtwork(id) {
    return this.request(`/api/artworks/${id}`, {
      method: 'DELETE',
    });
  }

  // SEARCH - Search artworks with filters
  async searchArtworks(searchParams) {
    const queryString = new URLSearchParams();
    
    if (searchParams.style_tags) {
      searchParams.style_tags.forEach(tag => queryString.append('style_tags', tag));
    }
    if (searchParams.min_price) queryString.append('min_price', searchParams.min_price);
    if (searchParams.max_price) queryString.append('max_price', searchParams.max_price);
    if (searchParams.brand) queryString.append('brand', searchParams.brand);
    if (searchParams.limit) queryString.append('limit', searchParams.limit);
    if (searchParams.offset) queryString.append('offset', searchParams.offset);

    return this.request(`/api/artworks/search?${queryString}`);
  }

  // SEARCH - Get artworks by style
  async getArtworksByStyle(styleTags) {
    const queryString = new URLSearchParams();
    styleTags.forEach(tag => queryString.append('style_tags', tag));
    return this.request(`/api/artworks/search/style?${queryString}`);
  }

  // SEARCH - Get artworks by price range
  async getArtworksByPriceRange(minPrice, maxPrice) {
    return this.request(`/api/artworks/search/price?min_price=${minPrice}&max_price=${maxPrice}`);
  }

  // SEARCH - Get artworks by brand
  async getArtworksByBrand(brand) {
    return this.request(`/api/artworks/search/brand?brand=${encodeURIComponent(brand)}`);
  }

  // STATS - Get artwork count
  async getArtworkCount() {
    return this.request('/api/artworks/stats/count');
  }

  // RECENT - Get recent artworks
  async getRecentArtworks(limit = 5) {
    return this.request(`/api/artworks/recent?limit=${limit}`);
  }

  // HEALTH - Check API health
  async checkHealth() {
    return this.request('/health');
  }
}

// Create and export a singleton instance
const artworkAPI = new ArtworkAPI();
export default artworkAPI;

// Export individual methods for convenience
export const {
  createArtwork,
  getArtwork,
  getAllArtworks,
  updateArtwork,
  deleteArtwork,
  searchArtworks,
  getArtworksByStyle,
  getArtworksByPriceRange,
  getArtworksByBrand,
  getArtworkCount,
  getRecentArtworks,
  checkHealth
} = artworkAPI;
