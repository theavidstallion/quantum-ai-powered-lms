"""
AI Video Generator Module
Generates educational Manim animations with voiceover narration
"""
import os
import re
import glob
import subprocess
from pathlib import Path
from datetime import datetime
from groq import Groq
from gtts import gTTS


class VideoGenerator:
    """Generates educational videos with Manim animations and AI narration"""
    
    # Topic-specific visual profiles
    TOPIC_PROFILES = {
        'math': {
            'keywords': ['calculus', 'derivative', 'integral', 'limit', 'matrix', 'vector',
                         'algebra', 'geometry', 'trigonometry', 'fourier', 'eigenvalue',
                         'polynomial', 'function', 'math', 'mathematics', 'pythagorean'],
            'formulas': [
                r'\frac{d}{dx}[f(g(x))] = f\'(g(x)) \cdot g\'(x)',
                r'\int_a^b f(x)\,dx = F(b) - F(a)',
                r'e^{i\pi} + 1 = 0',
                r'a^2 + b^2 = c^2',
            ],
            'visual_guide': '''
- Axes() for ALL function plots, x_length=7, y_length=4
- MathTex(r"...") for formulas at .to_edge(DOWN)
- Create(graph) to animate curve drawing
- Color formula terms: BLUE=variable, YELLOW=constant, GREEN=result
- Text title .to_edge(UP), diagram .move_to(ORIGIN), formula .to_edge(DOWN)
'''
        },
        'physics': {
            'keywords': ['physics', 'mechanics', 'quantum', 'force', 'energy', 'momentum',
                         'velocity', 'gravity', 'newton', 'electric', 'magnetic', 'wave'],
            'formulas': [r'F = ma', r'E = mc^2', r'KE = \frac{1}{2}mv^2', r'p = mv'],
            'visual_guide': '''
- Arrow() for forces with labels
- Axes() for motion graphs
- Color: RED=force, BLUE=velocity, GREEN=acceleration
- Text title .to_edge(UP), diagram .move_to(ORIGIN), formula .to_edge(DOWN)
'''
        },
        'dsa': {
            'keywords': ['array', 'tree', 'graph', 'stack', 'queue', 'sorting', 'bfs', 'dfs',
                         'recursion', 'algorithm', 'complexity', 'binary', 'linked list', 'dsa'],
            'formulas': [r'O(n)', r'O(\log n)', r'O(n \log n)', r'O(n^2)'],
            'visual_guide': '''
- Square() for array cells, arrange(RIGHT), fill_color for states
- Dot() for graph/tree nodes with Line() edges
- Color: YELLOW=active, GREEN=sorted, RED=error, BLUE=default
- Text title .to_edge(UP), diagram .move_to(ORIGIN), complexity .to_edge(DOWN)
'''
        },
        'ml': {
            'keywords': ['machine learning', 'regression', 'classification', 'gradient',
                         'neural network', 'training', 'loss', 'model', 'ml', 'ai', 'knn'],
            'formulas': [r'J(\theta) = \frac{1}{2m}\sum(h_\theta(x)-y)^2'],
            'visual_guide': '''
- Axes() for plots with Dot() data points
- Sigmoid: ParametricFunction(lambda t: np.array([t, 1/(1+np.exp(-t)), 0]))
- Color: BLUE=class0, RED=class1
- Text title .to_edge(UP), diagram .move_to(ORIGIN), formula .to_edge(DOWN)
'''
        },
        'default': {
            'keywords': [],
            'formulas': [],
            'visual_guide': '''
- BLUE=primary, GREEN=positive, RED=negative, YELLOW=highlight
- Animate step by step
- Text title .to_edge(UP), diagram .move_to(ORIGIN), formula .to_edge(DOWN)
'''
        }
    }

    def __init__(self, groq_api_key, output_dir='output/videos'):
        """Initialize video generator with Groq API key"""
        self.client = Groq(api_key=groq_api_key)
        self.model = "llama-3.3-70b-versatile"
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def detect_topic_profile(self, topic):
        """Detect topic type and return appropriate visual profile"""
        topic_lower = topic.lower()
        for name, profile in self.TOPIC_PROFILES.items():
            if name == 'default':
                continue
            if any(kw in topic_lower for kw in profile['keywords']):
                print(f'🎨 Detected topic: {name.upper()}')
                return profile
        print('🎨 Using default visual style')
        return self.TOPIC_PROFILES['default']
    
    def generate_narration_script(self, topic):
        """Generate educational narration script using Groq"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': f'''Write a clear 60-second educational narration script about "{topic}".
Plain text only, no headers or bullet points.
Make it engaging and suitable for a visual explainer video.
Focus on key concepts, examples, and practical applications.'''
                }],
                temperature=0.7,
                max_tokens=500
            )
            script = response.choices[0].message.content.strip()
            return script
        except Exception as e:
            print(f"❌ Script generation error: {e}")
            return f"Welcome to this educational video about {topic}. Let's explore the key concepts together."
    
    def text_to_speech(self, script, filename='narration.mp3'):
        """Convert script to speech using gTTS"""
        try:
            audio_path = os.path.join(self.output_dir, filename)
            tts = gTTS(text=script, lang='en', slow=False)
            tts.save(audio_path)
            
            # Estimate duration (150 words per minute)
            words = len(script.split())
            duration = (words / 150) * 60
            
            print(f'🎙️ Audio: {audio_path} (~{duration:.0f}s)')
            return audio_path, duration
        except Exception as e:
            print(f"❌ TTS error: {e}")
            return None, 30
    
    def generate_manim_code(self, topic, duration_seconds, visual_guide, formulas='', error_log=''):
        """Generate Manim animation code using Groq"""
        try:
            formula_hints = ''
            if formulas:
                formula_hints = '\n\nKEY FORMULAS TO SHOW:\n'
                for f in formulas[:3]:
                    formula_hints += f'  MathTex(r"{f}")\n'
            
            system_prompt = f'''You are a Manim CE expert. Generate ONLY raw Python code, no markdown.

RULES:
1. Class name: GeneratedVideo(Scene)
2. Start with: from manim import *\\nimport numpy as np
3. Duration: ~{duration_seconds:.0f} seconds total
4. LAYOUT (NO OVERLAP):
   - Title: .to_edge(UP) — short title only
   - Main: .move_to(ORIGIN) — diagram or graph
   - Formula: .to_edge(DOWN) — MathTex only
5. FadeOut(*self.mobjects) between stages
6. NO text narration — audio handles it
7. Use self.wait() to match audio timing

⚠️ CRITICAL RESTRICTIONS:
- DO NOT use SVGMobject, ImageMobject, or any external file references
- DO NOT reference files like "assets/...", "images/...", etc.
- ONLY use built-in Manim objects: Circle, Square, Rectangle, Line, Arrow, Text, MathTex, Dot, VGroup, Polygon, etc.
- Create diagrams using geometric primitives and positioning

{visual_guide}
{formula_hints}'''

            user_prompt = f'Topic: {topic}'
            if error_log:
                user_prompt += f'\n\nFix this error:\n{error_log[-1500:]}'
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            code = response.choices[0].message.content.strip()
            
            # Extract code from markdown if present
            if '```' in code:
                code = code.split('```python')[-1].split('```')[0].strip()
            
            return code
        except Exception as e:
            print(f"❌ Code generation error: {e}")
            return self._fallback_code(topic)
    
    def _fallback_code(self, topic):
        """Fallback Manim code if generation fails"""
        return f'''from manim import *
import numpy as np

class GeneratedVideo(Scene):
    def construct(self):
        title = Text("{topic}", font_size=48, color=BLUE).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        subtitle = Text("Educational Explainer", font_size=32).move_to(ORIGIN)
        self.play(FadeIn(subtitle))
        self.wait(2)
        
        formula = MathTex(r"f(x) = ax^2 + bx + c", font_size=40).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(2)
        
        self.play(FadeOut(*self.mobjects))
        self.wait(1)
'''
    
    def render_manim(self, code, scene_name='GeneratedVideo'):
        """Render Manim animation to video file with timeout and progress tracking"""
        try:
            # Save code to temporary file
            code_path = os.path.join(self.output_dir, 'temp_scene.py')
            with open(code_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            print(f'   📄 Scene file: {code_path}')
            print(f'   🎬 Starting Manim render (3 minute timeout)...')
            print(f'   ⏳ This may take 30-180 seconds depending on complexity')
            
            # Run Manim with proper timeout handling
            try:
                result = subprocess.run(
                    ['python', '-m', 'manim', code_path, scene_name,
                     '-ql', '--media_dir', self.output_dir, '--disable_caching'],
                    capture_output=True,
                    text=True,
                    timeout=180  # 3 minutes max
                )
                
                print(f'   ✅ Manim process completed (return code: {result.returncode})')
                
                # Show stdout/stderr for debugging
                if result.stdout:
                    print(f'   📋 Output preview: {result.stdout[:200]}')
                
                if result.returncode != 0:
                    print(f'   ❌ Manim failed with errors:')
                    print(f'   {result.stderr[:500]}')
                    return False, None, result.stderr
                
            except subprocess.TimeoutExpired:
                print(f'   ⏰ TIMEOUT: Manim took longer than 3 minutes!')
                print(f'   💡 This usually means:')
                print(f'      - LaTeX compilation is stuck (try simpler topics)')
                print(f'      - Memory issues (close other programs)')
                print(f'      - Manim configuration problem')
                return False, None, 'Rendering timeout after 180 seconds'
            
            # Find the rendered video
            print(f'   🔍 Searching for rendered video...')
            
            # Try multiple potential locations
            search_patterns = [
                os.path.join(self.output_dir, 'videos', '**', '*.mp4'),
                os.path.join(self.output_dir, '**', '*.mp4'),
                os.path.join(os.path.dirname(code_path), 'media', '**', '*.mp4')
            ]
            
            video_files = []
            for pattern in search_patterns:
                found = glob.glob(pattern, recursive=True)
                if found:
                    video_files.extend(found)
                    print(f'      Found {len(found)} file(s) in {pattern}')
            
            if video_files:
                # Get most recent file
                video_files.sort(key=os.path.getmtime, reverse=True)
                video_path = video_files[0]
                file_size = os.path.getsize(video_path) / 1024  # KB
                print(f'   ✅ Video found: {os.path.basename(video_path)} ({file_size:.1f} KB)')
                return True, video_path, ''
            else:
                print(f'   ❌ No video file found after rendering')
                print(f'   📂 Checked directories:')
                for pattern in search_patterns:
                    print(f'      - {pattern}')
                return False, None, 'Video file not found after rendering'
            
        except Exception as e:
            print(f'   ❌ Unexpected error: {str(e)}')
            import traceback
            traceback.print_exc()
            return False, None, str(e)
    
    def merge_video_audio(self, video_path, audio_path, output_name='final_video.mp4'):
        """Merge video and audio using ffmpeg"""
        try:
            final_path = os.path.join(self.output_dir, output_name)
            
            result = subprocess.run([
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                final_path
            ], capture_output=True, timeout=60)
            
            if result.returncode == 0 and os.path.exists(final_path):
                print(f'🎞️ Final video: {final_path}')
                return final_path
            return None
        except Exception as e:
            print(f"❌ Merge error: {e}")
            return None
    
    def generate_video(self, topic, max_attempts=3):
        """
        Complete video generation pipeline with detailed progress tracking
        Returns: (success, video_path, script, error_message)
        """
        start_time = datetime.now()
        print(f"\n{'='*60}")
        print(f"🎓 VIDEO GENERATION STARTED")
        print(f"📌 Topic: {topic}")
        print(f"🕐 Time: {start_time.strftime('%H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Detect topic profile
        profile = self.detect_topic_profile(topic)
        visual_guide = profile['visual_guide']
        formulas = profile.get('formulas', [])
        
        # Step 1: Generate narration
        print('\n📝 STEP 1/5: Generating narration script...')
        script = self.generate_narration_script(topic)
        print(f'   ✅ Script generated ({len(script)} chars)')
        print(f'   Preview: "{script[:80]}..."')
        
        # Step 2: Convert to speech
        print('\n🎙️ STEP 2/5: Converting text to speech...')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_filename = f'{timestamp}_audio.mp3'
        audio_path, duration = self.text_to_speech(script, audio_filename)
        
        if not audio_path:
            error_msg = "Failed to generate audio"
            print(f'   ❌ {error_msg}')
            return False, None, script, error_msg
        
        print(f'   ✅ Audio saved: {audio_filename} (~{duration:.0f}s)')
        
        # Step 3-4: Generate and render animation
        error_log = ''
        video_path = None
        
        for attempt in range(1, max_attempts + 1):
            print(f'\n🎨 STEP 3/5: Generating Manim code (Attempt {attempt}/{max_attempts})...')
            
            # Generate Manim code
            code = self.generate_manim_code(topic, duration, visual_guide, formulas, error_log)
            print(f'   ✅ Code generated ({len(code)} chars)')
            
            # Render animation
            print(f'\n🎬 STEP 4/5: Rendering animation (Attempt {attempt}/{max_attempts})...')
            success, video_path, error_log = self.render_manim(code)
            
            if success:
                print(f'   ✅ Animation rendered successfully!')
                break
            else:
                print(f'   ⚠️ Attempt {attempt} failed')
                if attempt < max_attempts:
                    print(f'   🔄 Retrying with error correction...')
                else:
                    print(f'   ❌ Max attempts reached')
        
        if not video_path:
            error_msg = f"Animation rendering failed after {max_attempts} attempts: {error_log[:200]}"
            print(f'\n❌ GENERATION FAILED: {error_msg}')
            return False, None, script, error_msg
        
        # Step 5: Merge video and audio
        print(f'\n🎞️ STEP 5/5: Merging video and audio...')
        final_filename = f'{timestamp}_{re.sub(r"[^a-z0-9]+", "_", topic.lower())}.mp4'
        final_path = self.merge_video_audio(video_path, audio_path, final_filename)
        
        if not final_path:
            error_msg = "Failed to merge video and audio"
            print(f'   ❌ {error_msg}')
            return False, None, script, error_msg
        
        # Success!
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"\n{'='*60}")
        print(f"🎉 VIDEO GENERATION COMPLETE!")
        print(f"📁 File: {os.path.basename(final_path)}")
        print(f"⏱️ Total time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
        print(f"📏 File size: {os.path.getsize(final_path)/1024/1024:.2f} MB")
        print(f"{'='*60}\n")
        
        return True, final_path, script, None
