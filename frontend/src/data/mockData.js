// ActionEDx Mock Data
// "Where Learning Becomes Execution"

export const brandConfig = {
  name: 'ActionEDx',
  tagline: 'Where Learning Becomes Execution',
  brandPromise: "We don't just teach concepts—we provide the frameworks, tools, and community to immediately apply learning to measurable outcomes.",
  colors: {
    graphiteBlack: '#0D0D0D',
    ingenuityGreen: '#00FF44',
    legacyGold: '#F2C84B',
    darkGray: '#1A1A1A',
    mediumGray: '#2D2D2D',
    lightGray: '#4A4A4A'
  }
};

export const navItems = [
  {
    title: 'Execution Tracks',
    submenu: [
      { title: 'Browse All Tracks', link: '/tracks' },
      { title: 'Innovation Foundations', link: '/tracks/innovation' },
      { title: 'AI Action Officer', link: '/tracks/ai-officer' },
      { title: 'GreenBid Bootcamp', link: '/tracks/greenbid' }
    ]
  },
  {
    title: 'Platform',
    submenu: [
      { title: 'Command Center', link: '/dashboard' },
      { title: 'Skill Graph', link: '/skills' },
      { title: 'Strategy Hub', link: '/strategy-hub' },
      { title: 'Crew Quarters', link: '/crews' }
    ]
  },
  {
    title: 'Community',
    submenu: [
      { title: 'Wednesday Wins', link: '/community/wins' },
      { title: 'Expert Network', link: '/community/experts' },
      { title: 'Hackathons', link: '/community/hackathons' }
    ]
  },
  {
    title: 'Enterprise',
    link: '/enterprise'
  },
  {
    title: 'Pricing',
    link: '/pricing'
  }
];

export const stats = [
  { value: '90', label: 'Day Execution Tracks', description: 'Complete innovation cycles from idea to impact' },
  { value: '3×', label: 'Faster Results', description: 'Implementation speed vs traditional learning' },
  { value: '10K+', label: 'Executed Projects', description: 'Real-world outcomes, not just certificates' },
  { value: '97%', label: 'Completion Rate', description: 'Action-driven learning keeps learners engaged' },
  { value: '500+', label: 'Expert Network', description: 'Access to Action Officers and strategists' },
  { value: '$2.4M', label: 'Learner Revenue', description: 'Generated through Money-in-30 projects' }
];

export const executionPhases = [
  {
    phase: 'BRIEFING',
    days: 'Days 1-15',
    title: 'Theory + Framework',
    description: 'Micro-lessons introducing Actionuity IP, AI Innovation Assistant audits, Master Ledger setup',
    icon: 'BookOpen',
    color: '#00FF44'
  },
  {
    phase: 'DRILLS',
    days: 'Days 16-45',
    title: 'Guided Practice',
    description: 'Interactive sandboxes, real tools, QC AUDIT checkpoints for self-assessment',
    icon: 'Target',
    color: '#F2C84B'
  },
  {
    phase: 'FIELD OPERATION',
    days: 'Days 46-75',
    title: 'Real Application',
    description: 'Mandatory projects, Crew collaboration, Money-in-30 focus for immediate revenue',
    icon: 'Rocket',
    color: '#00FF44'
  },
  {
    phase: 'DEBRIEF',
    days: 'Days 76-90',
    title: 'Integration & Legacy',
    description: 'House of Hearts peer review, portfolio compilation, verifiable credentials',
    icon: 'Award',
    color: '#F2C84B'
  }
];

export const executionTracks = [
  {
    id: 1,
    title: 'Innovation Execution Foundations',
    subtitle: 'Ultimate Business Strategy Framework',
    description: 'Master the 9-Pillar Framework and Tri-Core Loop to transform ideas into measurable impact.',
    duration: '90 Days',
    level: 'Foundation',
    learners: '2,450',
    completionRate: '94%',
    skills: ['Strategic Thinking', 'Framework Application', 'Impact Measurement'],
    featured: true
  },
  {
    id: 2,
    title: 'AI Action Officer Certification',
    subtitle: 'GPT-5 Strategy Integration',
    description: 'Become certified to deploy AI-powered strategy tools within the Actionuity ecosystem.',
    duration: '90 Days',
    level: 'Advanced',
    learners: '1,890',
    completionRate: '91%',
    skills: ['AI Strategy', 'Prompt Engineering', 'Automation'],
    featured: true
  },
  {
    id: 3,
    title: 'GreenBid Bootcamp',
    subtitle: 'Government Contracting Mastery',
    description: 'Navigate government procurement with proven frameworks and templates.',
    duration: '90 Days',
    level: 'Specialized',
    learners: '1,120',
    completionRate: '96%',
    skills: ['Proposal Writing', 'Compliance', 'Contract Management'],
    featured: false
  },
  {
    id: 4,
    title: 'Youth Energy Entrepreneurship',
    subtitle: 'Next-Gen Innovators',
    description: 'Adapted execution track for young entrepreneurs aged 16-24.',
    duration: '90 Days',
    level: 'Foundation',
    learners: '3,200',
    completionRate: '89%',
    skills: ['Business Basics', 'Innovation Mindset', 'First Revenue'],
    featured: false
  },
  {
    id: 5,
    title: 'House of Hearts Leadership',
    subtitle: 'Courage, Compassion, Accountability',
    description: 'Develop leadership skills through the House of Hearts framework.',
    duration: '90 Days',
    level: 'Leadership',
    learners: '1,650',
    completionRate: '97%',
    skills: ['Emotional Intelligence', 'Team Leadership', 'Ethical Decision Making'],
    featured: true
  }
];

