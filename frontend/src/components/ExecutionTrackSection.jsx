import React from 'react';
import { executionPhases } from '../data/mockData';
import { BookOpen, Target, Rocket, Award, ArrowRight } from 'lucide-react';

const ExecutionTrackSection = () => {
  const iconMap = {
    BookOpen,
    Target,
    Rocket,
    Award
  };

  return (
    <section className="bg-[#0D0D0D] py-24 border-t border-[#2D2D2D]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 bg-[#1A1A1A] border border-[#2D2D2D] rounded-full px-4 py-2 mb-6">
            <span className="text-[#F2C84B] text-sm font-medium">The Execution Model</span>
          </div>
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-4" style={{ fontFamily: 'Montserrat, sans-serif' }}>
            90 Days from{' '}
            <span className="text-[#00FF44]">Idea</span> to{' '}
            <span className="text-[#F2C84B]">Impact</span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Every track follows our proven 4-phase execution methodology
          </p>
        </div>

        {/* Timeline */}
        <div className="relative">
          {/* Connection Line */}
          <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-[#00FF44] via-[#F2C84B] to-[#00FF44] transform -translate-y-1/2" />

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {executionPhases.map((phase, index) => {
              const Icon = iconMap[phase.icon];
              return (
                <div key={index} className="relative group">
                  <div className="bg-[#1A1A1A] border border-[#2D2D2D] rounded-xl p-6 h-full transition-all duration-300 hover:border-[#00FF44]/50 hover:shadow-lg hover:shadow-[#00FF44]/5">
                    {/* Phase Badge */}
                    <div className="flex items-center gap-3 mb-4">
                      <div 
                        className="w-12 h-12 rounded-lg flex items-center justify-center"
                        style={{ backgroundColor: `${phase.color}20` }}
                      >
                        <Icon className="w-6 h-6" style={{ color: phase.color }} />
                      </div>
                      <div>
                        <div className="text-xs font-bold tracking-wider" style={{ color: phase.color }}>
                          {phase.phase}
                        </div>
                        <div className="text-gray-500 text-xs">{phase.days}</div>
                      </div>
                    </div>

                    <h3 className="text-white font-bold text-lg mb-2">{phase.title}</h3>
                    <p className="text-gray-400 text-sm leading-relaxed">{phase.description}</p>

                    {/* Arrow for larger screens */}
                    {index < 3 && (
                      <div className="hidden lg:flex absolute -right-3 top-1/2 transform -translate-y-1/2 z-10">
                        <div className="w-6 h-6 bg-[#0D0D0D] rounded-full flex items-center justify-center border border-[#2D2D2D]">
                          <ArrowRight className="w-3 h-3 text-[#00FF44]" />
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="mt-16 text-center">
          <p className="text-gray-400 mb-6">
            <span className="text-[#00FF44] font-bold">No traditional exams.</span>{' '}
            Grading based on executed projects with real-world outcomes.
          </p>
          <button className="inline-flex items-center gap-2 text-[#00FF44] font-medium hover:gap-3 transition-all">
            Explore All Execution Tracks
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </section>
  );
};

export default ExecutionTrackSection;
