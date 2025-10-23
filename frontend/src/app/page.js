import Image from "next/image";
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import UploadSection from './components/UploadSection';

import HowItWorksSection from './components/HowItWorksSection';
import CallToActionSection from './components/CallToActionSection';
import Footer from './components/Footer';

export default function Home() {
  return (
    <>
      <Header />
      <main>
        <HeroSection />
        <UploadSection />
        <HowItWorksSection />
        <CallToActionSection />
      </main>
      <Footer />
    </>
  );
}
