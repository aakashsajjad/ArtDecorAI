'use client';
// src/app/components/Footer.js
import { motion } from 'framer-motion';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <motion.footer
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.4 }}
      className="w-full bg-dark-gray text-light-gray text-center p-8 shadow-inner mt-20"
    >
      <div className="container mx-auto">
        <p className="text-lg font-sans">&copy; {currentYear} AI-Decor. All rights reserved.</p>
        <p className="text-md font-sans mt-2">Crafted with <span className="text-accent">&#9829;</span> by Your Team</p>
      </div>
    </motion.footer>
  );
}