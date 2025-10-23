'use client';
// src/app/components/GallerySection.js
import { motion } from 'framer-motion';

export default function GallerySection() {
  const artworks = [
    { id: 1, src: 'https://via.placeholder.com/300x200?text=Artwork+1', alt: 'Artwork 1' },
    { id: 2, src: 'https://via.placeholder.com/300x200?text=Artwork+2', alt: 'Artwork 2' },
    { id: 3, src: 'https://via.placeholder.com/300x200?text=Artwork+3', alt: 'Artwork 3' },
    { id: 4, src: 'https://via.placeholder.com/300x200?text=Artwork+4', alt: 'Artwork 4' },
  ];

  return (
    <motion.section
      className="gallery-section"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: 1.6 }}
    >
      <div className="container">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1.8 }}
        >
          Recommended Artworks
        </motion.h2>
        <motion.div
          className="artwork-grid"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 2.0 }}
        >
          {artworks.map((artwork, index) => (
            <motion.div
              key={artwork.id}
              className="artwork-item"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 2.0 + index * 0.1 }}
              whileHover={{ scale: 1.05 }}
            >
              <img src={artwork.src} alt={artwork.alt} />
              <p>{artwork.alt}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </motion.section>
  );
}