import React from 'react';
import { platformFeatures } from '../data/mockData';
import { LayoutDashboard, GitBranch, Bot, Users, FolderLock, Lightbulb } from 'lucide-react';

const PlatformFeatures = () => {
  const iconMap = {
    LayoutDashboard,
    GitBranch,
    Bot,
    Users,
    FolderLock,
    Lightbulb
  };

  return (
    <section className="bg-[#1A1A1A] py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4" style={{ fontFamily: 'Montserrat, sans-serif' }}>
            The Actionuity <span className="text-[#00FF44]">Command Center</span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            More than a dashboard—your mission control for execution
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {platformFeatures.map((feature, index) => {
            const Icon = iconMap[feature.icon];
            return (
              <div
                key={index}
                className="group bg-[#0D0D0D] border border-[#2D2D2D] rounded-xl p-6 hover:border-[#00FF44]/30 transition-all duration-300 cursor-pointer"
              >
                <div className="w-12 h-12 bg-[#00FF44]/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-[#00FF44]/20 transition-colors">
                  <Icon className="w-6 h-6 text-[#00FF44]" />
                </div>
                <h3 className="text-white font-bold text-lg mb-2 group-hover:text-[#00FF44] transition-colors">
                  {feature.title}
                </h3>
                <p className="text-gray-400 text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>

        {/* Tri-Core Loop */}
        <div className="mt-20">
          <div className="text-center mb-12">
            <h3 className="text-2xl font-bold text-white mb-2">The Tri-Core Execution Loop</h3>
            <p className="text-gray-400">Embedded in every project workflow</p>
          </div>

          <div className="flex flex-col md:flex-row items-center justify-center gap-8">
            {[
              { name: 'GPT-5', role: 'Strategy', desc: 'AI-guided planning within assignments', color: '#00FF44' },
              { name: 'Codex', role: 'Build', desc: 'Integrated development environments', color: '#F2C84B' },
              { name: 'Agent', role: 'Deploy', desc: 'Simulated deployment/scaling exercises', color: '#00FF44' }
            ].map((core, i) => (
              <React.Fragment key={i}>
                <div className="text-center">
                  <div 
                    className="w-24 h-24 rounded-2xl flex items-center justify-center mb-4 mx-auto"
                    style={{ backgroundColor: `${core.color}15`, border: `2px solid ${core.color}30` }}
                  >
                    <span className="text-2xl font-bold" style={{ color: core.color }}>{core.role}</span>
                  </div>
                  <div className="text-white font-bold mb-1">{core.name}</div>
                  <div className="text-gray-500 text-sm max-w-[180px]">{core.desc}</div>
                </div>
                {i < 2 && (
                  <div className="hidden md:block w-16 h-0.5 bg-gradient-to-r from-[#00FF44] to-[#F2C84B]" />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default PlatformFeatures;
