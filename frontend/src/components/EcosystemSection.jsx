import React from 'react';
import { Wrench, Users, ArrowRight } from 'lucide-react';

const EcosystemSection = () => {
  const cards = [
    {
      icon: Wrench,
      title: 'Service & Technology Partners',
      description: 'Get started! Connect with 3rd-party tools and extensions to keep your LMS cutting-edge.',
      color: 'from-blue-500 to-blue-600',
      hoverColor: 'group-hover:from-blue-600 group-hover:to-blue-700'
    },
    {
      icon: Users,
      title: 'Community',
      description: 'Get involved! Help build and support new Open edX innovations.',
      color: 'from-purple-500 to-purple-600',
      hoverColor: 'group-hover:from-purple-600 group-hover:to-purple-700'
    }
  ];

  return (
    <section className="bg-gradient-to-b from-[#f8f9fc] to-white py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-[#0D1033] mb-4">
            Our vibrant global ecosystem
          </h2>
        </div>

        <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {cards.map((card, index) => {
            const Icon = card.icon;
            return (
              <div
                key={index}
                className="group relative bg-white rounded-2xl p-8 border border-gray-100 hover:border-transparent hover:shadow-2xl transition-all duration-500 cursor-pointer overflow-hidden"
              >
                {/* Background gradient on hover */}
                <div className={`absolute inset-0 bg-gradient-to-br ${card.color} opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />
                
                <div className="relative z-10">
                  <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${card.color} flex items-center justify-center mb-6 group-hover:bg-white/20 transition-colors duration-300`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-[#0D1033] group-hover:text-white mb-3 transition-colors duration-300">
                    {card.title}
                  </h3>
                  <p className="text-gray-600 group-hover:text-white/90 mb-4 transition-colors duration-300">
                    {card.description}
                  </p>
                  <div className="flex items-center text-[#C92228] group-hover:text-white font-medium transition-colors duration-300">
                    <span>Explore</span>
                    <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-2 transition-transform duration-300" />
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

export default EcosystemSection;
