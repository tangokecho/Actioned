import React from 'react';
import { ArrowRight } from 'lucide-react';
import { Button } from './ui/button';

const HeroSection = () => {
  return (
    <section className="relative bg-gradient-to-b from-[#0D1033] via-[#0f1445] to-[#131a5c] pt-32 pb-20 overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-10 w-72 h-72 bg-[#C92228] rounded-full blur-[120px]" />
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-blue-600 rounded-full blur-[150px]" />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="text-center lg:text-left">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white leading-tight mb-6">
              Deliver inspiring learning experiences{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#C92228] to-[#ff6b6b]">
                on any scale
              </span>
            </h1>
            <p className="text-lg md:text-xl text-gray-300 mb-8 max-w-xl mx-auto lg:mx-0">
              Enable online campuses, instructor-led courses, degree programs, and self-paced courses using a single platform.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Button className="bg-[#C92228] hover:bg-[#a81d22] text-white px-8 py-6 rounded-full text-lg font-medium transition-all duration-300 hover:shadow-lg hover:shadow-red-500/30 group">
                Get Started
                <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button variant="outline" className="border-2 border-white/30 text-white hover:bg-white/10 px-8 py-6 rounded-full text-lg font-medium transition-all duration-300">
                Learn More
              </Button>
            </div>
          </div>

          {/* Right Illustration */}
          <div className="relative">
            <div className="relative z-10">
              {/* Main illustration - stylized learning platform mockup */}
              <div className="bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-sm rounded-3xl p-6 border border-white/10">
                <div className="bg-[#1a1f4e] rounded-2xl p-4">
                  {/* Browser Header */}
                  <div className="flex items-center gap-2 mb-4">
                    <div className="w-3 h-3 rounded-full bg-red-500" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500" />
                    <div className="w-3 h-3 rounded-full bg-green-500" />
                    <div className="flex-1 bg-[#0D1033] rounded-full h-6 ml-4" />
                  </div>
                  
                  {/* Content Preview */}
                  <div className="space-y-4">
                    <div className="bg-gradient-to-r from-[#C92228]/20 to-[#ff6b6b]/20 rounded-xl p-4">
                      <div className="w-16 h-2 bg-[#C92228] rounded mb-2" />
                      <div className="w-32 h-2 bg-white/30 rounded" />
                    </div>
                    <div className="grid grid-cols-3 gap-3">
                      {[1, 2, 3].map((i) => (
                        <div key={i} className="bg-[#0D1033] rounded-lg p-3">
                          <div className="w-full h-12 bg-gradient-to-br from-blue-500/30 to-purple-500/30 rounded mb-2" />
                          <div className="w-full h-2 bg-white/20 rounded mb-1" />
                          <div className="w-2/3 h-2 bg-white/10 rounded" />
                        </div>
                      ))}
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="flex-1 h-2 bg-[#C92228] rounded-full" style={{ width: '70%' }} />
                      <span className="text-white/60 text-xs">70%</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Floating Elements */}
              <div className="absolute -top-4 -right-4 bg-green-500 text-white px-4 py-2 rounded-full text-sm font-medium shadow-lg animate-bounce">
                100M+ Learners
              </div>
              <div className="absolute -bottom-4 -left-4 bg-white/10 backdrop-blur-sm border border-white/20 text-white px-4 py-2 rounded-full text-sm shadow-lg">
                53 Languages
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
