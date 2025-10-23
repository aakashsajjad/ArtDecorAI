'use client';
import { motion } from 'framer-motion';

export default function CallToActionSection() {
  return (
    <section className="py-20 bg-gradient-to-r from-primary to-secondary text-white text-center mt-20 shadow-lg">
      <div className="container mx-auto px-4">
        <motion.h2
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-5xl font-bold font-serif mb-6 drop-shadow-md"
        >
          Ready to Transform Your Space?
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-xl mb-10 max-w-2xl mx-auto opacity-90"
        >
          Join thousands of happy homeowners who have reimagined their living spaces with AI-Decor.
        </motion.p>
        <motion.button
          whileHover={{ scale: 1.05, backgroundColor: '#C5306C' }} /* Darker accent on hover */
          whileTap={{ scale: 0.95 }}
          className="bg-accent text-white font-bold py-4 px-12 rounded-full text-xl shadow-lg hover:shadow-xl transition duration-300 ease-in-out transform hover:-translate-y-1"
        >
          Start Your Journey
        </motion.button>
      </div>
    </section>
  );
}