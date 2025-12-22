import React from 'react';
import { Link } from 'react-router-dom';
import { footerLinks, pillars } from '../data/mockData';
import { Zap, Twitter, Linkedin, Github, Youtube, ArrowRight } from 'lucide-react';
import { Button } from './ui/button';

const Footer = () => {
  return (
    <footer className="bg-[#0D0D0D] border-t border-[#2D2D2D]">
      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-gradient-to-r from-[#00FF44]/10 to-[#00FF44]/5 rounded-2xl p-8 md:p-12 border border-[#00FF44]/20 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4" style={{ fontFamily: 'Montserrat, sans-serif' }}>
            Ready to <span className="text-[#00FF44]">Execute</span>?
          </h2>
          <p className="text-gray-400 mb-8 max-w-2xl mx-auto">
            Just Execute It. No Plan B. Transform learning into action. Build portfolios, not just certificates. Create legacy through executed innovation.
          </p>
          <Button className="bg-[#00FF44] hover:bg-[#00CC36] text-[#0D0D0D] px-8 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:shadow-lg hover:shadow-[#00FF44]/30 group">
            Start Your 90-Day Track
            <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Button>
        </div>
      </div>

      {/* 9 Pillars */}
      <div className="border-t border-[#2D2D2D]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center mb-4">
            <span className="text-gray-500 text-xs uppercase tracking-wider">The 9-Pillar Framework</span>
          </div>
          <div className="flex flex-wrap justify-center gap-4">
            {pillars.map((pillar, i) => (
              <span key={i} className="text-gray-600 text-sm hover:text-[#00FF44] transition-colors cursor-default">
                {pillar}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Main Footer */}
      <div className="border-t border-[#2D2D2D]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-2 md:grid-cols-6 gap-8">
            {/* Logo & Description */}
            <div className="col-span-2">
              <Link to="/" className="flex items-center gap-3 mb-4">
                <div className="relative w-10 h-10">
                  <div className="absolute inset-0 bg-gradient-to-br from-[#00FF44] to-[#00CC36] rounded-lg transform rotate-45" />
                  <div className="absolute inset-1 bg-[#0D0D0D] rounded-md transform rotate-45" />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Zap className="w-5 h-5 text-[#00FF44]" />
                  </div>
                </div>
                <span className="text-white font-bold text-lg">
                  Action<span className="text-[#00FF44]">EDx</span>
                </span>
              </Link>
              <p className="text-gray-500 text-sm mb-6 max-w-xs">
                Where Learning Becomes Execution. From Idea → Impact → Legacy.
              </p>
              <div className="flex items-center gap-4">
                <a href="#" className="text-gray-500 hover:text-[#00FF44] transition-colors">
                  <Twitter className="w-5 h-5" />
                </a>
                <a href="#" className="text-gray-500 hover:text-[#00FF44] transition-colors">
                  <Linkedin className="w-5 h-5" />
                </a>
                <a href="#" className="text-gray-500 hover:text-[#00FF44] transition-colors">
                  <Github className="w-5 h-5" />
                </a>
                <a href="#" className="text-gray-500 hover:text-[#00FF44] transition-colors">
                  <Youtube className="w-5 h-5" />
                </a>
              </div>
            </div>

            {/* Platform Links */}
            <div>
              <h4 className="text-white font-semibold mb-4 text-sm">Platform</h4>
              <ul className="space-y-3">
                {footerLinks.platform.map((link, index) => (
                  <li key={index}>
                    <Link
                      to={link.link}
                      className="text-gray-500 hover:text-[#00FF44] text-sm transition-colors"
                    >
                      {link.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Community Links */}
            <div>
              <h4 className="text-white font-semibold mb-4 text-sm">Community</h4>
              <ul className="space-y-3">
                {footerLinks.community.map((link, index) => (
                  <li key={index}>
                    <Link
                      to={link.link}
                      className="text-gray-500 hover:text-[#00FF44] text-sm transition-colors"
                    >
                      {link.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Resources Links */}
            <div>
              <h4 className="text-white font-semibold mb-4 text-sm">Resources</h4>
              <ul className="space-y-3">
                {footerLinks.resources.map((link, index) => (
                  <li key={index}>
                    <Link
                      to={link.link}
                      className="text-gray-500 hover:text-[#00FF44] text-sm transition-colors"
                    >
                      {link.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Company Links */}
            <div>
              <h4 className="text-white font-semibold mb-4 text-sm">Company</h4>
              <ul className="space-y-3">
                {footerLinks.company.map((link, index) => (
                  <li key={index}>
                    <Link
                      to={link.link}
                      className="text-gray-500 hover:text-[#00FF44] text-sm transition-colors"
                    >
                      {link.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-[#2D2D2D]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-gray-600 text-sm">
              © {new Date().getFullYear()} Actionuity. All rights reserved.
            </p>
            <div className="flex items-center gap-6 text-sm">
              <Link to="/privacy" className="text-gray-500 hover:text-white transition-colors">Privacy</Link>
              <Link to="/terms" className="text-gray-500 hover:text-white transition-colors">Terms</Link>
              <Link to="/cookies" className="text-gray-500 hover:text-white transition-colors">Cookies</Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
