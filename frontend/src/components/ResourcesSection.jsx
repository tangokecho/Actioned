import React from 'react';
import { blogPosts } from '../data/mockData';
import { ArrowRight, Calendar } from 'lucide-react';

const ResourcesSection = () => {
  return (
    <section className="bg-white py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-[#0D1033]">
            Resources
          </h2>
          <a
            href="/blog"
            className="hidden sm:flex items-center text-[#C92228] font-medium hover:underline group"
          >
            View all posts
            <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </a>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {blogPosts.map((post) => (
            <article
              key={post.id}
              className="group bg-white rounded-2xl border border-gray-100 overflow-hidden hover:shadow-xl hover:shadow-gray-200/50 transition-all duration-300 hover:-translate-y-1"
            >
              {/* Card Header with gradient */}
              <div className="h-3 bg-gradient-to-r from-[#C92228] to-[#ff6b6b]" />
              
              <div className="p-6">
                <div className="flex items-center gap-2 text-gray-400 text-sm mb-3">
                  <Calendar className="w-4 h-4" />
                  <span>{post.date}</span>
                </div>
                <h3 className="text-lg font-bold text-[#0D1033] mb-3 group-hover:text-[#C92228] transition-colors duration-300 line-clamp-2">
                  {post.title}
                </h3>
                <p className="text-gray-500 text-sm line-clamp-3 mb-4">
                  {post.excerpt}
                </p>
                <a
                  href={post.link}
                  className="inline-flex items-center text-[#C92228] font-medium text-sm hover:underline group/link"
                >
                  Read more
                  <ArrowRight className="ml-1 w-4 h-4 group-hover/link:translate-x-1 transition-transform" />
                </a>
              </div>
            </article>
          ))}
        </div>

        <div className="text-center mt-8 sm:hidden">
          <a
            href="/blog"
            className="inline-flex items-center text-[#C92228] font-medium hover:underline group"
          >
            View all posts
            <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </a>
        </div>
      </div>
    </section>
  );
};

export default ResourcesSection;
