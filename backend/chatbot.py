"""
AI-powered chatbot with conversation management and scoring logic.
"""

import os
import json
from openai import OpenAI
from topics import TOPICS, get_keywords_list


class ChatbotManager:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.conversation_history = []
        self.user_responses = []
        self.topic = None
        self.topic_data = None
        self.turn_count = 0
        self.max_turns = 5
        
    def start_conversation(self, topic):
        self.topic = topic
        self.topic_data = TOPICS[topic]
        self.conversation_history = []
        self.user_responses = []
        self.turn_count = 0
        
        system_prompt = f"""You are a curious and friendly journalist/interviewer conducting an interview. 
                        You are interested in learning about {topic}. Your goal is to engage the user in a natural conversation 
                        about this topic, asking follow-up questions based on their responses. Be conversational, enthusiastic, 
                        and genuinely curious. Keep your questions concise and engaging. You should conduct about {self.max_turns} 
                        exchanges before concluding the interview."""
        
        self.conversation_history.append({
            "role": "system",
            "content": system_prompt
        })
        
        initial_message = f"Hey! I've heard that you have some interesting insights about {topic}. Could you tell me more? What do you think has the biggest influence on it?"
        
        return initial_message
    
    def get_bot_response(self, user_message):
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        self.user_responses.append(user_message)
        self.turn_count += 1
        
        # Check if conversation should end
        if self.turn_count >= self.max_turns:
            final_message = "Thank you so much for sharing your insights! This has been really enlightening. I appreciate you taking the time to discuss this with me."
            self.conversation_history.append({
                "role": "assistant",
                "content": final_message
            })
            return final_message, True  # True indicates conversation is done
        
        # Get response from OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=0.7,
            max_tokens=200
        )
        
        bot_message = response.choices[0].message.content
        
        # Add bot response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": bot_message
        })
        
        return bot_message, False  # False indicates conversation continues
    
    def evaluate_and_score(self):
        """Evaluate user responses and calculate score with detailed breakdown."""
        # Combine all user responses
        full_transcript = "\n".join(self.user_responses)
        
        # Get keywords for the topic
        keywords = self.topic_data["keywords"]
        
        # Create evaluation prompt
        evaluation_prompt = f"""You are an expert evaluator analyzing a conversation about {self.topic}.

                            The conversation focused on these key concepts:
                            {json.dumps(keywords, indent=2)}

                            Here is the user's complete responses during the interview:
                            {full_transcript}

                            Please evaluate the user's responses based on:
                            1. Keyword Coverage (40 points): How many of the key concepts did they mention or discuss?
                            2. Contextual Relevance (40 points): How well did they use these concepts in context? Were they used meaningfully?
                            3. Depth of Explanation (20 points): How detailed and insightful were their explanations?

                            For each keyword, indicate:
                            - Whether it was mentioned (directly or indirectly)
                            - How relevant/appropriate the usage was
                            - A brief comment on their understanding

                            Provide your evaluation in the following JSON format:
                            {{
                                "keyword_analysis": {{
                                    "Keyword Name": {{
                                        "mentioned": true/false,
                                        "relevance_score": 0-10,
                                    "comment": "brief evaluation"
                                }},
                                ...
                            }},
                            "coverage_score": 0-40,
                            "relevance_score": 0-40,
                            "depth_score": 0-20,
                            "total_score": 0-100,
                            "overall_feedback": "A brief summary of the user's performance"
                        }}

                            Respond ONLY with valid JSON, no additional text."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert evaluator. Respond only with valid JSON."},
                {"role": "user", "content": evaluation_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        evaluation_text = response.choices[0].message.content
        
        # Parse JSON response
        try:
            # Try to extract JSON if there's any surrounding text
            start_idx = evaluation_text.find('{')
            end_idx = evaluation_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                evaluation_text = evaluation_text[start_idx:end_idx]
            
            evaluation = json.loads(evaluation_text)
        except json.JSONDecodeError as e:
            # Fallback if JSON parsing fails
            evaluation = {
                "keyword_analysis": {},
                "coverage_score": 20,
                "relevance_score": 20,
                "depth_score": 10,
                "total_score": 50,
                "overall_feedback": "Unable to parse evaluation. Please try again."
            }
        
        return evaluation

