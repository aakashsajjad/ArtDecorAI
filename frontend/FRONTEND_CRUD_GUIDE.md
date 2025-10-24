# Frontend CRUD Operations for Artwork Table

This guide shows you how to run the frontend CRUD operations for the artwork table in the ArtDecorAI project.

## 🚀 Quick Start

### Method 1: Run Frontend Demo (No Backend Required)

This is the easiest way to see the frontend CRUD interface:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start the development server
npm run dev
```

**Access the demo:**
- 🌐 **Main App**: http://localhost:3000
- 🎨 **Artwork CRUD Demo**: http://localhost:3000/artwork-demo
- 🔧 **Artwork CRUD (with API)**: http://localhost:3000/artwork-crud

### Method 2: Using the Batch File (Windows)

```bash
# Navigate to frontend directory
cd frontend

# Run the batch file
run-frontend-crud.bat
```

## 📋 What You'll See

### 🎨 Artwork CRUD Demo Page (`/artwork-demo`)

**Features:**
- ✅ **CREATE** - Add new artworks with form
- ✅ **READ** - View all artworks in cards
- ✅ **UPDATE** - Edit existing artworks
- ✅ **DELETE** - Remove artworks
- ✅ **SEARCH** - Filter by title, brand
- ✅ **FILTER** - Filter by style, price range
- ✅ **OPERATION LOG** - See all CRUD operations in real-time

**Mock Data Included:**
- Modern Abstract Waves ($299.99)
- Minimalist Black Lines ($199.99)
- Vintage Botanical Print ($149.99)

### 🔧 Artwork CRUD with API (`/artwork-crud`)

**Features:**
- ✅ **Full API Integration** - Connects to Python backend
- ✅ **Real Database Operations** - CRUD with Supabase
- ✅ **Error Handling** - Shows API errors
- ✅ **Loading States** - Visual feedback during operations

**Requirements:**
- Python backend must be running (`python main.py`)
- Supabase database must be accessible

## 🛠️ CRUD Operations Available

### 1. CREATE Operations
```javascript
// Add new artwork
const newArtwork = {
  title: "Modern Abstract Waves",
  brand: "Contemporary Gallery",
  price: 299.99,
  style_tags: ["abstract", "modern", "blue"],
  dominant_palette: {
    primary: "#1e3a8a",
    secondary: "#3b82f6"
  },
  image_url: "https://example.com/artwork1.jpg"
};
```

### 2. READ Operations
```javascript
// Get all artworks
GET /api/artworks/

// Get artwork by ID
GET /api/artworks/{id}

// Search artworks
GET /api/artworks/search?style_tags=abstract&min_price=100
```

### 3. UPDATE Operations
```javascript
// Update artwork
PUT /api/artworks/{id}
{
  "price": 349.99,
  "style_tags": ["abstract", "modern", "blue", "contemporary"]
}
```

### 4. DELETE Operations
```javascript
// Delete artwork
DELETE /api/artworks/{id}
```

## 🎯 Frontend Components

### 1. ArtworkCRUDDemo.js
- **Purpose**: Standalone demo with mock data
- **Features**: No backend required, shows all CRUD operations
- **Best for**: Testing UI, demonstrating functionality

### 2. ArtworkCRUD.js
- **Purpose**: Full API integration
- **Features**: Real database operations, error handling
- **Best for**: Production use, real data

### 3. artworkApi.js
- **Purpose**: API service layer
- **Features**: Centralized API calls, error handling
- **Best for**: Reusable API functions

## 🔧 Development Setup

### Prerequisites
- Node.js 18 or higher
- npm or yarn
- Python backend (for API integration)

### Installation
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Environment Variables
Create `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## 🎨 UI Features

### Visual Elements
- **Artwork Cards** - Display artwork information
- **Color Palettes** - Show dominant colors
- **Style Tags** - Display style categories
- **Images** - Artwork previews
- **Forms** - Create/edit artwork data

### Interactive Features
- **Search** - Filter artworks by text
- **Filters** - Filter by style, price range
- **Sorting** - Order by date, price, title
- **Pagination** - Handle large datasets
- **Real-time Updates** - Live operation log

### Responsive Design
- **Mobile First** - Works on all devices
- **Grid Layout** - Responsive artwork cards
- **Form Validation** - Client-side validation
- **Loading States** - Visual feedback

## 🚀 Running Both Frontend and Backend

### Terminal 1: Start Backend
```bash
cd backend
python main.py
```

### Terminal 2: Start Frontend
```bash
cd frontend
npm run dev
```

### Access Points
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install dependencies
   ```bash
   npm install
   ```

2. **Port Already in Use**: Change port
   ```bash
   npm run dev -- -p 3001
   ```

3. **API Connection Error**: Check backend is running
   ```bash
   # Check if backend is running
   curl http://localhost:8000/health
   ```

4. **CORS Error**: Add CORS configuration in backend

### Debug Mode
```bash
# Run with debug logging
DEBUG=* npm run dev
```

## 📊 Expected Output

When you run the demo, you should see:

```
🎨 ArtDecorAI - Frontend CRUD Operations
================================================
✅ Node.js and npm are available
✅ Dependencies already installed
🚀 Starting Next.js development server...

📱 Frontend will be available at: http://localhost:3000
🎨 Artwork CRUD Demo: http://localhost:3000/artwork-demo
🔧 Artwork CRUD (with API): http://localhost:3000/artwork-crud

> Ready - started server on 0.0.0.0:3000
```

## 🎯 Next Steps

1. **Run the demo**: Visit http://localhost:3000/artwork-demo
2. **Test CRUD operations**: Create, read, update, delete artworks
3. **Connect to backend**: Set up API integration
4. **Customize UI**: Modify components for your needs
5. **Add features**: Implement additional functionality

## 📚 Additional Resources

- **Next.js Documentation**: https://nextjs.org/docs
- **React Documentation**: https://react.dev
- **Tailwind CSS**: https://tailwindcss.com
- **Framer Motion**: https://www.framer.com/motion
