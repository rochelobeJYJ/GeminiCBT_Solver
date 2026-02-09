
from google import genai
from PIL import Image

class GeminiSolver:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model_name

    def optimize_image(self, image_path: str) -> Image.Image:
        """
        Resize image to max width 800px and return PIL Image object.
        """
        img = Image.open(image_path)
        max_width = 800
        if img.width > max_width:
            w_percent = (max_width / float(img.width))
            h_size = int((float(img.height) * float(w_percent)))
            img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
        return img

    def solve_problem_stream(self, image_path: str, context: str = ""):
        """
        Generator function to stream response from Gemini API using google-genai.
        """
        img = self.optimize_image(image_path)
        
        if not context.strip():
            context = "모든 과목"

        prompt = f"""
        Role: 당신은 {context} 전문가입니다.
        Task: 이미지를 보고 문제를 정확히 분석하여 정답을 찾고, 그에 대한 명확한 해설을 제공하세요.
        Language: 한국어(Korean)
        Output Format:
        - 정답을 가장 먼저 **굵게** 표시하세요.
        - 줄바꿈 후, 한 문단 길이의 핵심 해설을 작성하세요.
        """

        # Using google-genai SDK
        # Pass both prompt (str) and image (PIL.Image or path) in `contents`.
        # The new SDK supports PIL images directly in the contents list.
        response_stream = self.client.models.generate_content_stream(
            model=self.model,
            contents=[prompt, img]
        )

        for chunk in response_stream:
            # chunk.text is the attribute for text content in the new SDK too
            if chunk.text:
                yield chunk.text
