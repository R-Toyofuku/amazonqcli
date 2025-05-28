#!/usr/bin/env python3
"""
AWS Quiz Game - Japanese Names Edition
A quiz game where AWS services are represented as fictional Japanese full names.
"""
import pygame
import sys
import random
import os
import math
from typing import List, Tuple, Dict, Optional

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED = (255, 99, 71)
BLUE = (70, 130, 180)
LIGHT_BLUE = (173, 216, 230)
GRAY = (220, 220, 220)
LIGHT_GREEN = (230, 255, 230)
LIGHT_RED = (255, 230, 230)
GOLD = (255, 215, 0)
FONT_SIZE = 32
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60
BUTTON_MARGIN = 20
PROGRESS_BAR_HEIGHT = 20

# Quiz questions - each entry contains:
# - Japanese full name (surname + given name)
# - Correct AWS service
# - Incorrect AWS service (similar but wrong)
# - Optional explanation of the metaphorical connection
QUIZ_QUESTIONS = [
    {
        "name": "高橋 龍",
        "correct": "Amazon EC2",
        "incorrect": "Amazon Lightsail",
        "explanation": "高橋 (Takahashi) means 'high bridge', representing the connection to the cloud. 龍 (Ryu) means 'dragon', symbolizing EC2's powerful computing capabilities."
    },
    {
        "name": "水野 清",
        "correct": "Amazon RDS",
        "incorrect": "Amazon DynamoDB",
        "explanation": "水野 (Mizuno) contains 水 (water), while 清 (Sei) means 'clear/pure', representing how RDS handles data flow like a well-managed stream of information."
    },
    {
        "name": "雲井 保",
        "correct": "Amazon S3",
        "incorrect": "Amazon EBS",
        "explanation": "雲井 (Kumoi) contains 雲 (cloud), and 保 (Tamotsu) means 'to protect/preserve', representing S3's role in securely storing data in the cloud."
    },
    {
        "name": "早河 道",
        "correct": "Amazon CloudFront",
        "incorrect": "Amazon Route 53",
        "explanation": "早河 (Hayakawa) contains 早 (fast) and 河 (river), while 道 (Michi) means 'path/road', representing CloudFront's fast content delivery network."
    },
    {
        "name": "監物 晴",
        "correct": "Amazon CloudWatch",
        "incorrect": "AWS Config",
        "explanation": "監物 (Kenmotsu) contains 監 (supervise), and 晴 (Haru) means 'clear/bright', representing CloudWatch's monitoring capabilities that provide clear insights."
    },
    {
        "name": "壁川 守",
        "correct": "AWS WAF",
        "incorrect": "AWS Shield",
        "explanation": "壁川 (Kabekawa) contains 壁 (wall), and 守 (Mamoru) means 'to protect', representing WAF's role as a web application firewall that guards against threats."
    },
    {
        "name": "氷室 永",
        "correct": "Amazon Glacier",
        "incorrect": "AWS Backup",
        "explanation": "氷室 (Himuro) means 'ice room', and 永 (Hisashi) means 'eternal/long-lasting', representing Glacier's long-term cold storage capabilities."
    },
    {
        "name": "関 計",
        "correct": "AWS Lambda",
        "incorrect": "AWS Fargate",
        "explanation": "関 (Seki) means 'related/connection', and 計 (Kei) means 'calculate/measure', representing Lambda's function-based serverless computing."
    },
    {
        "name": "智野 探",
        "correct": "Amazon Athena",
        "incorrect": "Amazon Redshift",
        "explanation": "智野 (Tomono) contains 智 (wisdom), and 探 (Sagasu) means 'to search/explore', representing Athena's intelligent query service named after the Greek goddess of wisdom."
    },
    {
        "name": "桜井 器",
        "correct": "Amazon ECS",
        "incorrect": "Amazon EKS",
        "explanation": "桜井 (Sakurai) is a common Japanese surname, while 器 (Utsuwa) means 'container', representing Amazon ECS (Elastic Container Service)."
    },
    {
        "name": "森 賢",
        "correct": "Amazon SageMaker",
        "incorrect": "Amazon Comprehend",
        "explanation": "森 (Mori) means 'forest', and 賢 (Ken) means 'wisdom/intelligence', representing SageMaker's role in bringing wisdom (sage) and creating value from data forests."
    },
    {
        "name": "大野 無",
        "correct": "Amazon Aurora",
        "incorrect": "Amazon Neptune",
        "explanation": "大野 (Ohno) means 'big field', and 無 (Mu) means 'nothingness/infinity', representing Aurora's vast scalability and performance capabilities."
    },
    {
        "name": "渡辺 信",
        "correct": "Amazon SNS",
        "incorrect": "Amazon SQS",
        "explanation": "渡辺 (Watanabe) contains 渡 (to cross/transmit), and 信 (Shin) means 'message/trust', representing SNS's role in message transmission and notifications."
    },
    {
        "name": "鍵山 秘",
        "correct": "AWS KMS",
        "incorrect": "AWS Secrets Manager",
        "explanation": "鍵山 (Kagiyama) contains 鍵 (key), and 秘 (Hi) means 'secret', representing KMS's role in key management and encryption."
    },
    {
        "name": "橋本 連",
        "correct": "AWS Step Functions",
        "incorrect": "AWS AppFlow",
        "explanation": "橋本 (Hashimoto) contains 橋 (bridge), and 連 (Ren) means 'connect/link', representing Step Functions' role in coordinating multiple AWS services."
    },
    {
        "name": "小川 流",
        "correct": "Amazon Kinesis",
        "incorrect": "Amazon MSK",
        "explanation": "小川 (Ogawa) means 'small river', and 流 (Ryu) means 'flow/stream', representing Kinesis's role in real-time data streaming."
    },
    {
        "name": "山田 索",
        "correct": "Amazon Elasticsearch",
        "incorrect": "Amazon CloudSearch",
        "explanation": "山田 (Yamada) is a common Japanese surname, and 索 (Saku) means 'search', representing Elasticsearch's powerful search capabilities."
    },
    {
        "name": "石川 築",
        "correct": "AWS CloudFormation",
        "incorrect": "AWS CDK",
        "explanation": "石川 (Ishikawa) contains 石 (stone), and 築 (Chiku) means 'build/construct', representing CloudFormation's role in building infrastructure."
    }
]

