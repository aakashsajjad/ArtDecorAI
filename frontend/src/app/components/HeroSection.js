'use client';
// src/app/components/HeroSection.js
import { motion } from 'framer-motion';

export default function HeroSection() {
  return (
    <section className="py-10 px-4 text-center">
      <div className="container mx-auto">
        <h2 className="text-4xl font-bold text-gray-800 mb-4">
          Upload a photo of your room and let our AI redecorate it with stunning new styles.
        </h2>
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Get Started
        </button>
      </div>
    </section>
  );
}