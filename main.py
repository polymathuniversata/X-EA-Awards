from x_analyzer import XAnalyzer
import sys

def display_menu():
    """Display the main menu options."""
    print("\n=== X Account Analyzer for East Africa ===")
    print("1. Analyze accounts by topic")
    print("2. View available parameters")
    print("3. View influencer categories")
    print("4. Exit")
    return input("\nSelect an option (1-4): ")

def display_parameters():
    """Display available parameters for analysis."""
    print("\nAvailable Parameters for Analysis:")
    print("1. ai_rank - Overall AI-based ranking score")
    print("2. engagement_score - Weighted engagement metrics")
    print("3. intensity_score - Posting frequency and thread creation")
    print("4. followers_count - Number of followers")
    print("5. annual_posts - Original posts in the past year")
    print("\nFiltering Criteria:")
    print("- Location: Must be in East Africa (Tanzania, Kenya, Uganda, Rwanda, Burundi)")
    print("- Activity: Minimum 365 original posts per year")
    print("- Content: Only original posts (not retweets/replies)")
    print("\nAI Ranking Weights:")
    print("- Engagement: 40% (likes, retweets, replies)")
    print("- Posting Intensity: 40% (frequency and threads)")
    print("- Follower Base: 20%")

def display_categories():
    """Display influencer categories and criteria."""
    print("\nInfluencer Categories:")
    print("\n1. Nano Influencers")
    print("   - Followers: 1K - 10K")
    print("   - Typically highly engaged with their community")
    print("   - Often focused on specific niches")
    
    print("\n2. Micro Influencers")
    print("   - Followers: 10K - 100K")
    print("   - Strong engagement rates")
    print("   - Growing authority in their field")
    
    print("\n3. Macro Influencers")
    print("   - Followers: 100K+")
    print("   - Wide reach and impact")
    print("   - Established authority")

def get_topic():
    """Get topic from user input."""
    while True:
        topic = input("\nEnter the topic to analyze (e.g., 'Tech Startups', 'Digital Artists'): ").strip()
        if topic:
            return topic
        print("Topic cannot be empty. Please try again.")

def format_number(num):
    """Format numbers for better readability."""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)

def format_score(score):
    """Format score values for display."""
    return f"{score:.2f}"

def main():
    analyzer = XAnalyzer()
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            # Get topic and analyze
            topic = get_topic()
            print(f"\nAnalyzing accounts related to '{topic}'...")
            print("This may take a while as we analyze metrics and verify locations.")
            print("Only accounts meeting all criteria will be shown.")
            
            # Perform analysis
            results_df = analyzer.analyze_accounts(topic)
            
            if results_df is not None and not results_df.empty:
                # First show overall AI rankings
                print("\n🏆 Top Accounts (AI-Ranked):")
                print("=" * 60)
                top_overall = analyzer.get_top_accounts(results_df, 'ai_rank')
                if top_overall is not None:
                    for _, account in top_overall.iterrows():
                        print(f"@{account['username']} ({account['name']})")
                        print(f"  📍 {account['location']} ({account['country'].title()})")
                        print(f"  🏅 Category: {account['category'].title()} Influencer")
                        print(f"  👥 Followers: {format_number(account['followers_count'])}")
                        print(f"  📊 Annual Posts: {format_number(account['annual_posts'])}")
                        print(f"  🧵 Threads: {account['thread_count']}")
                        if account['verified']:
                            print("  ✓ Verified account")
                        print()
                
                # Then show rankings by different metrics
                parameters = ['engagement_score', 'intensity_score', 'followers_count']
                for param in parameters:
                    print(f"\nTop accounts by {param}:")
                    print("=" * 60)
                    top_accounts = analyzer.get_top_accounts(results_df, param)
                    if top_accounts is not None:
                        for _, account in top_accounts.iterrows():
                            print(f"@{account['username']} ({account['name']})")
                            print(f"  📍 {account['location']} ({account['country'].title()})")
                            print(f"  🏅 {account['category'].title()} Influencer")
                            
                            # Format the parameter value
                            if param in ['followers_count', 'annual_posts']:
                                value = format_number(account[param])
                            else:
                                value = format_score(account[param])
                            
                            print(f"  {param}: {value}")
                            print(f"  📝 {format_number(account['annual_posts'])} posts/year")
                            print(f"  🧵 {account['thread_count']} threads")
                            if account['verified']:
                                print("  ✓ Verified account")
                            print()
                
                # Save results
                saved_file = analyzer.save_results(results_df, topic)
                if saved_file:
                    print(f"\n📁 Full results have been saved to: {saved_file}")
                    print("The CSV file contains additional metrics and details about each account.")
            else:
                print("\n❌ No accounts found matching the criteria.")
                print("\nPossible reasons:")
                print("1. No accounts from East Africa found for this topic")
                print("2. Found accounts don't meet the minimum 365 posts/year requirement")
                print("3. Found accounts mostly retweet/reply rather than post original content")
                print("\nTry:")
                print("- Using different search terms")
                print("- Broadening your topic")
                print("- Checking for spelling variations")
                
        elif choice == '2':
            display_parameters()
            
        elif choice == '3':
            display_categories()
            
        elif choice == '4':
            print("\nThank you for using X Account Analyzer!")
            sys.exit(0)
            
        else:
            print("\n❌ Invalid choice. Please select 1-4.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        sys.exit(1) 