// Mock data for Open edX clone

export const trustedLogos = [
  { name: 'edX', logo: 'https://www.edx.org/images/logos/edx-logo-elm.svg' },
  { name: 'IBM', logo: 'https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg' },
  { name: 'Microsoft', logo: 'https://upload.wikimedia.org/wikipedia/commons/9/96/Microsoft_logo_%282012%29.svg' },
  { name: 'MIT', logo: 'https://upload.wikimedia.org/wikipedia/commons/0/0c/MIT_logo.svg' },
  { name: 'Harvard', logo: 'https://upload.wikimedia.org/wikipedia/commons/c/cc/Harvard_University_coat_of_arms.svg' },
  { name: 'XuetangX', logo: 'https://www.xuetangx.com/static/images/logo.png' }
];

export const stats = [
  { value: '70K+', label: 'Courses', description: '70K+ courses are deployed by Open edX sites around the world' },
  { value: '53', label: 'Languages supported', description: 'The Open edX platform supports 53 different languages' },
  { value: '100M+', label: 'Learners', description: '100M+ learners use Open edX to develop in-demand skills and earn new credentials' },
  { value: '99.96%', label: 'Availability', description: 'The edX site, powered by Open edX, achieves 99.96% availability' },
  { value: '9 of 10', label: 'Top Universities', description: "Of the Times Higher Education World University Report's Top 10 universities, 9 use Open edX" },
  { value: '20+', label: 'Gov/NGOs', description: 'In addition to university consortiums, 20+ governments and NGOs trust the Open edX platform to deliver education on a national scale.' }
];

export const ecosystemCards = [
  {
    icon: 'Wrench',
    title: 'Service & Technology Partners',
    description: 'Get started! Connect with 3rd-party tools and extensions to keep your LMS cutting-edge.',
    link: '/marketplace'
  },
  {
    icon: 'Users',
    title: 'Community',
    description: 'Get involved! Help build and support new Open edX innovations.',
    link: '/community'
  }
];

export const features = [
  {
    category: 'Empower learners and instructors',
    items: [
      'Advanced learner and Instructor dashboards',
      'Interactive forums and discussion boards',
      'Live video conferencing'
    ]
  },
  {
    category: 'Cross-device / cross-platform',
    items: [
      'Works on any device',
      'Seamlessly integrates with third party tools and extensions such as Salesforce'
    ]
  },
  {
    category: 'Extensible and inclusive',
    items: [
      'Customizable and easy to use',
      'Create your own learning platform in minutes',
      'Use on-premise or in the cloud',
      'Single tenant or multi-tenant'
    ]
  },
  {
    category: 'Rich authoring experience',
    items: [
      'Interactive content with adaptive video streaming',
      'Multimedia, animation, and simulation',
      'AR, VR, and more'
    ]
  },
  {
    category: 'Intelligent analytics',
    items: [
      'Dashboards with near real-time data analysis',
      'Insights for course teams',
      'Extensive data collection for learning researchers & instructors'
    ]
  }
];

export const navItems = [
  {
    title: 'The Platform',
    submenu: [
      { title: 'Overview', link: '/platform' },
      { title: 'Features', link: '/features' },
      { title: 'Releases', link: '/releases' }
    ]
  },
  {
    title: 'Community',
    submenu: [
      { title: 'Overview', link: '/community' },
      { title: 'Contributors', link: '/contributors' },
      { title: 'Events', link: '/events' }
    ]
  },
  {
    title: 'Marketplace',
    link: '/marketplace'
  },
  {
    title: 'About',
    submenu: [
      { title: 'About Open edX', link: '/about' },
      { title: 'Team', link: '/team' },
      { title: 'Careers', link: '/careers' }
    ]
  },
  {
    title: 'Blog',
    link: '/blog'
  }
];

export const blogPosts = [
  {
    id: 1,
    title: 'Presenting at the Open edX Conference 2026 – Call for Speakers!',
    excerpt: 'The Open edX Conference 2026 will provide in-depth and interactive presentations, ranging from keynotes to...',
    date: 'June 15, 2025',
    link: '/blog/conference-2026-speakers'
  },
  {
    id: 2,
    title: 'How NASA Scaled Open Science Education to 20,000 Researchers with the Open edX Platform',
    excerpt: 'When NASA set out to democratize open science practices across the global research community, they...',
    date: 'June 10, 2025',
    link: '/blog/nasa-open-science'
  },
  {
    id: 3,
    title: 'Voting Is Now Open for the Open edX TOC Community Representatives!',
    excerpt: 'The moment has arrived! Voting is now live for the Open edX Technical Oversight Committee...',
    date: 'June 5, 2025',
    link: '/blog/toc-voting'
  },
  {
    id: 4,
    title: 'Join Us for the Open edX Conference 2026!',
    excerpt: 'We are excited to announce that Western Governors University (WGU) will be hosting the Open...',
    date: 'May 28, 2025',
    link: '/blog/conference-2026'
  }
];

export const footerLinks = {
  platform: [
    { title: 'Overview', link: '/platform' },
    { title: 'Features', link: '/features' },
    { title: 'Releases', link: '/releases' },
    { title: 'Demo', link: '/demo' }
  ],
  community: [
    { title: 'Overview', link: '/community' },
    { title: 'Contributors', link: '/contributors' },
    { title: 'Events', link: '/events' },
    { title: 'Forum', link: '/forum' }
  ],
  resources: [
    { title: 'Documentation', link: '/docs' },
    { title: 'Blog', link: '/blog' },
    { title: 'Case Studies', link: '/case-studies' },
    { title: 'Support', link: '/support' }
  ],
  company: [
    { title: 'About', link: '/about' },
    { title: 'Careers', link: '/careers' },
    { title: 'Contact', link: '/contact' },
    { title: 'Privacy Policy', link: '/privacy' }
  ]
};

export const languages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'es', name: 'Spanish', flag: '🇪🇸' },
  { code: 'fr', name: 'French', flag: '🇫🇷' },
  { code: 'de', name: 'German', flag: '🇩🇪' },
  { code: 'pt', name: 'Portuguese', flag: '🇵🇹' },
  { code: 'it', name: 'Italian', flag: '🇮🇹' },
  { code: 'ar', name: 'Arabic', flag: '🇸🇦' },
  { code: 'zh', name: 'Chinese', flag: '🇨🇳' },
  { code: 'uk', name: 'Ukrainian', flag: '🇺🇦' }
];

export const courses = [
  {
    id: 1,
    title: 'Introduction to Computer Science',
    institution: 'Harvard University',
    image: 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400&h=225&fit=crop',
    rating: 4.8,
    learners: '3.2M',
    duration: '12 weeks',
    level: 'Introductory'
  },
  {
    id: 2,
    title: 'Data Science Fundamentals',
    institution: 'MIT',
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=225&fit=crop',
    rating: 4.7,
    learners: '1.8M',
    duration: '8 weeks',
    level: 'Intermediate'
  },
  {
    id: 3,
    title: 'Machine Learning Basics',
    institution: 'Stanford University',
    image: 'https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=400&h=225&fit=crop',
    rating: 4.9,
    learners: '2.5M',
    duration: '10 weeks',
    level: 'Intermediate'
  },
  {
    id: 4,
    title: 'Digital Marketing Strategy',
    institution: 'University of Edinburgh',
    image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=225&fit=crop',
    rating: 4.6,
    learners: '890K',
    duration: '6 weeks',
    level: 'Beginner'
  }
];