class Button:
    """Button class for creating interactive buttons."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY
        self.text_color = BLACK
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button on the screen."""
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)  # Button border
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        """Check if the button is clicked."""
        return self.rect.collidepoint(pos)


class QuizGame:
    """Main quiz game class."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AWS 人名クイズ")
        
        # Set up fonts with better size for title
        self.setup_fonts()
        
        # Adjust font size for title to ensure it fits
        self.title_font = pygame.font.SysFont(self.font_name, FONT_SIZE + 5)
        
        # Get all available questions
        self.all_questions = QUIZ_QUESTIONS.copy()
        
        # Select 5 random questions
        self.select_random_questions()
        
        self.current_question_index = 0
        self.score = 0
        
        self.buttons = []
        self.next_button = None
        self.feedback_text = ""
        self.feedback_color = BLACK
        self.explanation_text = ""
        self.show_feedback = False
        self.background_color = WHITE
        
        # Celebration effects
        self.celebration_particles = []
        self.celebration_active = False
        self.celebration_start_time = 0
        self.celebration_duration = 3000  # 3 seconds in milliseconds
        
        # Try to load sound effects
        self.setup_sounds()
        
        self.setup_question()
    
    def select_random_questions(self):
        """Select 5 random questions from all available questions."""
        # Make a copy of all questions
        questions_pool = self.all_questions.copy()
        random.shuffle(questions_pool)
        
        # Select the first 5 questions
        self.questions = questions_pool[:5]
        self.total_questions = len(self.questions)
    
    def setup_fonts(self):
        """Set up fonts with Japanese support."""
        # Try to find a Japanese font
        japanese_fonts = [
            'Yu Gothic', 'MS Gothic', 'Meiryo', 'Noto Sans CJK JP', 
            'Hiragino Sans GB', 'Arial Unicode MS', 'NanumGothic'
        ]
        
        # Check if any Japanese fonts are available
        available_fonts = pygame.font.get_fonts()
        font_found = False
        self.font_name = None
        
        for font_name in japanese_fonts:
            # Check for partial matches in available fonts
            for available_font in available_fonts:
                if font_name.lower() in available_font.lower():
                    self.font_name = available_font
                    self.font_large = pygame.font.SysFont(available_font, FONT_SIZE + 10)
                    self.font_medium = pygame.font.SysFont(available_font, FONT_SIZE)
                    self.font_small = pygame.font.SysFont(available_font, FONT_SIZE - 10)
                    font_found = True
                    print(f"Using font: {available_font}")
                    break
            
            if font_found:
                break
        
        # If no Japanese font found, try to use the default font
        if not font_found:
            try:
                # Try to use a system font that might support Japanese
                self.font_name = None
                self.font_large = pygame.font.SysFont(None, FONT_SIZE + 10)
                self.font_medium = pygame.font.SysFont(None, FONT_SIZE)
                self.font_small = pygame.font.SysFont(None, FONT_SIZE - 10)
                print("Using default font. Japanese characters may not display correctly.")
            except Exception as e:
                print(f"Error setting up fonts: {e}")
                # Last resort: use the default font
                self.font_large = pygame.font.Font(None, FONT_SIZE + 10)
                self.font_medium = pygame.font.Font(None, FONT_SIZE)
                self.font_small = pygame.font.Font(None, FONT_SIZE - 10)
    
    def setup_sounds(self):
        """Set up sound effects."""
        self.sound_available = False
        try:
            # Create simple sound files if they don't exist
            if not os.path.exists("correct.wav") and not os.path.exists("incorrect.wav"):
                try:
                    import numpy as np
                    from scipy.io import wavfile
                    
                    # Create a simple "correct" sound (higher frequency)
                    sample_rate = 44100
                    duration = 0.5
                    t = np.linspace(0, duration, int(sample_rate * duration))
                    correct_data = np.sin(2 * np.pi * 880 * t) * 0.5
                    wavfile.write("correct.wav", sample_rate, correct_data.astype(np.float32))
                    
                    # Create a simple "incorrect" sound (lower frequency)
                    incorrect_data = np.sin(2 * np.pi * 220 * t) * 0.5
                    wavfile.write("incorrect.wav", sample_rate, incorrect_data.astype(np.float32))
                    
                    print("Created sound effect files.")
                except ImportError:
                    print("NumPy and SciPy required to generate sound files.")
                except Exception as e:
                    print(f"Error creating sound files: {e}")
            
            # Try to load the sound files
            self.correct_sound = pygame.mixer.Sound("correct.wav")
            self.incorrect_sound = pygame.mixer.Sound("incorrect.wav")
            self.sound_available = True
            print("Sound effects loaded successfully.")
        except Exception as e:
            print(f"Could not load sound effects: {e}")
            self.sound_available = False
        
    def setup_question(self) -> None:
        """Set up the current question and answer buttons."""
        if self.current_question_index >= self.total_questions:
            return
            
        question = self.questions[self.current_question_index]
        
        # Create buttons for answers
        self.buttons = []
        self.next_button = None
        self.background_color = WHITE
        
        # Randomly decide button positions for correct and incorrect answers
        if random.choice([True, False]):
            correct_button = Button(
                (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
                SCREEN_HEIGHT // 2,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                question["correct"]
            )
            incorrect_button = Button(
                (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
                SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_MARGIN,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                question["incorrect"]
            )
        else:
            incorrect_button = Button(
                (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
                SCREEN_HEIGHT // 2,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                question["incorrect"]
            )
            correct_button = Button(
                (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
                SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_MARGIN,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                question["correct"]
            )
            
        self.buttons.append(correct_button)
        self.buttons.append(incorrect_button)
        
    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle mouse click events."""
        if self.show_feedback:
            # If showing feedback, check if next button is clicked
            if self.next_button and self.next_button.is_clicked(pos):
                self.show_feedback = False
                self.celebration_active = False
                self.celebration_particles = []
                self.current_question_index += 1
                if self.current_question_index < self.total_questions:
                    self.setup_question()
            return
            
        current_question = self.questions[self.current_question_index]
        
        for button in self.buttons:
            if button.is_clicked(pos):
                if button.text == current_question["correct"]:
                    self.score += 1
                    self.feedback_text = "正解!"
                    self.feedback_color = GREEN
                    self.background_color = LIGHT_GREEN
                    
                    # Start celebration effects
                    self.celebration_active = True
                    self.celebration_start_time = pygame.time.get_ticks()
                    self.create_celebration_particles()
                    
                    if self.sound_available:
                        self.correct_sound.play()
                else:
                    self.feedback_text = f"不正解! 正解は {current_question['correct']} です。"
                    self.feedback_color = RED
                    self.background_color = LIGHT_RED
                    self.celebration_active = False
                    if self.sound_available:
                        self.incorrect_sound.play()
                
                self.explanation_text = current_question["explanation"]
                self.show_feedback = True
                
                # Create next button with ASCII text
                self.next_button = Button(
                    (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
                    SCREEN_HEIGHT - 80,
                    BUTTON_WIDTH, BUTTON_HEIGHT,
                    "Next Question"
                )
                self.next_button.color = BLUE
                self.next_button.text_color = WHITE
                
                break
                
    def update(self) -> None:
        """Update game state."""
        # Update celebration effects
        if self.celebration_active:
            self.update_celebration()
            
            # Check if celebration duration has passed
            current_time = pygame.time.get_ticks()
            if current_time - self.celebration_start_time > self.celebration_duration:
                self.celebration_active = False
                self.celebration_particles = []
            
    def create_celebration_particles(self):
        """Create particles for celebration effect."""
        self.celebration_particles = []
        for _ in range(100):  # Create 100 particles
            particle = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(5, 15),
                'color': random.choice([GOLD, GREEN, BLUE, (255, 105, 180)]),  # Gold, Green, Blue, Hot Pink
                'speed_x': random.uniform(-3, 3),
                'speed_y': random.uniform(-3, 3)
            }
            self.celebration_particles.append(particle)
    
    def update_celebration(self):
        """Update celebration particles."""
        if not self.celebration_active:
            return
            
        # Update particle positions
        for particle in self.celebration_particles:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            
            # Bounce off edges
            if particle['x'] <= 0 or particle['x'] >= SCREEN_WIDTH:
                particle['speed_x'] *= -1
            if particle['y'] <= 0 or particle['y'] >= SCREEN_HEIGHT:
                particle['speed_y'] *= -1
                
    def draw_celebration_particles(self):
        """Draw celebration particle effects."""
        if not self.celebration_active:
            return
            
        # Draw particles
        for particle in self.celebration_particles:
            pygame.draw.circle(
                self.screen,
                particle['color'],
                (int(particle['x']), int(particle['y'])),
                particle['size']
            )
            
    def draw_celebration_text(self):
        """Draw celebration text effect."""
        if not self.celebration_active:
            return
            
        # Draw celebratory text
        elapsed_time = pygame.time.get_ticks() - self.celebration_start_time
        if elapsed_time < 2000:  # Show text for 2 seconds
            # Make text pulse/grow
            scale = 1.0 + 0.2 * abs(math.sin(elapsed_time / 200))
            size = int(FONT_SIZE * 1.5 * scale)
            
            # Create a larger font for the celebration text
            celebration_font = pygame.font.SysFont(self.font_name, size)
            
            # Main text with gold color (no shadow)
            celebration_text = celebration_font.render("素晴らしい!", True, GOLD)
            celebration_rect = celebration_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            self.screen.blit(celebration_text, celebration_rect)
            celebration_rect = celebration_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            self.screen.blit(celebration_text, celebration_rect)
                
    def draw(self) -> None:
        """Draw the game screen."""
        # Set background color - special colors for results screen
        if self.current_question_index >= self.total_questions:
            # Set background color based on score for the results screen
            percentage = (self.score / self.total_questions) * 100
            if percentage >= 80:
                self.screen.fill((255, 250, 205))  # Light golden yellow
            elif percentage >= 60:
                self.screen.fill((230, 230, 250))  # Lavender
            else:
                self.screen.fill((240, 248, 255))  # Alice blue
        else:
            # Normal background for questions
            self.screen.fill(self.background_color)
        
        # Draw celebration effects for correct answers (behind everything else)
        if self.celebration_active:
            self.draw_celebration_particles()
        
        # Draw game title
        title_text = self.title_font.render("AWS 人名クイズ", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Draw score
        score_text = self.font_small.render(f"スコア: {self.score}/{self.total_questions}", True, BLACK)
        self.screen.blit(score_text, (20, 20))
        
        # Draw progress bar
        if self.current_question_index < self.total_questions:
            self.draw_progress_bar()
        
        if self.current_question_index < self.total_questions:
            # Draw current question
            question = self.questions[self.current_question_index]
            question_text = self.font_medium.render(f"この名前は何のAWSサービス？", True, BLACK)
            question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 30))
            self.screen.blit(question_text, question_rect)
            
            # Draw the Japanese name
            name_text = self.font_large.render(question["name"], True, BLUE)
            name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 20))
            self.screen.blit(name_text, name_rect)
            
            # Draw buttons if not showing feedback
            if not self.show_feedback:
                for button in self.buttons:
                    button.draw(self.screen)
            else:
                # Draw feedback without clearing the question area
                
                # Draw feedback
                feedback_text = self.font_medium.render(self.feedback_text, True, self.feedback_color)
                feedback_rect = feedback_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(feedback_text, feedback_rect)
                
                # Draw explanation
                lines = self._wrap_text(self.explanation_text, self.font_small, SCREEN_WIDTH - 100)
                for i, line in enumerate(lines):
                    line_text = self.font_small.render(line, True, BLACK)
                    line_rect = line_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40 + i * 30))
                    self.screen.blit(line_text, line_rect)
                
                # Draw next button
                if self.next_button:
                    self.next_button.draw(self.screen)
                    
                # Draw celebration text effect for correct answers (on top of everything)
                if self.celebration_active:
                    self.draw_celebration_text()
        else:
            # Draw final score with special effects
            percentage = (self.score / self.total_questions) * 100
            
            # Draw golden particles for high scores
            if percentage >= 80:
                self.draw_results_celebration()
            
            # Draw final score with appropriate color
            if percentage >= 80:
                score_color = GOLD
            elif percentage >= 60:
                score_color = (75, 0, 130)  # Indigo
            else:
                score_color = BLUE
                
            final_text = self.font_large.render(f"最終スコア: {self.score}/{self.total_questions}", True, score_color)
            final_rect = final_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(final_text, final_rect)
            
            # Draw message based on score
            percentage = (self.score / self.total_questions) * 100
            if percentage >= 80:
                message = "素晴らしい! あなたはAWSマスターです!"
                message_en = "Excellent! You're an AWS master!"
                message_color = GOLD
            elif percentage >= 60:
                message = "よくできました! AWSサービスをよく知っていますね!"
                message_en = "Good job! You know your AWS services well!"
                message_color = (75, 0, 130)  # Indigo
            else:
                message = "頑張って! もっと勉強すればAWSマスターになれます!"
                message_en = "Keep learning! You'll master AWS services soon!"
                message_color = BLUE
                
            message_text = self.font_medium.render(message, True, message_color)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(message_text, message_rect)
            
            message_en_text = self.font_small.render(message_en, True, message_color)
            message_en_rect = message_en_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(message_en_text, message_en_rect)
            
            # Draw restart instruction
            restart_text = self.font_small.render("リスタート: R キー / 終了: Q キー", True, BLACK)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            self.screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()
    
    def draw_progress_bar(self):
        """Draw a progress bar showing current question number."""
        # Draw progress bar
        progress_bg_rect = pygame.Rect(50, 80, SCREEN_WIDTH - 100, PROGRESS_BAR_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, progress_bg_rect, border_radius=5)
        
        # Calculate progress
        progress_width = ((self.current_question_index) / self.total_questions) * (SCREEN_WIDTH - 100)
        progress_rect = pygame.Rect(50, 80, progress_width, PROGRESS_BAR_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_BLUE, progress_rect, border_radius=5)
        
        # Draw segment markers
        segment_width = (SCREEN_WIDTH - 100) / self.total_questions
        for i in range(self.total_questions + 1):
            x_pos = 50 + i * segment_width
            pygame.draw.line(self.screen, BLACK, (x_pos, 80), (x_pos, 80 + PROGRESS_BAR_HEIGHT), 2)
        
        # Draw question number
        question_num_text = self.font_small.render(f"問題 {self.current_question_index + 1}/{self.total_questions}", True, BLACK)
        question_num_rect = question_num_text.get_rect(center=(SCREEN_WIDTH // 2, 110))
        self.screen.blit(question_num_text, question_num_rect)
        
    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """Wrap text to fit within a certain width."""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
        
    def restart(self) -> None:
        """Restart the game."""
        self.current_question_index = 0
        self.score = 0
        self.select_random_questions()
        self.show_feedback = False
        self.background_color = WHITE
        self.celebration_active = False
        self.celebration_particles = []
        self.setup_question()
        
    def draw_results_celebration(self):
        """Draw celebration effects for high scores on the results screen."""
        # Draw golden particles
        for i in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(3, 8)
            pygame.draw.circle(self.screen, GOLD, (x, y), size)
            
        # Draw stars
        for i in range(20):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            size = random.randint(10, 20)
            self.draw_star(x, y, size, GOLD)
    
    def draw_star(self, x, y, size, color):
        """Draw a star shape."""
        points = []
        for i in range(10):
            angle = math.pi * 2 * i / 10
            radius = size if i % 2 == 0 else size / 2
            point_x = x + radius * math.sin(angle)
            point_y = y + radius * math.cos(angle)
            points.append((point_x, point_y))
        pygame.draw.polygon(self.screen, color, points)


def main():
    """Main function to run the game."""
    game = QuizGame()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if game.current_question_index >= game.total_questions:
                    if event.key == pygame.K_r:
                        game.restart()
                    elif event.key == pygame.K_q:
                        running = False
                        
        game.update()
        game.draw()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
