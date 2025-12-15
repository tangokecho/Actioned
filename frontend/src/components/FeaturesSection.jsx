import React from 'react';
import { features } from '../data/mockData';
import { Check, Monitor, Puzzle, Video, BarChart3, ArrowRight } from 'lucide-react';
import { Button } from './ui/button';

const FeaturesSection = () => {
  const iconMap = {
    0: Monitor,
    1: Monitor,
    2: Puzzle,
    3: Video,
    4: BarChart3
  };

  return (
    <section className="bg-white py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-4">
          <p className="text-gray-500 text-lg max-w-3xl mx-auto">
            Easily and confidently scale from supporting small learning to{' '}
            <span className="text-[#0D1033] font-semibold">
              thousands of simultaneous learners.
            </span>
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 items-start mt-16">
          {/* Left Side - Features List */}
          <div className="space-y-8">
            {features.slice(0, 3).map((feature, index) => {
              const Icon = iconMap[index];
              return (
                <div key={index} className="group">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-xl bg-[#0D1033] flex items-center justify-center flex-shrink-0 group-hover:bg-[#C92228] transition-colors duration-300">
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-[#0D1033] mb-3">
                        {feature.category}
                      </h3>
                      <ul className="space-y-2">
                        {feature.items.map((item, itemIndex) => (
                          <li key={itemIndex} className="flex items-start gap-2 text-gray-600">
                            <Check className="w-5 h-5 text-[#C92228] flex-shrink-0 mt-0.5" />
                            <span>{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Right Side - Illustration */}
          <div className="relative">
            <div className="bg-gradient-to-br from-[#f8f9fc] to-white rounded-3xl p-8 border border-gray-100">
              <div className="aspect-square relative">
                {/* Decorative circles */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 border-2 border-dashed border-gray-200 rounded-full" />
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 border-2 border-dashed border-[#C92228]/20 rounded-full" />
                
                {/* Central element */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-24 bg-gradient-to-br from-[#C92228] to-[#ff6b6b] rounded-2xl flex items-center justify-center shadow-lg shadow-red-500/30">
                  <svg className="w-12 h-12 text-white" viewBox="0 0 32 32" fill="none">
                    <circle cx="16" cy="16" r="10" stroke="currentColor" strokeWidth="2" />
                    <circle cx="16" cy="16" r="4" fill="currentColor" />
                  </svg>
                </div>

                {/* Floating icons */}
                <div className="absolute top-4 left-4 w-16 h-16 bg-white rounded-xl shadow-lg flex items-center justify-center animate-pulse">
                  <Monitor className="w-8 h-8 text-blue-500" />
                </div>
                <div className="absolute top-4 right-4 w-16 h-16 bg-white rounded-xl shadow-lg flex items-center justify-center animate-pulse delay-100">
                  <Puzzle className="w-8 h-8 text-purple-500" />
                </div>
                <div className="absolute bottom-4 left-4 w-16 h-16 bg-white rounded-xl shadow-lg flex items-center justify-center animate-pulse delay-200">
                  <Video className="w-8 h-8 text-green-500" />
                </div>
                <div className="absolute bottom-4 right-4 w-16 h-16 bg-white rounded-xl shadow-lg flex items-center justify-center animate-pulse delay-300">
                  <BarChart3 className="w-8 h-8 text-orange-500" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Features */}
        <div className="grid md:grid-cols-2 gap-8 mt-16 pt-16 border-t border-gray-100">
          {features.slice(3, 5).map((feature, index) => {
            const Icon = iconMap[index + 3];
            return (
              <div key={index} className="group">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-xl bg-[#0D1033] flex items-center justify-center flex-shrink-0 group-hover:bg-[#C92228] transition-colors duration-300">
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-[#0D1033] mb-3">
                      {feature.category}
                    </h3>
                    <ul className="space-y-2">
                      {feature.items.map((item, itemIndex) => (
                        <li key={itemIndex} className="flex items-start gap-2 text-gray-600">
                          <Check className="w-5 h-5 text-[#C92228] flex-shrink-0 mt-0.5" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="text-center mt-12">
          <Button className="bg-[#C92228] hover:bg-[#a81d22] text-white px-8 py-6 rounded-full text-lg font-medium transition-all duration-300 hover:shadow-lg hover:shadow-red-500/30 group">
            Get Started
            <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Button>
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
