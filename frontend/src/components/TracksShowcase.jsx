import React from 'react';
import { executionTracks } from '../data/mockData';
import { Clock, Users, TrendingUp, ArrowRight, Star } from 'lucide-react';
import { Button } from './ui/button';

const TracksShowcase = () => {
  return (
    <section className="bg-[#0D0D0D] py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end md:justify-between mb-12">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-2" style={{ fontFamily: 'Montserrat, sans-serif' }}>
              Execution Tracks
            </h2>
            <p className="text-gray-400">Choose your path to impact</p>
          </div>
          <button className="mt-4 md:mt-0 inline-flex items-center gap-2 text-[#00FF44] font-medium hover:gap-3 transition-all">
            View All Tracks
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Tracks Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {executionTracks.filter(t => t.featured).map((track) => (
            <div
              key={track.id}
              className="group bg-[#1A1A1A] border border-[#2D2D2D] rounded-xl overflow-hidden hover:border-[#00FF44]/50 transition-all duration-300"
            >
              {/* Track Header */}
              <div className="p-6 border-b border-[#2D2D2D]">
                <div className="flex items-start justify-between mb-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    track.level === 'Foundation' ? 'bg-[#00FF44]/10 text-[#00FF44]' :
                    track.level === 'Advanced' ? 'bg-[#F2C84B]/10 text-[#F2C84B]' :
                    'bg-purple-500/10 text-purple-400'
                  }`}>
                    {track.level}
                  </span>
                  <div className="flex items-center gap-1 text-[#F2C84B]">
                    <Star className="w-4 h-4 fill-current" />
                    <span className="text-sm">{track.completionRate}</span>
                  </div>
                </div>
                <h3 className="text-xl font-bold text-white mb-1 group-hover:text-[#00FF44] transition-colors">
                  {track.title}
                </h3>
                <p className="text-gray-500 text-sm">{track.subtitle}</p>
              </div>

              {/* Track Body */}
              <div className="p-6">
                <p className="text-gray-400 text-sm mb-6 leading-relaxed">
                  {track.description}
                </p>

                {/* Skills */}
                <div className="flex flex-wrap gap-2 mb-6">
                  {track.skills.map((skill, i) => (
                    <span key={i} className="px-2 py-1 bg-[#0D0D0D] text-gray-400 text-xs rounded">
                      {skill}
                    </span>
                  ))}
                </div>

                {/* Meta */}
                <div className="flex items-center gap-4 text-gray-500 text-sm mb-6">
                  <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    {track.duration}
                  </div>
                  <div className="flex items-center gap-1">
                    <Users className="w-4 h-4" />
                    {track.learners}
                  </div>
                </div>

                {/* CTA */}
                <Button className="w-full bg-[#2D2D2D] hover:bg-[#00FF44] text-white hover:text-[#0D0D0D] py-3 rounded-lg font-medium transition-all duration-300 group">
                  Start Track
                  <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 bg-gradient-to-r from-[#1A1A1A] to-[#2D2D2D] rounded-xl p-8 border border-[#2D2D2D]">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-[#F2C84B]/10 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-[#F2C84B]" />
              </div>
              <div>
                <h3 className="text-white font-bold text-lg">Quick Win Modules</h3>
                <p className="text-gray-400 text-sm">≤1 day effort for rapid skill acquisition</p>
              </div>
            </div>
            <Button variant="outline" className="border-[#F2C84B] text-[#F2C84B] hover:bg-[#F2C84B] hover:text-[#0D0D0D] px-6 py-3 rounded-lg font-medium">
              Explore Quick Wins
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TracksShowcase;
