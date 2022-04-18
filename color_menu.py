class color_menu:
    def __init__(self):
        self.colors = [
            '#00FFFF', #BLUE
            '#8A2BE2', #PURPLE
            '#DC143C', #RED
            '#FFD700', #YELLOW
            '#FF69B4', #PINK
            '#FF4500', #ORANGE
            '#DDA0DD', #PLUM
            '#00FF7F', #GREEN
            '#800000', #MAROON
            '#BDB76B', #KHAKI
        ]
    
    def swap_color(self, idx, new_color):
        self.colors[idx] = new_color

    def add_color(self, new_color):
        self.colors.append(new_color)
    
    def generate_window(self):
        return

        

