import React from 'react';
import { testimonials } from '../data/mockData';
import { Quote, TrendingUp } from 'lucide-react';

const Testimonials = () => {
  return (
    <section className="bg-[#0D0D0D] py-24 border-t border-[#2D2D2D]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4" style={{ fontFamily: 'Montserrat, sans-serif' }}>
            Real Results from Real{' '}
            <span className="text-[#F2C84B]">Executors</span>
          </h2>
          <p className="text-gray-400 text-lg">
            Not just testimonials—verified outcomes with measurable impact
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className="bg-[#1A1A1A] border border-[#2D2D2D] rounded-xl p-6 relative group hover:border-[#00FF44]/30 transition-all duration-300"
            >
              {/* Quote Icon */}
              <div className="absolute top-6 right-6 text-[#2D2D2D] group-hover:text-[#00FF44]/20 transition-colors">
                <Quote className="w-8 h-8" />
              </div>

              {/* Quote */}
              <p className="text-gray-300 text-sm leading-relaxed mb-6 pr-8">
                "{testimonial.quote}"
              </p>

              {/* Metric Badge */}
              <div className="inline-flex items-center gap-2 bg-[#00FF44]/10 border border-[#00FF44]/30 rounded-full px-4 py-2 mb-6">
                <TrendingUp className="w-4 h-4 text-[#00FF44]" />
                <span className="text-[#00FF44] text-sm font-medium">{testimonial.metric}</span>
              </div>

              {/* Author */}
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#00FF44] to-[#00CC36] flex items-center justify-center">
                  <span className="text-[#0D0D0D] font-bold text-sm">
                    {testimonial.name.split(' ').map(n => n[0]).join('')}
                  </span>
                </div>
                <div>
                  <div className="text-white font-medium text-sm">{testimonial.name}</div>
                  <div className="text-gray-500 text-xs">{testimonial.role}</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Stats Banner */}
        <div className="mt-16 bg-gradient-to-r from-[#00FF44]/10 to-[#F2C84B]/10 rounded-xl p-8 border border-[#2D2D2D]">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { value: '$2.4M', label: 'Learner Revenue Generated' },
              { value: '10K+', label: 'Projects Executed' },
              { value: '500+', label: 'Companies Started' },
              { value: '89', label: 'Countries Reached' }
            ].map((stat, i) => (
              <div key={i} className="text-center">
                <div className="text-2xl md:text-3xl font-bold text-white mb-1">{stat.value}</div>
                <div className="text-gray-400 text-sm">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
