import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import HeroSection from "./components/HeroSection";
import TrustedBy from "./components/TrustedBy";
import StatsSection from "./components/StatsSection";
import EcosystemSection from "./components/EcosystemSection";
import FeaturesSection from "./components/FeaturesSection";
import AboutSection from "./components/AboutSection";
import ResourcesSection from "./components/ResourcesSection";
import Footer from "./components/Footer";

const HomePage = () => {
  return (
    <div className="min-h-screen">
      <Header />
      <main>
        <HeroSection />
        <TrustedBy />
        <StatsSection />
        <EcosystemSection />
        <FeaturesSection />
        <AboutSection />
        <ResourcesSection />
      </main>
      <Footer />
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="*" element={<HomePage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
