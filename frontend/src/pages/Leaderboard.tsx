import React, { useState } from 'react';
import { Tab } from '@headlessui/react';

interface Influencer {
  username: string;
  name: string;
  category: string;
  country: string;
  followers: number;
  engagement: number;
  posts: number;
  verified: boolean;
}

const Leaderboard: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sortBy, setSortBy] = useState('engagement');

  // Sample data
  const influencers: Influencer[] = [
    {
      username: 'techboss',
      name: 'Tech Boss',
      category: 'micro',
      country: 'Tanzania',
      followers: 25000,
      engagement: 4.8,
      posts: 450,
      verified: true,
    },
    // Add more sample data
  ];

  const categories = ['all', 'nano', 'micro', 'macro'];
  const sortOptions = [
    { value: 'engagement', label: 'Engagement Rate' },
    { value: 'followers', label: 'Followers' },
    { value: 'posts', label: 'Post Count' },
  ];

  const formatNumber = (num: number): string => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Leaderboard
        </h1>
        <div className="flex space-x-4">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200"
          >
            {sortOptions.map((option) => (
              <option key={option.value} value={option.value}>
                Sort by {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <Tab.Group>
        <Tab.List className="flex space-x-1 rounded-xl bg-primary-900/20 p-1">
          {categories.map((category) => (
            <Tab
              key={category}
              className={({ selected }: { selected: boolean }) =>
                `w-full rounded-lg py-2.5 text-sm font-medium leading-5
                ${
                  selected
                    ? 'bg-white dark:bg-gray-800 text-primary-700 dark:text-primary-400 shadow'
                    : 'text-gray-700 dark:text-gray-400 hover:bg-white/[0.12] hover:text-primary-600'
                }`
              }
              onClick={() => setSelectedCategory(category)}
            >
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </Tab>
          ))}
        </Tab.List>

        <Tab.Panels>
          {categories.map((category) => (
            <Tab.Panel
              key={category}
              className="rounded-xl bg-white dark:bg-gray-800 p-3"
            >
              <div className="space-y-4">
                {influencers
                  .filter(
                    (inf) =>
                      category === 'all' || inf.category === category.toLowerCase()
                  )
                  .map((influencer, idx) => (
                    <div
                      key={influencer.username}
                      className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
                    >
                      <div className="flex items-center space-x-4">
                        <span className="text-2xl font-bold text-primary-600 dark:text-primary-400 w-8">
                          #{idx + 1}
                        </span>
                        <div>
                          <div className="flex items-center">
                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                              @{influencer.username}
                            </h3>
                            {influencer.verified && (
                              <span className="ml-2 text-primary-600 dark:text-primary-400">
                                ✓
                              </span>
                            )}
                          </div>
                          <p className="text-gray-500 dark:text-gray-400">
                            {influencer.name} • {influencer.country}
                          </p>
                        </div>
                      </div>
                      <div className="flex space-x-8">
                        <div className="text-center">
                          <p className="text-sm text-gray-500 dark:text-gray-400">
                            Followers
                          </p>
                          <p className="text-lg font-semibold text-gray-900 dark:text-white">
                            {formatNumber(influencer.followers)}
                          </p>
                        </div>
                        <div className="text-center">
                          <p className="text-sm text-gray-500 dark:text-gray-400">
                            Engagement
                          </p>
                          <p className="text-lg font-semibold text-gray-900 dark:text-white">
                            {influencer.engagement}%
                          </p>
                        </div>
                        <div className="text-center">
                          <p className="text-sm text-gray-500 dark:text-gray-400">
                            Posts
                          </p>
                          <p className="text-lg font-semibold text-gray-900 dark:text-white">
                            {formatNumber(influencer.posts)}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            </Tab.Panel>
          ))}
        </Tab.Panels>
      </Tab.Group>
    </div>
  );
};

export default Leaderboard; 