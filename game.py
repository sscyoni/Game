import tkinter as tk
import random

class AppleGame:
    def __init__(self, root):
        self.root = root 
        root.title("🍎 사과 숫자 합 게임 (시간어택)") 
        # --- 게임 변수 초기화 ---
        self.MAX_APPLES = 20          
        self.initial_game_time = 60   
        self.time_left = self.initial_game_time
        
        self.score = 0
        self.life = 3
        self.target = 10 
        self.selected_apples = []     
        self.current_sum = 0
        self.apple_data = {}          
        self.game_running = True      
        
        # --- UI 요소 생성 및 배치 ---
        info_frame = tk.Frame(root) 
        info_frame.pack(pady=10)
        
        self.score_label = tk.Label(info_frame, text=f"점수: {self.score}", font=('Arial', 14))
        self.score_label.pack(side=tk.LEFT, padx=15)
        
        self.life_label = tk.Label(info_frame, text=f"Life: {self.life}", font=('Arial', 14, 'bold'), fg='red')
        self.life_label.pack(side=tk.LEFT, padx=15)
        
        self.timer_label = tk.Label(info_frame, text=f"⏰ 시간: {self.time_left}", font=('Arial', 14, 'italic'), fg='blue')
        self.timer_label.pack(side=tk.LEFT, padx=15)
        
        self.target_label = tk.Label(info_frame, text=f"⭐ 목표: {self.target} ⭐", font=('Arial', 16, 'underline'))
        self.target_label.pack(side=tk.LEFT, padx=15)
        
        self.restart_button = tk.Button(
            info_frame, 
            text="🔄 재시작", 
            command=self.restart,
            font=('Arial', 14, 'bold'),
            bg='lightgreen',
            fg='black'
        )
        self.restart_button.pack(side=tk.LEFT, padx=15)
        
        self.sum_label = tk.Label(root, text=f"현재 합계: {self.current_sum}", font=('Arial', 18, 'bold')) # root 사용
        self.sum_label.pack(pady=10)
        
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='#E0FFFF', relief=tk.SUNKEN, borderwidth=2) # root 사용
        self.canvas.pack(padx=10, pady=10)
        
        self.canvas.bind("<Button-1>", self.on_apple_click)
    
        self.initialize_game()

    def initialize_game(self):
        self.spawn_new_apples(self.MAX_APPLES) 
        self.update_ui()
        self.countdown() 
        self.periodic_apple_check() 

    # --- 사과 생성 및 관리 ---
    def create_apple(self, number, x, y):
        radius = 30
        
        apple_id = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill="red", outline="darkred", width=2, tags=("apple_body",)
        )
        
        text_id = self.canvas.create_text(
            x, y, text=str(number), fill="white", font=('Arial', 18, 'bold'),
            tags=("apple_text",)
        )
        
        self.apple_data[apple_id] = {'number': number, 'text_id': text_id, 'is_selected': False}
        return apple_id
        
    def spawn_new_apples(self, count):
        actual_count = 0
        for _ in range(count):
            if len(self.apple_data) < self.MAX_APPLES:
                number = random.randint(1, 9)
                x = random.randint(50, self.canvas_width - 50)
                y = random.randint(50, self.canvas_height - 50)
                self.create_apple(number, x, y)
                actual_count += 1
        return actual_count

    def periodic_apple_check(self):
        if not self.game_running:
            return

        if len(self.apple_data) < self.MAX_APPLES:
            self.spawn_new_apples(1) 
        
       
        self.root.after(3000, self.periodic_apple_check)

    def on_apple_click(self, event):
        if not self.game_running:
            return
        # 클릭 로직 (생략)
        clicked_item_ids = self.canvas.find_closest(event.x, event.y)
        apple_id = None 
        
        for item_id in clicked_item_ids:
            if item_id in self.apple_data:
                apple_id = item_id
                break
            elif "apple_text" in self.canvas.gettags(item_id):
                for oval_id, data in self.apple_data.items():
                    if data['text_id'] == item_id:
                        apple_id = oval_id
                        break
                if apple_id:
                    break
        
        if apple_id:
            self.toggle_apple(apple_id)
            self.check_game_state()

    def toggle_apple(self, apple_id):
        data = self.apple_data.get(apple_id)
        if not data:
            return
        # 토글 로직 (생략)
        is_selected = data['is_selected']
        apple_number = data['number']

        if is_selected:
            self.canvas.itemconfig(apple_id, fill="red", outline="darkred")
            self.selected_apples.remove(apple_id)
            self.current_sum -= apple_number
            data['is_selected'] = False
        else:
            self.canvas.itemconfig(apple_id, fill="yellow", outline="gold")
            self.selected_apples.append(apple_id)
            self.current_sum += apple_number
            data['is_selected'] = True
            
        self.update_ui()

    def check_game_state(self):
        # 게임 상태 확인 로직 (생략)
        if self.current_sum == self.target and self.selected_apples:
            removed_count = len(self.selected_apples)
            self.score += 1
            self.remove_selected_apples()
            self.spawn_new_apples(removed_count)
            self.reset_selection()
            self.target = random.randint(8, 15)
            self.update_ui(message="성공! 점수 +1")
            
        elif self.current_sum > self.target:
            self.life -= 1
            self.reset_selection(fail=True)
            self.update_ui(message="실패! 합이 초과되어 라이프 -1")
            
            if self.life <= 0:
                self.game_over(reason="라이프 0")

    def reset_selection(self, fail=False):
        # 선택 해제 로직
        for apple_id in self.selected_apples:
            if apple_id in self.apple_data:
                self.canvas.itemconfig(apple_id, fill="red", outline="darkred")
                self.apple_data[apple_id]['is_selected'] = False
                
        self.selected_apples = []
        self.current_sum = 0
        self.update_ui()
    
    def remove_selected_apples(self):
        # 사과 제거 로직
        for apple_id in self.selected_apples:
            if apple_id in self.apple_data:
                self.canvas.delete(apple_id) 
                self.canvas.delete(self.apple_data[apple_id]['text_id']) 
                del self.apple_data[apple_id]

    def countdown(self):
        if not self.game_running:
            return

        self.time_left -= 1
        self.timer_label.config(text=f"⏰ 시간: {self.time_left}")

        if self.time_left > 0:
            self.root.after(1000, self.countdown) 
        else:
            self.game_over(reason="시간 종료")

    def game_over(self, reason):
        if not self.game_running:
            return
            
        self.game_running = False
        self.canvas.unbind("<Button-1>") 
        
        message = f"--- GAME OVER ({reason}) ---\n"
        message += f"최종 점수: {self.score}"
    
        self.canvas.create_text(
            self.canvas_width / 2, self.canvas_height / 2,
            text=message,
            fill="black", font=('Arial', 30, 'bold'), justify=tk.CENTER, tags="game_over_text"
        )
        
    def update_ui(self, message=""):
        # UI 업데이트 로직 
        self.score_label.config(text=f"점수: {self.score}")
        self.life_label.config(text=f"Life: {self.life}")
        self.target_label.config(text=f"⭐ 목표: {self.target} ⭐")
        self.sum_label.config(text=f"현재 합계: {self.current_sum}")
        
        if message:
            print(f"시스템 메시지: {message}")

    def restart(self):
        self.canvas.delete("all")
        
        # 변수 초기화 로직
        self.score = 0
        self.life = 3
        self.target = 10
        self.selected_apples = []
        self.current_sum = 0
        self.apple_data = {}
        self.game_running = True
        self.time_left = self.initial_game_time
        
        self.canvas.bind("<Button-1>", self.on_apple_click)
        self.initialize_game() 
        
        print("--- 게임이 성공적으로 재시작되었습니다. ---")

if __name__ == '__main__':
    root = tk.Tk()
    game = AppleGame(root)
    root.mainloop()