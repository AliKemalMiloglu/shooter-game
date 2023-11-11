from pygame import *
from random import randint
 
#Arka plan müziği
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# fontlar ve yazılar
font.init()
font2 = font.Font(None,36)

# oyun sonu yazıları
font1 =font.Font(None,80)
win = font1.render("YOU WIN!",True,(255,255,255))
lose = font1.render("YOU LOSE!!",True,(180,0,0))

# sayaçlar
score = 0 # düşmüş gemiler
lost = 0 # kaçırılan gemiler
max_lost = 3 # bu kadar uzaylı geçişi olur ise kaybettin
goal = 10 # kazanmak için vurulması gereken gemi sayısı

#böyle resimlere ihtiyacımız var:
img_back = "galaxy.jpg" #oyunun arka planı
img_hero = "rocket.png" #kahraman
img_enemy = "ufo.png" # düşman
img_bullet = "bullet.png" # mermi

#sprite'lar için ebeveyn sınıfı
class GameSprite(sprite.Sprite):
 #Sınıf kurucusu
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Sınıf yapıcısını (Sprite) çağırın:
       sprite.Sprite.__init__(self)
 
       # Her sprite image - resim özelliğini depolamalıdır
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
       # Her sprite, içine yazıldığı dikdörtgenin  rect özelliğini saklamalıdır
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #pencereye kahraman çizen yöntem
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
#ana oyuncunun sınıfı
class Player(GameSprite):
   #Sprite'ı klavye oklarıyla kontrol etme yöntemi
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 # atış yöntemi (o
   def fire(self):
       bullet = Bullet(img_bullet,self.rect.centerx-7,self.rect.top,15,20,-15)
       bullets.add(bullet)
       

# Sprite Düşman sınıfı
class Enemy (GameSprite):
    # Düşmanın hareketi
    def update(self):
        self.rect.y +=self.speed
        global lost 
        # ekranın kenarına gelince kaybolur
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

# mermi sprite sınıfı
class Bullet(GameSprite):
    # Mermi hareketi
    def update(self):
        self.rect.y +=self.speed
        if self.rect.y < 0:
            self.kill()

#Bir pencere oluştur
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#sozdayem spraytyvolume_up16 / 5.000Çeviri sonuçları# sprite oluştur 
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# monster grubu 
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
    monsters.add(monster)

# mermi grubu 
bullets = sprite.Group()


# "oyun bitti" değişkeni: True olduğunda, sprite ana döngüde çalışmayı durdurur
finish = False
#Ana oyun döngüsü:
run = True #bayrak pencereyi kapat düğmesiyle sıfırlanır
while run:
   #Kapat düğmesindeki olayı tıklayın
   for e in event.get():
       if e.type == QUIT:
           run = False
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()
 
   if not finish:
       # arka planı güncelliyoruz
       window.blit(background,(0,0))

       # ekrana metin yazıyoruz
       text = font2.render("Score:"+str(score),1,(255,255,255))
       window.blit(text,(10,20))

       text_lose = font2.render("Missed:"+str(lost),1,(255,255,0))
       window.blit(text_lose,(10,50))

 
       #sprite hareketleri üretiyoruz
       ship.update()
       monsters.update()
       bullets.update()
 
       #Döngünün her yinelemesinde onları yeni bir konumda güncelliyoruz
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       # mermi ile  uzaylının carpışmasını burada düzenleyeceğiz
       collides = sprite.groupcollide(monsters,bullets,True,True)
       for c in collides:
           score = score + 1
           monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,6))
           monsters.add(monster)
        
        # uzaylı ile kahramanın çarpışması 
       if sprite.spritecollide(ship,monsters,False) or lost >= max_lost:
            finish = True # oyun döngüsü tamamlandı
            window.blit(lose,(200,210))
       
       if score >= goal:
           finish = True
           window.blit(win,(200,210))
           
       display.update()

     
   else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        
        time.delay(2000)
        for i in range(1,7):
            monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(2,8))
            monsters.add(monster)
   
   #loop her 0,05 saniyede bir çalışır
   time.delay(50)