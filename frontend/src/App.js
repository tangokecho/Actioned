import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import HeroSection from "./components/HeroSection";
import ExecutionTrackSection from "./components/ExecutionTrackSection";
import TracksShowcase from "./components/TracksShowcase";
import PlatformFeatures from "./components/PlatformFeatures";
import Testimonials from "./components/Testimonials";
import PricingSection from "./components/PricingSection";
import Footer from "./components/Footer";

const HomePage = () => {
  return (
    <div className="min-h-screen bg-[#0D0D0D]">
      <Header />
      <main>
        <HeroSection />
        <ExecutionTrackSection />
        <TracksShowcase />
        <PlatformFeatures />
        <Testimonials />
        <PricingSection />
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
