'use client';
// src/app/components/UploadSection.js
'use client';

import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { useDropzone } from 'react-dropzone';

export default function UploadSection() {
  const [image, setImage] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setImage(file);
      setImageSrc(URL.createObjectURL(file));
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const handleAnalyzeRoom = () => {
    if (image) {
      alert('Analyzing room with image: ' + image.name);
      // Here you would typically send the image to your backend for analysis
    } else {
      alert('Please upload an image first.');
    }
  };

  return (
    <motion.section>
        <div className="container mx-auto px-4">
          <motion.h2
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-5xl font-bold font-serif text-center text-dark-gray mb-12"
          >
            Upload Your Room Photo
          </motion.h2>

          <div
            {...getRootProps()}
            className="border-dashed border-4 border-primary rounded-3xl p-20 text-center cursor-pointer hover:border-accent transition-colors duration-300 ease-in-out bg-white shadow-xl hover:shadow-2xl"
          >
            <input {...getInputProps()} />
            {isDragActive ? (
              <p className="text-primary text-xl font-sans">Drop the files here ...</p>
            ) : (
              <p className="text-gray-600 text-xl font-sans flex flex-col items-center justify-center">
                <svg className="w-16 h-16 mb-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 0115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                Drag 'n' drop some files here, or click to select files
              </p>
            )}
          </div>

          {imageSrc && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              className="mt-12 flex justify-center"
            >
              <img src={imageSrc} alt="Preview" className="max-h-[500px] rounded-2xl shadow-xl border-4 border-primary" />
            </motion.div>
          )}

          <div className="text-center mt-12">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-gradient-to-r from-primary to-secondary hover:from-secondary hover:to-primary text-white font-bold py-4 px-12 rounded-full text-xl shadow-lg hover:shadow-xl transition duration-300 ease-in-out transform hover:-translate-y-1"
              onClick={() => console.log('Analyze Room clicked')}
            >
              Analyze Room
            </motion.button>
          </div>
        </div>
      </motion.section>
  );
}