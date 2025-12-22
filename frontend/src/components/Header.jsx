import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ChevronDown, Menu, X, Zap } from 'lucide-react';
import { navItems } from '../data/mockData';
import { Button } from './ui/button';

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState(null);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#0D0D0D] border-b border-[#2D2D2D]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3">
            {/* Actionuity Shield */}
            <div className="relative w-10 h-10">
              <div className="absolute inset-0 bg-gradient-to-br from-[#00FF44] to-[#00CC36] rounded-lg transform rotate-45" />
              <div className="absolute inset-1 bg-[#0D0D0D] rounded-md transform rotate-45" />
              <div className="absolute inset-0 flex items-center justify-center">
                <Zap className="w-5 h-5 text-[#00FF44]" />
              </div>
            </div>
            <div className="flex flex-col">
              <span className="text-white font-bold text-lg tracking-tight" style={{ fontFamily: 'Montserrat, sans-serif' }}>
                Action<span className="text-[#00FF44]">EDx</span>
              </span>
              <span className="text-[#4A4A4A] text-[10px] tracking-wider uppercase">Execute. Impact. Legacy.</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            {navItems.map((item, index) => (
              <div
                key={index}
                className="relative"
                onMouseEnter={() => item.submenu && setActiveDropdown(index)}
                onMouseLeave={() => setActiveDropdown(null)}
              >
                {item.submenu ? (
                  <button className="flex items-center gap-1 px-4 py-2 text-gray-400 hover:text-white transition-colors text-sm font-medium">
                    {item.title}
                    <ChevronDown className="w-4 h-4" />
                  </button>
                ) : (
                  <Link
                    to={item.link}
                    className="px-4 py-2 text-gray-400 hover:text-white transition-colors text-sm font-medium"
                  >
                    {item.title}
                  </Link>
                )}

                {/* Dropdown Menu */}
                {item.submenu && activeDropdown === index && (
                  <div className="absolute top-full left-0 mt-1 w-56 bg-[#1A1A1A] rounded-lg shadow-xl py-2 z-50 border border-[#2D2D2D]">
                    {item.submenu.map((subItem, subIndex) => (
                      <Link
                        key={subIndex}
                        to={subItem.link}
                        className="block px-4 py-2.5 text-gray-400 hover:bg-[#2D2D2D] hover:text-[#00FF44] transition-colors text-sm"
                      >
                        {subItem.title}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </nav>

          {/* Right Section */}
          <div className="hidden lg:flex items-center gap-4">
            <Link to="/login" className="text-gray-400 hover:text-white transition-colors text-sm font-medium">
              Sign In
            </Link>
            <Button
              className="bg-[#00FF44] hover:bg-[#00CC36] text-[#0D0D0D] px-5 py-2 rounded-lg text-sm font-bold transition-all duration-300 hover:shadow-lg hover:shadow-[#00FF44]/20"
            >
              Start Executing
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="lg:hidden text-white"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-[#0D0D0D] border-t border-[#2D2D2D]">
          <div className="px-4 py-4 space-y-3">
            {navItems.map((item, index) => (
              <div key={index}>
                {item.submenu ? (
                  <div>
                    <button
                      className="flex items-center justify-between w-full py-2 text-gray-400 text-sm font-medium"
                      onClick={() => setActiveDropdown(activeDropdown === index ? null : index)}
                    >
                      {item.title}
                      <ChevronDown className={`w-4 h-4 transition-transform ${activeDropdown === index ? 'rotate-180' : ''}`} />
                    </button>
                    {activeDropdown === index && (
                      <div className="pl-4 space-y-2 mt-2">
                        {item.submenu.map((subItem, subIndex) => (
                          <Link
                            key={subIndex}
                            to={subItem.link}
                            className="block py-1 text-gray-500 hover:text-[#00FF44] text-sm"
                            onClick={() => setMobileMenuOpen(false)}
                          >
                            {subItem.title}
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                ) : (
                  <Link
                    to={item.link}
                    className="block py-2 text-gray-400 text-sm font-medium"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    {item.title}
                  </Link>
                )}
              </div>
            ))}
            <div className="pt-4 space-y-3">
              <Link to="/login" className="block text-center text-gray-400 py-2 text-sm">
                Sign In
              </Link>
              <Button
                className="w-full bg-[#00FF44] hover:bg-[#00CC36] text-[#0D0D0D] py-2 rounded-lg text-sm font-bold"
              >
                Start Executing
              </Button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
