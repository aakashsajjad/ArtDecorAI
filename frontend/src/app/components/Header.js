'use client';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function Header() {
  return (
    <motion.header
      initial={{ opacity: 0, y: -80 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: 'spring', stiffness: 60, damping: 14, duration: 0.8 }}
      className="relative z-50 w-full bg-white border-b border-gray-200"
    >
      <div className="container mx-auto flex justify-between items-center px-8 py-4">
        {/* Logo */}
        <motion.div
          whileHover={{ scale: 1.05, rotate: 1 }}
          className="text-3xl md:text-4xl font-extrabold bg-gradient-to-r from-sky-300 via-blue-500 to-indigo-400 bg-clip-text text-transparent tracking-tight select-none"
        >
          AI<span className="text-black">•Decor</span>
        </motion.div>

        {/* Navigation */}
        <nav>
          <ul className="flex items-center space-x-6 md:space-x-10">
            {['Home', 'Upload', 'About'].map((item, i) => (
              <motion.li key={item} whileHover={{ scale: 1.1, y: -2 }}>
                <Link
                  href={`#${item.toLowerCase()}`}
                  className="relative text-black/90 hover:text-black text-lg font-medium transition-colors duration-300"
                >
                  {item}
                </Link>
              </motion.li>
            ))}
          </ul>
        </nav>
      </div>

      {/* Glow border effect */}

    </motion.header>
  );
}