import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { footerLinks, languages } from '../data/mockData';
import { ChevronDown, Twitter, Linkedin, Youtube, Github } from 'lucide-react';

const Footer = () => {
  const [languageOpen, setLanguageOpen] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState(languages[0]);

  return (
    <footer className="bg-[#0D1033]">
      {/* CTA Banner */}
      <div className="border-b border-[#1a1f4e]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="bg-gradient-to-r from-[#C92228]/20 to-[#ff6b6b]/20 rounded-2xl p-8 md:p-12 text-center backdrop-blur-sm border border-[#C92228]/20">
            <h3 className="text-2xl md:text-3xl font-bold text-white mb-4">
              Join the Open edX Conference 2026!
            </h3>
            <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
              The 2026 Open edX Conference will present innovative use cases for one of the world's best open source online learning management systems.
            </p>
            <a
              href="#register"
              className="inline-flex items-center bg-[#C92228] hover:bg-[#a81d22] text-white px-8 py-3 rounded-full font-medium transition-all duration-300 hover:shadow-lg hover:shadow-red-500/30"
            >
              Register Now
            </a>
          </div>
        </div>
      </div>

      {/* Main Footer */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8">
          {/* Logo & Description */}
          <div className="col-span-2 md:col-span-1">
            <Link to="/" className="flex items-center gap-2 mb-4">
              <svg className="w-8 h-8" viewBox="0 0 32 32" fill="none">
                <circle cx="16" cy="16" r="14" stroke="#C92228" strokeWidth="3" />
                <circle cx="16" cy="16" r="6" fill="#C92228" />
              </svg>
              <span className="text-white font-bold text-xl">Open edX</span>
            </Link>
            <p className="text-gray-400 text-sm mb-6">
              Delivering inspiring learning experiences on any scale.
            </p>
            
            {/* Social Links */}
            <div className="flex items-center gap-4">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <Youtube className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <Github className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Platform Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Platform</h4>
            <ul className="space-y-3">
              {footerLinks.platform.map((link, index) => (
                <li key={index}>
                  <Link
                    to={link.link}
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                  >
                    {link.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Community Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Community</h4>
            <ul className="space-y-3">
              {footerLinks.community.map((link, index) => (
                <li key={index}>
                  <Link
                    to={link.link}
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                  >
                    {link.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Resources</h4>
            <ul className="space-y-3">
              {footerLinks.resources.map((link, index) => (
                <li key={index}>
                  <Link
                    to={link.link}
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                  >
                    {link.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Company</h4>
            <ul className="space-y-3">
              {footerLinks.company.map((link, index) => (
                <li key={index}>
                  <Link
                    to={link.link}
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                  >
                    {link.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-[#1a1f4e]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-gray-400 text-sm">
              © {new Date().getFullYear()} Open edX. All rights reserved.
            </p>

            {/* Language Selector */}
            <div className="relative">
              <button
                className="flex items-center gap-2 text-gray-400 hover:text-white text-sm transition-colors px-4 py-2 rounded-lg border border-[#1a1f4e] hover:border-white/20"
                onClick={() => setLanguageOpen(!languageOpen)}
              >
                <span>{selectedLanguage.name}</span>
                <ChevronDown className={`w-4 h-4 transition-transform ${languageOpen ? 'rotate-180' : ''}`} />
              </button>

              {languageOpen && (
                <div className="absolute bottom-full left-0 mb-2 w-48 bg-[#1a1f4e] rounded-lg shadow-xl py-2 z-50">
                  {languages.map((lang) => (
                    <button
                      key={lang.code}
                      className={`w-full text-left px-4 py-2 text-sm transition-colors ${
                        selectedLanguage.code === lang.code
                          ? 'text-[#C92228] bg-white/5'
                          : 'text-gray-300 hover:text-white hover:bg-white/5'
                      }`}
                      onClick={() => {
                        setSelectedLanguage(lang);
                        setLanguageOpen(false);
                      }}
                    >
                      {lang.name}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
