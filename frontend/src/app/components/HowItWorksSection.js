'use client';
import { motion } from 'framer-motion';

const steps = [
  {
    id: 1,
    title: 'Upload Photo',
    description: 'Show your room and get AI recommendations.',
  },
  {
    id: 2,
    title: 'Describe Style',
    description: 'Tell us your design preferences.',
  },
  {
    id: 3,
    title: 'Voice Query',
    description: 'Speak your design ideas naturally.',
  },
  {
    id: 4,
    title: 'Get Recommendations',
    description: 'Receive personalized design suggestions.',
  },
];

export default function HowItWorksSection() {
  return (
    <section className="py-20 bg-light-gray">
      <div className="container mx-auto px-4">
        <motion.h2
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-5xl font-bold font-serif text-center text-dark-gray mb-16"
        >
          How It Works
        </motion.h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="bg-white p-8 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 ease-in-out transform hover:-translate-y-2 text-center"
            >
              <div className="text-primary text-5xl font-extrabold mb-4">{step.id}</div>
              <h3 className="text-2xl font-bold font-sans text-dark-gray mb-3">{step.title}</h3>
              <p className="text-gray-600 text-lg leading-relaxed">{step.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}