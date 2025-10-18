import os
from dotenv import load_dotenv
from chatbot import ChatbotManager
from topics import get_all_topics
import random

# Load environment variables
load_dotenv()

def test_chatbot():
    """Test the chatbot with a sample conversation."""
    
    # Check API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY not found!")
        print("Please create a .env file with your OpenAI API key.")
        return
    
    print("=================================")
    print("AI Chatbot - Backend Test")
    print("=================================\n")
    
    # Initialize chatbot
    chatbot = ChatbotManager()
    
    # Select random topic
    topics = get_all_topics()
    topic = random.choice(topics)
    
    print(f"Selected Topic: {topic}")
    print("-" * 50)
    
    # Start conversation
    initial_message = chatbot.start_conversation(topic)
    print(f"\n🤖 Bot: {initial_message}\n")
    
    # Simulate user responses
    sample_responses = [
        "Well, I think there are several important factors. For example, when it comes to the primary influences, I believe they all work together in complex ways.",
        "From my understanding, the environmental and systemic aspects play crucial roles. The way these elements interact determines the overall outcome.",
        "I'd also mention that timing and conditions matter a lot. Different scenarios require different approaches and considerations.",
        "There are also underlying mechanisms that aren't always obvious but significantly impact the results we see.",
        "In conclusion, it's really a combination of multiple factors working together that creates the full picture."
    ]
    
    # Conduct conversation
    for i, response in enumerate(sample_responses, 1):
        print(f"👤 You: {response}\n")
        
        bot_message, is_complete = chatbot.get_bot_response(response)
        print(f"🤖 Bot: {bot_message}\n")
        
        if is_complete:
            break
    
    # Get evaluation
    print("\n" + "=" * 50)
    print("EVALUATION RESULTS")
    print("=" * 50 + "\n")
    
    evaluation = chatbot.evaluate_and_score()
    
    print(f"Total Score: {evaluation['total_score']}/100\n")
    print(f"Breakdown:")
    print(f"  - Keyword Coverage: {evaluation['coverage_score']}/40")
    print(f"  - Contextual Relevance: {evaluation['relevance_score']}/40")
    print(f"  - Depth of Explanation: {evaluation['depth_score']}/20\n")
    
    print(f"Overall Feedback:")
    print(f"  {evaluation['overall_feedback']}\n")
    
    print("Keyword Analysis:")
    for keyword, analysis in evaluation['keyword_analysis'].items():
        status = "✅ Mentioned" if analysis['mentioned'] else "❌ Not mentioned"
        print(f"  - {keyword}: {status}")
        if analysis['mentioned']:
            print(f"    Relevance: {analysis['relevance_score']}/10")
        print(f"    Comment: {analysis['comment']}")
    
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    try:
        test_chatbot()
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