export const platformFeatures = [
  {
    title: 'Mission Control',
    description: 'Your command center showing active Execution Tracks with NEXT LOGICAL STEP highlighted.',
    icon: 'LayoutDashboard'
  },
  {
    title: 'Skill Graph',
    description: 'Visual mapping of your competencies aligned with the 10-alities framework.',
    icon: 'GitBranch'
  },
  {
    title: 'Action Officer Hub',
    description: 'Access AI Action Officers-as-a-Service for real-time strategy guidance.',
    icon: 'Bot'
  },
  {
    title: 'Crew Quarters',
    description: 'Team workspaces with shared tools for collaborative execution.',
    icon: 'Users'
  },
  {
    title: 'Evidence Locker',
    description: 'Your personal Master Ledger of all projects and verifiable outcomes.',
    icon: 'FolderLock'
  },
  {
    title: 'Strategy Hub',
    description: 'Crowdsourced strategies you can fork, remix, and deploy.',
    icon: 'Lightbulb'
  }
];

export const pricingTiers = [
  {
    name: 'Explorer',
    price: 'Free',
    period: '',
    description: 'Start your execution journey',
    features: [
      'Access to Briefing phases',
      'Community forums',
      'Basic Skill Graph',
      'Limited AI Assistant access',
      '1 Quick Win module/month'
    ],
    cta: 'Start Free',
    highlighted: false
  },
  {
    name: 'Executor',
    price: '$99',
    period: '/month',
    description: 'Full track access for serious learners',
    features: [
      'Unlimited Execution Tracks',
      'Full AI Innovation Assistant',
      'Basic credentials',
      'Crew collaboration',
      'Weekly Office Hours',
      'Evidence Locker'
    ],
    cta: 'Start Executing',
    highlighted: true
  },
  {
    name: 'Innovator',
    price: '$299',
    period: '/month',
    description: 'Premium access for impact creators',
    features: [
      'Everything in Executor',
      'NFT credentials',
      'Strategy Hub publishing',
      'Priority expert access',
      'Quarterly hackathons',
      'Royalty Badges eligibility',
      'PriorityScore analytics'
    ],
    cta: 'Become Innovator',
    highlighted: false
  }
];

export const testimonials = [
  {
    name: 'Marcus Chen',
    role: 'AI Action Officer Graduate',
    quote: 'In 90 days, I went from learning about AI to deploying a strategy tool that now serves 200+ clients. This is not learning—this is launching.',
    metric: '$45K revenue in first quarter'
  },
  {
    name: 'Sarah Okonkwo',
    role: 'GreenBid Bootcamp Alumni',
    quote: 'The execution-driven approach meant I won my first government contract before completing the track. The frameworks are that practical.',
    metric: '$180K contract won'
  },
  {
    name: 'David Park',
    role: 'Innovation Foundations Graduate',
    quote: 'The difference between this and other platforms? I have a portfolio of executed projects, not just a certificate.',
    metric: '3 products launched'
  }
];

export const footerLinks = {
  platform: [
    { title: 'Execution Tracks', link: '/tracks' },
    { title: 'Command Center', link: '/dashboard' },
    { title: 'Strategy Hub', link: '/strategy-hub' },
    { title: 'Credentials', link: '/credentials' }
  ],
  community: [
    { title: 'Wednesday Wins', link: '/community/wins' },
    { title: 'Expert Network', link: '/experts' },
    { title: 'Hackathons', link: '/hackathons' },
    { title: 'Crew Finder', link: '/crews' }
  ],
  resources: [
    { title: 'Documentation', link: '/docs' },
    { title: 'API Access', link: '/api' },
    { title: 'Brand Guidelines', link: '/brand' },
    { title: 'Support', link: '/support' }
  ],
  company: [
    { title: 'About Actionuity', link: '/about' },
    { title: 'Enterprise', link: '/enterprise' },
    { title: 'Careers', link: '/careers' },
    { title: 'Contact', link: '/contact' }
  ]
};

export const pillars = [
  'Clarity', 'Speed', 'Ingenuity', 'Discipline', 'Ethics',
  'Resilience', 'Collaboration', 'Innovation', 'Legacy'
];
