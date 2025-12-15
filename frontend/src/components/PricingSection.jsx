import React from 'react';
import { pricingTiers } from '../data/mockData';
import { Check, Zap } from 'lucide-react';
import { Button } from './ui/button';

const PricingSection = () => {
  return (
    <section className="bg-[#1A1A1A] py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4" style={{ fontFamily: 'Montserrat, sans-serif' }}>
            Invest in <span className="text-[#00FF44]">Execution</span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Premium but accessible. Justified by faster, measurable results.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {pricingTiers.map((tier, index) => (
            <div
              key={index}
              className={`relative bg-[#0D0D0D] rounded-xl overflow-hidden transition-all duration-300 ${
                tier.highlighted 
                  ? 'border-2 border-[#00FF44] shadow-lg shadow-[#00FF44]/10' 
                  : 'border border-[#2D2D2D] hover:border-[#2D2D2D]'
              }`}
            >
              {/* Highlighted Badge */}
              {tier.highlighted && (
                <div className="absolute top-0 left-0 right-0 bg-[#00FF44] text-[#0D0D0D] text-center py-2 text-sm font-bold">
                  <Zap className="w-4 h-4 inline mr-1" />
                  MOST POPULAR
                </div>
              )}

              <div className={`p-6 ${tier.highlighted ? 'pt-14' : ''}`}>
                {/* Tier Name */}
                <h3 className="text-xl font-bold text-white mb-2">{tier.name}</h3>
                <p className="text-gray-500 text-sm mb-6">{tier.description}</p>

                {/* Price */}
                <div className="mb-6">
                  <span className="text-4xl font-bold text-white">{tier.price}</span>
                  <span className="text-gray-500 text-sm">{tier.period}</span>
                </div>

                {/* Features */}
                <ul className="space-y-3 mb-8">
                  {tier.features.map((feature, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <div className="w-5 h-5 rounded-full bg-[#00FF44]/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <Check className="w-3 h-3 text-[#00FF44]" />
                      </div>
                      <span className="text-gray-400 text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>

                {/* CTA */}
                <Button
                  className={`w-full py-3 rounded-lg font-medium transition-all duration-300 ${
                    tier.highlighted
                      ? 'bg-[#00FF44] hover:bg-[#00CC36] text-[#0D0D0D]'
                      : 'bg-[#2D2D2D] hover:bg-[#3D3D3D] text-white'
                  }`}
                >
                  {tier.cta}
                </Button>
              </div>
            </div>
          ))}
        </div>

        {/* Enterprise CTA */}
        <div className="mt-12 text-center">
          <p className="text-gray-400 mb-4">Need custom deployment for your team?</p>
          <button className="text-[#F2C84B] font-medium hover:underline">
            Contact us for Enterprise pricing →
          </button>
        </div>
      </div>
    </section>
  );
};

export default PricingSection;
