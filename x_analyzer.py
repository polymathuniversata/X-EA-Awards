import tweepy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from typing import List, Dict, Tuple
import os
from dotenv import load_dotenv
import sys
from time import sleep
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

# Load environment variables
load_dotenv()

def print_progress(seconds_remaining):
    """Print a progress bar for rate limit waiting."""
    bar_length = 30
    filled_length = int(round(bar_length))
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rWaiting for rate limit: [{bar}] {seconds_remaining}s remaining')
    sys.stdout.flush()

class XAnalyzer:
    def __init__(self):
        # Initialize API credentials from environment variables
        self.client = tweepy.Client(
            bearer_token=os.getenv('BEARER_TOKEN'),
            consumer_key=os.getenv('API_KEY'),
            consumer_secret=os.getenv('API_KEY_SECRET'),
            access_token=os.getenv('ACCESS_TOKEN'),
            access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True
        )
        
        # Initialize AI model components
        self.scaler = MinMaxScaler()
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
        
        # Metric weights for ranking
        self.weights = {
            'engagement': 0.4,
            'intensity': 0.4,
            'followers': 0.2
        }
        
        # Influencer category thresholds
        self.categories = {
            'nano': (1000, 10000),
            'micro': (10000, 100000),
            'macro': (100000, float('inf'))
        }
        
        # East African countries and cities for strict filtering
        self.east_african_locations = {
            'tanzania': ['tanzania', 'dar es salaam', 'dodoma', 'arusha', 'mwanza', 'zanzibar', 'tz'],
            'kenya': ['kenya', 'nairobi', 'mombasa', 'kisumu', 'nakuru', 'ke'],
            'uganda': ['uganda', 'kampala', 'entebbe', 'jinja', 'gulu', 'ug'],
            'rwanda': ['rwanda', 'kigali', 'butare', 'gisenyi', 'rw'],
            'burundi': ['burundi', 'bujumbura', 'gitega', 'bi']
        }

    def get_influencer_category(self, followers: int) -> str:
        """Determine influencer category based on follower count."""
        for category, (min_followers, max_followers) in self.categories.items():
            if min_followers <= followers < max_followers:
                return category
        return 'nano'  # Default category

    def calculate_engagement_score(self, metrics: Dict) -> float:
        """Calculate normalized engagement score."""
        total_engagement = (
            metrics['like_count'] * 1.0 +
            metrics['retweet_count'] * 1.5 +
            metrics['reply_count'] * 2.0  # Weighted more as it requires more effort
        )
        return total_engagement

    def calculate_intensity_score(self, annual_posts: int, thread_count: int) -> float:
        """Calculate posting intensity score."""
        daily_avg = annual_posts / 365
        return (daily_avg * 0.7) + (thread_count * 0.3)  # Weight regular posts and threads

    def get_thread_count(self, user_id: str) -> int:
        """Count number of thread posts in recent tweets."""
        try:
            thread_count = 0
            prev_tweet_id = None
            
            for response in tweepy.Paginator(
                self.client.get_users_tweets,
                user_id,
                tweet_fields=['conversation_id', 'in_reply_to_user_id'],
                max_results=100,
                limit=5  # Look at recent 500 tweets max
            ):
                if not response.data:
                    break
                    
                for tweet in response.data:
                    # Check if tweet is part of a thread (self-reply)
                    if tweet.in_reply_to_user_id == user_id:
                        thread_count += 1
                        
            return thread_count
            
        except Exception as e:
            print(f"Error counting threads for user {user_id}: {str(e)}")
            return 0

    def calculate_ai_rank(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate AI-based ranking using multiple metrics."""
        if df.empty:
            return df
            
        # Prepare features for AI ranking
        features = pd.DataFrame()
        features['engagement_score'] = df.apply(
            lambda x: self.calculate_engagement_score(x['metrics']), axis=1
        )
        features['intensity_score'] = df.apply(
            lambda x: self.calculate_intensity_score(x['annual_posts'], x['thread_count']), axis=1
        )
        features['follower_score'] = df['followers_count'].apply(np.log1p)  # Log transform for better scaling
        
        # Normalize features
        features_scaled = self.scaler.fit_transform(features)
        
        # Train model on normalized features (using engagement as target for initial ranking)
        self.model.fit(features_scaled, features['engagement_score'])
        
        # Get feature importance and calculate final rank
        importance = self.model.feature_importances_
        df['ai_rank'] = self.model.predict(features_scaled)
        
        # Add influencer categories
        df['category'] = df['followers_count'].apply(self.get_influencer_category)
        
        return df.sort_values('ai_rank', ascending=False)

    def analyze_accounts(self, topic: str, max_pages: int = 25) -> pd.DataFrame:
        """Analyze X accounts with enhanced metrics and AI ranking."""
        accounts = []
        query = f"{topic} lang:en -is:retweet -is:reply"
        page_count = 0
        
        print(f"\nSearching for accounts related to '{topic}'...")
        print("This may take a while as we analyze metrics and verify locations.")
        
        while page_count < max_pages:
            try:
                for response in tweepy.Paginator(
                    self.client.search_recent_tweets,
                    query=query,
                    tweet_fields=['public_metrics', 'created_at', 'referenced_tweets', 'conversation_id'],
                    user_fields=['public_metrics', 'location', 'description', 'verified'],
                    expansions=['author_id'],
                    max_results=100,
                    limit=1
                ):
                    page_count += 1
                    print(f"Processing page {page_count}/{max_pages}...")
                    
                    if not response.data:
                        continue
                        
                    users = {u.id: u for u in response.includes['users']}
                    
                    for tweet in response.data:
                        if not self.is_original_post(tweet):
                            continue
                            
                        user = users[tweet.author_id]
                        
                        is_east_african, country = self.extract_location_info(user.location)
                        if not is_east_african:
                            continue
                            
                        annual_posts = self.get_user_timeline(user.id)
                        if annual_posts < 365:
                            continue
                            
                        thread_count = self.get_thread_count(user.id)
                        
                        account_info = {
                            'username': user.username,
                            'name': user.name,
                            'location': user.location,
                            'country': country,
                            'followers_count': user.public_metrics['followers_count'],
                            'following_count': user.public_metrics['following_count'],
                            'tweet_count': user.public_metrics['tweet_count'],
                            'annual_posts': annual_posts,
                            'thread_count': thread_count,
                            'metrics': tweet.public_metrics,
                            'verified': user.verified,
                            'description': user.description
                        }
                        
                        if not any(acc['username'] == user.username for acc in accounts):
                            accounts.append(account_info)
                            print(f"Found new account: @{user.username} from {user.location}")
                            print(f"  - Annual posts: {annual_posts}")
                            print(f"  - Threads: {thread_count}")
                            print(f"  - Country: {country.title()}")
                            
            except tweepy.TooManyRequests as e:
                reset_time = int(e.response.headers.get('x-rate-limit-reset', 0))
                self.handle_rate_limit(reset_time)
                continue
                
            except Exception as e:
                print(f"\nError occurred: {str(e)}")
                break
        
        if not accounts:
            return pd.DataFrame()
            
        # Create DataFrame and apply AI ranking
        df = pd.DataFrame(accounts)
        return self.calculate_ai_rank(df)
    
    def save_results(self, df: pd.DataFrame, topic: str) -> str:
        """Save results with enhanced metrics to CSV."""
        if df.empty:
            return None
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"{topic.replace(' ', '_')}_{timestamp}"
        
        os.makedirs('results', exist_ok=True)
        csv_path = os.path.join('results', f"{base_filename}.csv")
        
        # Prepare metrics for saving
        df['engagement_score'] = df.apply(
            lambda x: self.calculate_engagement_score(x['metrics']), axis=1
        )
        df['intensity_score'] = df.apply(
            lambda x: self.calculate_intensity_score(x['annual_posts'], x['thread_count']), axis=1
        )
        
        # Drop the raw metrics dictionary before saving
        df = df.drop('metrics', axis=1)
        df.to_csv(csv_path, index=False)
        
        return csv_path
            
    def get_top_accounts(self, df: pd.DataFrame, parameter: str, n: int = 10) -> pd.DataFrame:
        """Get top N accounts with enhanced metrics."""
        if df.empty or parameter not in df.columns:
            return None
            
        display_columns = [
            'username', 'name', 'location', 'country', parameter,
            'annual_posts', 'thread_count', 'category', 'verified'
        ]
        
        return df.nlargest(n, parameter)[display_columns] 