import pygame

class Font:
    def __init__(self, img, hor_spacing=1):
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','.',',','"','\'','?','!','_','#','%','&','(',')','+','-','/',':','<','>']
        self.characters = {}
        self.spacing = hor_spacing
        self.space_width = 3
        font_img = img
        char_width = 0
        char_count = 0
        for i in range(font_img.get_width()):
            color = font_img.get_at((i,0))
            if color == (255,0,0):
                char_img = self.cut_image(font_img, i - char_width, 0, char_width, font_img.get_height())
                self.characters[self.character_order[char_count]] = char_img
                char_count += 1
                char_width = 0
            else:
                char_width += 1

        self.height = self.characters['A'].get_height()

    def cut_image(self,surf,x,y,width,height):
        surf_copy = surf.copy()
        clip = pygame.Rect(x,y,width,height)
        surf_copy.set_clip(clip)
        cut = surf.subsurface(surf_copy.get_clip())
        return cut.copy()

    def palette_swap(self, img, old_color, new_color):
        img_copy = pygame.Surface(img.get_size())
        img_copy.fill(new_color)
        img.set_colorkey(old_color)
        img_copy.blit(img,(0,0))
        return img_copy

    def get_width(self, text):
        width = 0
        for char in text:
            if char == ' ':
                width += self.space_width
            elif char != '|':
                width += self.characters[char].get_width()
            width += self.spacing
        return width

    def draw(self, text, color=(1,0,0), alpha=255, size=1):
        char_position = 0
        text_surf = pygame.Surface((self.get_width(text), self.height))
        for char in text:
            if char not in self.characters:
                char_position += self.space_width + self.spacing
            else:
                img = self.characters[char]
                img = self.palette_swap(img,(255,255,255),color)
                text_surf.blit(img, (char_position, 0))
                text_surf.set_colorkey((0,0,0))
                text_surf.set_alpha(alpha)
                char_position += self.characters[char].get_width() + self.spacing
        return pygame.transform.scale_by(text_surf, size)      
    