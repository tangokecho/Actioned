import React from 'react';
import { ArrowRight } from 'lucide-react';
import { Button } from './ui/button';

const AboutSection = () => {
  return (
    <section className="bg-gradient-to-b from-[#0D1033] to-[#131a5c] py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left - Logos */}
          <div className="relative">
            <div className="flex items-center justify-center gap-8">
              {/* edX Logo */}
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/10">
                <div className="text-4xl font-bold text-white">edX</div>
              </div>
              
              {/* Connection */}
              <div className="flex items-center">
                <div className="w-8 h-0.5 bg-[#C92228]" />
                <div className="w-4 h-4 rounded-full bg-[#C92228]" />
                <div className="w-8 h-0.5 bg-[#C92228]" />
              </div>
              
              {/* Open edX Logo */}
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/10">
                <div className="flex items-center gap-2">
                  <svg className="w-10 h-10" viewBox="0 0 32 32" fill="none">
                    <circle cx="16" cy="16" r="12" stroke="#C92228" strokeWidth="3" />
                    <circle cx="16" cy="16" r="5" fill="#C92228" />
                  </svg>
                  <span className="text-2xl font-bold text-white">Open edX</span>
                </div>
              </div>
            </div>

            {/* Decorative elements */}
            <div className="absolute -top-10 -left-10 w-40 h-40 bg-[#C92228]/10 rounded-full blur-3xl" />
            <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-blue-500/10 rounded-full blur-3xl" />
          </div>

          {/* Right - Content */}
          <div>
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Two strong brands,{' '}
              <span className="text-[#C92228]">one shared vision.</span>
            </h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-6">
              edX is the online learning destination co-founded by Harvard and MIT. The Open edX platform provides the learner-centric, massively scalable learning technology behind it.
            </p>
            <p className="text-gray-400 leading-relaxed mb-8">
              Originally envisioned for MOOCs, Open edX platform has evolved into one of the leading learning solutions catering to Higher Ed, enterprise, and government organizations alike.
            </p>
            <Button
              variant="outline"
              className="border-2 border-white/30 text-white hover:bg-white/10 px-6 py-5 rounded-full font-medium transition-all duration-300 group"
            >
              More About Us
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
