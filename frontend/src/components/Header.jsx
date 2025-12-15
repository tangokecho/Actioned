import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ChevronDown, Menu, X, Search } from 'lucide-react';
import { navItems } from '../data/mockData';
import { Button } from './ui/button';

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState(null);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#0D1033] border-b border-[#1a1f4e]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="flex items-center">
              <svg className="w-8 h-8" viewBox="0 0 32 32" fill="none">
                <circle cx="16" cy="16" r="14" stroke="#C92228" strokeWidth="3" />
                <circle cx="16" cy="16" r="6" fill="#C92228" />
              </svg>
              <span className="ml-2 text-white font-bold text-xl">Open edX</span>
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
                  <button className="flex items-center gap-1 px-4 py-2 text-gray-300 hover:text-white transition-colors text-sm font-medium">
                    {item.title}
                    <ChevronDown className="w-4 h-4" />
                  </button>
                ) : (
                  <Link
                    to={item.link}
                    className="px-4 py-2 text-gray-300 hover:text-white transition-colors text-sm font-medium"
                  >
                    {item.title}
                  </Link>
                )}

                {/* Dropdown Menu */}
                {item.submenu && activeDropdown === index && (
                  <div className="absolute top-full left-0 mt-1 w-48 bg-white rounded-lg shadow-xl py-2 z-50">
                    {item.submenu.map((subItem, subIndex) => (
                      <Link
                        key={subIndex}
                        to={subItem.link}
                        className="block px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-[#C92228] transition-colors text-sm"
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
            <button className="text-gray-300 hover:text-white transition-colors">
              <Search className="w-5 h-5" />
            </button>
            <Button
              className="bg-[#C92228] hover:bg-[#a81d22] text-white px-5 py-2 rounded-full text-sm font-medium transition-all duration-300 hover:shadow-lg hover:shadow-red-500/20"
            >
              Get Started
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
        <div className="lg:hidden bg-[#0D1033] border-t border-[#1a1f4e]">
          <div className="px-4 py-4 space-y-3">
            {navItems.map((item, index) => (
              <div key={index}>
                {item.submenu ? (
                  <div>
                    <button
                      className="flex items-center justify-between w-full py-2 text-gray-300 text-sm font-medium"
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
                            className="block py-1 text-gray-400 hover:text-white text-sm"
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
                    className="block py-2 text-gray-300 text-sm font-medium"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    {item.title}
                  </Link>
                )}
              </div>
            ))}
            <Button
              className="w-full bg-[#C92228] hover:bg-[#a81d22] text-white py-2 rounded-full text-sm font-medium mt-4"
            >
              Get Started
            </Button>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
