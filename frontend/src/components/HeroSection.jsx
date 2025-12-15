import React from 'react';
import { ArrowRight, Zap, Play } from 'lucide-react';
import { Button } from './ui/button';

const HeroSection = () => {
  return (
    <section className="relative bg-[#0D0D0D] pt-32 pb-24 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0">
        {/* Grid Pattern */}
        <div className="absolute inset-0 opacity-[0.03]" style={{
          backgroundImage: `linear-gradient(#00FF44 1px, transparent 1px), linear-gradient(90deg, #00FF44 1px, transparent 1px)`,
          backgroundSize: '60px 60px'
        }} />
        {/* Glow Effects */}
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-[#00FF44] rounded-full blur-[200px] opacity-10" />
        <div className="absolute bottom-20 right-1/4 w-96 h-96 bg-[#F2C84B] rounded-full blur-[200px] opacity-5" />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-[#1A1A1A] border border-[#2D2D2D] rounded-full px-4 py-2 mb-8">
            <Zap className="w-4 h-4 text-[#00FF44]" />
            <span className="text-gray-400 text-sm">From Idea → Impact → Legacy</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white leading-tight mb-6" style={{ fontFamily: 'Montserrat, sans-serif' }}>
            Where Learning Becomes{' '}
            <span className="relative">
              <span className="text-[#00FF44]">Execution</span>
              <svg className="absolute -bottom-2 left-0 w-full" height="8" viewBox="0 0 200 8" fill="none">
                <path d="M0 4C50 4 50 1 100 1C150 1 150 7 200 7" stroke="#00FF44" strokeWidth="2" />
              </svg>
            </span>
          </h1>

          {/* Subheadline */}
          <p className="text-lg md:text-xl text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed" style={{ fontFamily: 'Lato, sans-serif' }}>
            We don&apos;t just teach concepts—we provide the frameworks, tools, and community to immediately apply learning to measurable outcomes.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Button className="bg-[#00FF44] hover:bg-[#00CC36] text-[#0D0D0D] px-8 py-6 rounded-lg text-lg font-bold transition-all duration-300 hover:shadow-lg hover:shadow-[#00FF44]/30 group">
              Start Your 90-Day Track
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button variant="outline" className="border-2 border-[#2D2D2D] text-white hover:bg-[#1A1A1A] hover:border-[#00FF44] px-8 py-6 rounded-lg text-lg font-medium transition-all duration-300 group">
              <Play className="mr-2 w-5 h-5 text-[#00FF44]" />
              Watch How It Works
            </Button>
          </div>

          {/* Stats Row */}
          <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto">
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-[#00FF44] mb-1">90</div>
              <div className="text-gray-500 text-sm">Day Execution Tracks</div>
            </div>
            <div className="text-center border-x border-[#2D2D2D]">
              <div className="text-3xl md:text-4xl font-bold text-[#F2C84B] mb-1">3×</div>
              <div className="text-gray-500 text-sm">Faster Results</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-white mb-1">97%</div>
              <div className="text-gray-500 text-sm">Completion Rate</div>
            </div>
          </div>
        </div>

        {/* Command Center Preview */}
        <div className="mt-20 relative">
          <div className="absolute inset-0 bg-gradient-to-t from-[#0D0D0D] via-transparent to-transparent z-10 pointer-events-none" />
          <div className="bg-[#1A1A1A] rounded-2xl border border-[#2D2D2D] overflow-hidden shadow-2xl">
            {/* Browser Header */}
            <div className="flex items-center gap-2 px-4 py-3 border-b border-[#2D2D2D]">
              <div className="w-3 h-3 rounded-full bg-[#FF5F57]" />
              <div className="w-3 h-3 rounded-full bg-[#FFBD2E]" />
              <div className="w-3 h-3 rounded-full bg-[#28CA41]" />
              <div className="flex-1 ml-4 bg-[#0D0D0D] rounded-md h-6 flex items-center px-3">
                <span className="text-gray-500 text-xs">app.actionuity.com/command-center</span>
              </div>
            </div>
            
            {/* Dashboard Preview */}
            <div className="p-6 grid grid-cols-12 gap-4">
              {/* Sidebar */}
              <div className="col-span-3 space-y-4">
                <div className="bg-[#0D0D0D] rounded-lg p-4">
                  <div className="text-[#00FF44] text-xs font-bold mb-2">MISSION CONTROL</div>
                  <div className="space-y-2">
                    {['Dashboard', 'Skill Graph', 'Evidence Locker', 'Strategy Hub'].map((item, i) => (
                      <div key={i} className={`text-sm py-1.5 px-2 rounded ${i === 0 ? 'bg-[#00FF44]/10 text-[#00FF44]' : 'text-gray-500'}`}>
                        {item}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              
              {/* Main Content */}
              <div className="col-span-9 space-y-4">
                <div className="bg-[#0D0D0D] rounded-lg p-4">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-white font-bold">Current Track: Innovation Foundations</span>
                    <span className="text-[#00FF44] text-sm">Day 47 of 90</span>
                  </div>
                  <div className="h-2 bg-[#2D2D2D] rounded-full overflow-hidden">
                    <div className="h-full w-[52%] bg-gradient-to-r from-[#00FF44] to-[#00CC36] rounded-full" />
                  </div>
                  <div className="mt-4 p-3 bg-[#00FF44]/10 border border-[#00FF44]/30 rounded-lg">
                    <span className="text-[#00FF44] text-sm font-bold">NEXT LOGICAL STEP:</span>
                    <span className="text-gray-300 text-sm ml-2">Complete Field Operation Project Brief</span>
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-4">
                  {[{ label: 'Skills Unlocked', value: '12/18' }, { label: 'Projects Completed', value: '3' }, { label: 'Impact Score', value: '847' }].map((stat, i) => (
                    <div key={i} className="bg-[#0D0D0D] rounded-lg p-4 text-center">
                      <div className="text-2xl font-bold text-white">{stat.value}</div>
                      <div className="text-gray-500 text-xs">{stat.label}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
