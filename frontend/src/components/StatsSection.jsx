import React from 'react';
import { stats } from '../data/mockData';
import { BookOpen, Globe, Users, CheckCircle, GraduationCap, Building } from 'lucide-react';

const StatsSection = () => {
  const iconMap = {
    0: BookOpen,
    1: Globe,
    2: Users,
    3: CheckCircle,
    4: GraduationCap,
    5: Building
  };

  return (
    <section className="bg-white py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-[#0D1033] mb-4">
            Over 100 million{' '}
            <span className="text-[#C92228]">learners reached</span>
          </h2>
          <p className="text-gray-600 text-lg">Open edX project by the numbers</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-6 lg:gap-8">
          {stats.map((stat, index) => {
            const Icon = iconMap[index];
            return (
              <div
                key={index}
                className="group bg-gradient-to-br from-gray-50 to-white p-6 lg:p-8 rounded-2xl border border-gray-100 hover:border-[#C92228]/30 hover:shadow-xl hover:shadow-red-500/5 transition-all duration-300"
              >
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-xl bg-[#C92228]/10 flex items-center justify-center group-hover:bg-[#C92228] transition-colors duration-300">
                    <Icon className="w-6 h-6 text-[#C92228] group-hover:text-white transition-colors duration-300" />
                  </div>
                  <div>
                    <div className="text-3xl lg:text-4xl font-bold text-[#0D1033] mb-1">
                      {stat.value}
                    </div>
                    <div className="text-[#C92228] font-semibold mb-2">{stat.label}</div>
                    <p className="text-gray-500 text-sm leading-relaxed">{stat.description}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default StatsSection;
