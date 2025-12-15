import React from 'react';

const TrustedBy = () => {
  // Using text-based logos for reliability
  const logos = [
    { name: 'edX', style: 'font-bold text-2xl' },
    { name: 'IBM', style: 'font-bold text-2xl tracking-widest' },
    { name: 'Microsoft', style: 'font-semibold text-xl' },
    { name: 'MIT', style: 'font-bold text-2xl tracking-wide' },
    { name: 'Harvard', style: 'font-serif text-xl italic' },
    { name: 'XuetangX', style: 'font-semibold text-xl' }
  ];

  return (
    <section className="bg-[#0D1033] py-12 border-t border-b border-[#1a1f4e]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p className="text-center text-gray-400 text-sm font-medium mb-8 uppercase tracking-wider">
          Trusted by top organizations worldwide
        </p>
        <div className="flex flex-wrap items-center justify-center gap-8 md:gap-12 lg:gap-16">
          {logos.map((logo, index) => (
            <div
              key={index}
              className="text-white/60 hover:text-white transition-all duration-300 cursor-pointer hover:scale-110"
            >
              <span className={logo.style}>{logo.name}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TrustedBy;
